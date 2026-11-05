# VIBE-optimizer — TDD-07 Adaptive Tool Workbench

**Versie:** onderzoeksontwerp v0.1 · **Datum:** 5 november 2026  
**Status:** concept en technische hypothese; **niet geïmplementeerd of end-to-end getest**.

## 1. Doel

Vergroot de effectieve capaciteit van **één** codingagent door tools als een uitbreidbare, doorzoekbare werkbank beschikbaar te stellen. De agent kan gedurende een taak een ontbrekende capaciteit herkennen, beschikbare instrumenten inspecteren, de meest geschikte kiezen, gebruik aanpassen, meerdere tools combineren of een nieuw instrument als *kandidaat* ontwerpen. Bestaande tools worden niet automatisch geïnstalleerd of machtiger gemaakt.

**Kernvraag:** wat heb ik nodig om de volgende stap betrouwbaar uit te voeren, en heb ik daarvoor het passende en daadwerkelijk bruikbare instrument?

## 2. De cyclische Tool Adequacy Check

Start bij taaktriage, bij een relevante blokkade, na onverwachte tooluitvoer, na gewijzigde requirements en voordat een agent verklaart iets niet te kunnen. Niet na iedere triviale handeling.

```text
Taak / nieuwe observatie
   ↓
Definieer vereiste operatie (capability gap)
   ↓
Tool Adequacy Check
   ├── aanwezig en geschikt? → correct aanroepen
   ├── bekend maar niet geladen? → zoeken, bereikbaarheid toetsen
   ├── geschikt met aanpassing? → argumenten/wrapper/compositie voorstellen
   ├── werkelijk ontbrekend? → kandidaat-tool ontwerpen en testen
   └── te riskant of te duur? → melden / toestemming vragen / stoppen
   ↓
Onafhankelijke observatie of test
   ↓
Taak hervatten; tooluitkomst, kosten en beperkingen registreren
   ↓
Eventuele herbruikbare tool ter beoordeling voorstellen
```

## 3. Drie niveaus van de werkbank

| Niveau | Eigenschappen | Laadstrategie |
|---|---|---|
| **Hot tools** | Vaak nodig, vertrouwd, reeds bruikbaar | Altijd in klein actief palet |
| **Cold tools** | Gedocumenteerd en vindbaar, maar niet actief zichtbaar | Progressive discovery: schema pas inladen als nodig |
| **Candidate tools** | Te ontwikkelen scripts, adapters, niet-geïnstalleerde toolopties | Apart beoordelen, testen en daarna pas beschikbaar stellen |

Houd de toestanden `catalogued`, `installed`, `reachable`, `authorized`, `compatible`, `healthy`, `suitable`, `staged`, `quarantined` uit elkaar. Een tool die op GitHub bestaat is niet automatisch uitvoerbaar binnen Vibe.

## 4. Machine-readable capability card

*Onderstaand is een **eigen voorgesteld JSON-contract**, niet een Vibe- of MCP-standaard.*

```json
{
  "tool_id": "repo.symbol_inspector",
  "version": "0.1.0",
  "summary": "Locate symbols and references in a versioned repository",
  "capabilities": ["find_symbols", "find_references"],
  "limits": {"languages": ["python"], "dirty_tree_supported": false},
  "access": {"kind": "local", "read_only": true, "approval": "host-policy"},
  "lifecycle": "catalogued",
  "health": {"last_probe": null, "contract_tests_passed": null},
  "source": {"uri": "TO_BE_VERIFIED", "license": "review-required"},
  "known_failures": []
}
```

Het register moet ook **negatieve kennis** bevatten: onder welke versies, taken of omstandigheden werkt dit instrument juist niet? Het model moet een andere tool kunnen kiezen voordat het dezelfde fout herhaalt.

## 5. Voorgestelde minimale services

| Tool/Service | Doel | Veiligheidsgrens |
|---|---|---|
| `workbench_search(capability, context)` | Toolkandidaten vinden | Alleen metadata |
| `workbench_inspect(tool_id)` | I/O-schema, vereisten en beperkingen lezen | Read-only |
| `workbench_probe(tool_id, fixture)` | Of tool bereikbaar en passend is controleren | Beperkt, met rechtencheck |
| `workbench_recommend(task, obstacle)` | Keuze: gebruiken, anders inzetten, combineren, kandidaat maken of stoppen | Alleen advies |
| `workbench_propose_tool(spec, tests)` | Korte adapter/script als kandidaat voorstellen | Apart geïsoleerd en te reviewen |
| `workbench_evaluate(candidate, fixtures)` | Testresultaten en foutgevallen vastleggen | Uitvoering alleen volgens hostbeleid |

**Belangrijke grens:** een generieke `invoke_any_tool()` mag niet worden gebruikt als omweg om alle host-permissies te omzeilen. Gevoelige tools behouden eigen rechten en goedkeuringen; kandidaat-scripts en externe packages worden niet blind uitgevoerd.
