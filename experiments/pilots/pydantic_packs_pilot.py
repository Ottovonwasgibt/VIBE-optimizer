"""Real API contract smoke test for Pydantic v1 compatibility API and v2 API.

Pydantic.v1 is the compatibility namespace inside Pydantic 2.x, not a
separately installed v1 distribution. The experiments assess versioned
recipe compatibility, NOT the behavior of an LLM or a Vibe agent.
"""
from __future__ import annotations
import importlib.metadata
import json
import sys
import warnings
from pathlib import Path
from pydantic import BaseModel as PydanticV2Base
from pydantic.v1 import BaseModel as PydanticV1Base

class LegacyInvoice(PydanticV1Base):
    amount: int

class ModernInvoice(PydanticV2Base):
    amount: int

OPERATIONS = ('validate', 'serialize', 'json', 'schema', 'copy', 'construct', 'fields')

def apply_recipe(target: str, recipe: str, operation: str):
    cls = LegacyInvoice if target == 'v1' else ModernInvoice
    obj = cls(amount=7)
    if recipe == 'legacy':
        if operation == 'validate': result = cls.parse_obj({'amount': 7}).amount
        elif operation == 'serialize': result = obj.dict()
        elif operation == 'json': result = json.loads(obj.json())
        elif operation == 'schema': result = 'amount' in cls.schema()['properties']
        elif operation == 'copy': result = obj.copy(update={'amount': 8}).amount
        elif operation == 'construct': result = cls.construct(amount=7).amount
        elif operation == 'fields': result = 'amount' in cls.__fields__
    else:
        if operation == 'validate': result = cls.model_validate({'amount': 7}).amount
        elif operation == 'serialize': result = obj.model_dump()
        elif operation == 'json': result = json.loads(obj.model_dump_json())
        elif operation == 'schema': result = 'amount' in cls.model_json_schema()['properties']
        elif operation == 'copy': result = obj.model_copy(update={'amount': 8}).amount
        elif operation == 'construct': result = cls.model_construct(amount=7).amount
        elif operation == 'fields': result = 'amount' in cls.model_fields
    return result

EXPECTED = {
    'validate': 7, 'serialize': {'amount': 7},
    'json': {'amount': 7}, 'schema': True, 'copy': 8,
    'construct': 7, 'fields': True,
}

def evaluate():
    records = []
    for target in ('v1', 'v2'):
        for recipe in ('legacy', 'modern'):
            for operation in OPERATIONS:
                with warnings.catch_warnings(record=True) as ws:
                    warnings.simplefilter('always')
                    try:
                        result = apply_recipe(target, recipe, operation)
                        passed = result == EXPECTED[operation]
                        error = None if passed else 'Unexpected output'
                    except Exception as exc:
                        passed = False
                        error = f'{type(exc).__name__}: {str(exc)[:200]}'
                records.append({
                    'target_api': target, 'recipe': recipe, 'operation': operation,
                    'passed': passed, 'deprecation_warnings': sum(
                        issubclass(w.category, DeprecationWarning) for w in ws),
                    'error': error,
                })
    aggregates = {}
    for target in ('v1', 'v2'):
        for recipe in ('legacy', 'modern'):
            group = [r for r in records if
                     r['target_api'] == target and r['recipe'] == recipe]
            aggregates[target + '__' + recipe] = {
                'passed': sum(r['passed'] for r in group),
                'total': len(group),
                'deprecation_warnings': sum(r['deprecation_warnings'] for r in group),
            }
    return {
        'python': sys.version.split()[0],
        'pydantic': importlib.metadata.version('pydantic'),
        'environment_note': 'pydantic.v1 compatibility API shipped within v2',
        'aggregates': aggregates, 'records': records,
    }

if __name__ == '__main__':
    summary = evaluate()
    print(json.dumps(summary['aggregates'], indent=2))
    (Path(__file__).parent / 'pydantic_packs_results.json').write_text(
        json.dumps(summary, indent=2) + '\n', encoding='utf-8')
