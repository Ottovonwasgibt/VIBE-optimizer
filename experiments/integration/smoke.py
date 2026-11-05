"""Full synthetic end-to-end research smoke, no model or private data.

Runs a real SQLite FTS5 index, approved-only lookup, advisory task routing,
bounded evidence packet, tool delivery audit, safe pure recipe, candidate
verification boundary and paired-score fixture.
"""
from __future__ import annotations

from datetime import date
import json
from pathlib import Path
import sys
import tempfile

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/"src"))
sys.path.insert(0,str(ROOT/"experiments"/"live_agent"))

from vibe_optimizer.knowledge import init_database,stage_document,review_source,search,get_chunk
from vibe_optimizer.capability_registry import CapabilityRegistry,TaskContext
from vibe_optimizer.task_router import Signals
from vibe_optimizer.evidence_packets import Evidence
from vibe_optimizer.capability_loop import advise
from vibe_optimizer.checkpoint_watchdog import SessionCounters
from vibe_optimizer.capability_delivery import audit_delivery
from vibe_optimizer.recipe_compiler import Recipe,evaluate_fixtures
from vibe_optimizer.candidate_governance import propose,adjudicate,ReviewReceipt,applicable
from paired_eval import report


def main() -> None:
    now=date(2026,11,5)
    registry=CapabilityRegistry.load(
        ROOT/"examples"/"capability-workbench"/"catalog.json")
    text=("SYNTHETIC ONLY. Institution enrollment process: "
          "message received, local human decision pending; "
          "no final registration or actual Studielink event code is described.")
    with tempfile.TemporaryDirectory() as temp:
        db=Path(temp)/"public.sqlite"
        init_database(db)
        stage_document(db,source_id="synthetic-ho",
                       uri="synthetic://fictional-institution-flow",
                       title="Fictional HO enrollment flow",
                       content=text,license="test-fixture",
                       version="fixture-v1")
        # This is an offline TEST fixture admin action, not auto-approval.
        review_source(db,source_id="synthetic-ho",
                      reviewer="synthetic-independent-fixture",action="approve")
        retrieved=search(db,"enrollment")
        assert len(retrieved)==1
        chunk=get_chunk(db,retrieved[0]["chunk_id"])
        assert chunk is not None and chunk["source_id"]=="synthetic-ho"

        evidence=Evidence(
            source_id=chunk["source_id"],locator=chunk["locator"],
            revision=chunk["version"],sha256_hex=chunk["sha256"],
            classification="PUBLIC",topic="fictional enrollment",
            excerpt=chunk["body"],observed_at=now
        )
        result=advise(
            task_id="synthetic-ho-check",
            context=TaskContext(
                "Studielink Osiris enrollment status process","windows"),
            signals=Signals(criteria_clear=True,external_capability_needed=True),
            registry=registry,evidence=[evidence],date_of_use=now,
            checkpoint=SessionCounters(tool_calls=25)
        )
        assert "higher_ed_process" in result.candidates
        assert result.evidence_packet["status"]=="evidence_available"
        assert result.checkpoint["action"]=="review"
        assert result.execution_status=="advisory_only_not_executed"

    delivered=audit_delivery(
        qualified_ids=list(result.candidates),
        host_visible_ids=list(result.candidates[:1]),
        host_invocation_ids=[],
        independently_relevant_ids=list(result.candidates[:1])
    )
    recipe_fixture=json.loads(
        (ROOT/"examples"/"script-workshop"/"synthetic-recipe.json").read_text(
            encoding="utf-8"))
    recipe=Recipe.parse(recipe_fixture["recipe"])
    tests=evaluate_fixtures(recipe,recipe_fixture["fixtures"])
    assert tests["all_passed"]
    candidate=propose(
        candidate_id=recipe.recipe_id,kind="function",
        proposer="simulated-agent",candidate_bytes=recipe.manifest_bytes(),
        scope={"test_suite":"synthetic-only"},
        source_refs=["examples/script-workshop/synthetic-recipe.json"]
    )
    assert not applicable(candidate,{"test_suite":"synthetic-only"})
    receipt=ReviewReceipt(
        reviewer="simulated-separate-test-runner",
        observed_content_sha256=candidate.content_sha256,
        validation_refs=("synthetic-recipe-fixtures",),
        tests_passed=True,independently_reproduced=True,
        applicability_confirmed=True,reviewed_at=now
    )
    candidate=adjudicate(
        candidate,receipt,trusted_admin_process=True
    )
    assert applicable(candidate,{"test_suite":"synthetic-only"})
    paired=report(json.loads(
        (ROOT/"experiments"/"live_agent"/"synthetic_results.json").read_text(
            encoding="utf-8")))
    assert paired["evidence_status"]=="synthetic"
    summary={
        "status":"SYNTHETIC INTEGRATION SMOKE ONLY — NO VIBE OR LLM RUN",
        "public_fts5_source_chunks":len(retrieved),
        "candidate_ids":list(result.candidates),
        "evidence_packet_status":result.evidence_packet["status"],
        "checkpoint_decision":result.checkpoint["action"],
        "tool_delivery_missing":list(delivered.missing_from_host),
        "pure_recipe_fixture_passed":tests["fixture_passed"],
        "recipe_qualification_state":"simulated-"+candidate.status,
        "paired_eval_status":paired["evidence_status"],
        "execution":"no real tools/admin actions/agent/model were invoked",
    }
    print(json.dumps(summary,indent=2))


if __name__=="__main__":
    main()
