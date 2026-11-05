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

## 6. Toolgeschiktheid versus beschikbaarheid

Toets bij een kandidaat:

- Kloppen input, output en semantiek met de taak?
- Past de tool bij het OS, de taal, projectversie en huidige repositorytoestand?
- Is de tool werkelijk bereikbaar, geïnstalleerd, geautoriseerd en gezond?
- Geeft gebruik van de tool meer nieuwe informatie dan een goedkope alternatieve stap?
- Zijn er slechte eerdere ervaringen met hetzelfde instrument en deze omstandigheden?
- Zijn de resultaten onafhankelijk toetsbaar?

Maak geen gefingeerde confidence-percentages; registreer gemeten toolresultaten en onzekerheid.

## 7. Vibe- en MCP-integratie

**Publieke documentatie als ontwerpbasis (te controleren tegen de geïnstalleerde versie):**

- Vibe ondersteunt MCP-servers, beheer via `vibe mcp add` of `/mcp`, connectoren en per-tool permissies. Zie https://docs.mistral.ai/vibe/code/cli/mcp-servers en https://docs.mistral.ai/vibe/code/cli/connectors.
- Vibe-plugins kunnen skills, referentiekennis en MCP-servers bundelen; pluginwijzigingen kunnen `/reload-plugins` vereisen, afhankelijk van sessie en moment. Zie https://docs.mistral.ai/vibe/code/cli/plugins.
- MCP ondersteunt tool listing en tool calling en mechanismen om wijzigingen in de toolset kenbaar te maken. Zie https://modelcontextprotocol.io/specification/2026-07-28/server/tools.
- Een host beslist zelf of en wanneer nieuw ontdekte schema's in de modelcontext verschijnen. **Automatisch live tools bijplaatsen tijdens een lopende Vibe-stap is niet aangetoond.**

**Voorgestelde aanpak:** start met een klein, stabiel MCP-werkbankoppervlak. Dat oppervlak biedt zoeken en inspecteren binnen een groter extern toolregister. Nieuwe native servers/plugins blijven afzonderlijk beheerd; een gevonden tool krijgt niet automatisch uitvoeringsrechten.

## 8. Theorie en toetsbare hypothesen

**H-11 — Tool discoverability:** een taakafhankelijk doorzoekbare werkbank vergroot de kans dat het model het passende instrument vindt ten opzichte van een statische tool-lijst bij vergelijkbaar contextbudget.

**H-12 — Tool adequacy:** actief toetsen van versie, bereikbaarheid, input/output en geschiktheid reduceert herhaalde mislukte aanroepen en onnodige zelfontwikkelde tools.

**H-13 — Tool adaptation:** zorgvuldig geteste aanpassing of compositie van bestaande tools levert bij geselecteerde taken meer winst per kosteneenheid dan extra algemene modelredenering.

**H-14 — Tool synthesis transfer:** door de agent voorgestelde en onafhankelijk goedgekeurde kleine scripts zijn herbruikbaar op andere, ongeziene taken; het effect moet worden gecorrigeerd voor ontwikkelkosten en regressies.

### Experimentele varianten

1. Statische baseline (alleen standaard Vibe-tools).
2. Grotere statische toolset (controleren op contextoverbelasting).
3. Doorzoekbare, reeds goedgekeurde toolcatalogus.
4. Catalogus plus bereikbaarheid/geschiktheidscontrole.
5. Catalogus plus toolcompositie/adapterkandidaten.
6. Catalogus plus afzonderlijk geteste nieuwe toolkandidaten.
7. Zelfde model met hetzelfde totale budget, maar zonder nieuwe tools (extra redeneertijd/samples).

Primaire metric: **extern geverifieerde taakoplossing**. Secundair: correcte toolselectie, detectie ontbrekende capaciteit, tool contract errors, onnodige aanroepen, tokenkosten, latency, onveilige bevoegdheidsverzoeken en transfer naar ongeziene taken.

Test uitdrukkelijk gevallen waarin **geen tool nodig is**, of waarin een beschikbare tool juist ongeschikt blijkt.

## 9. Literatuur en bestaande referentiearchitecturen

- Mistral Vibe MCP: https://docs.mistral.ai/vibe/code/cli/mcp-servers
- Mistral Vibe Plugins: https://docs.mistral.ai/vibe/code/cli/plugins
- MCP Tool Protocol: https://modelcontextprotocol.io/specification/2026-07-28/server/tools
- Tool Search in Microsoft Foundry: https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/tools/tool-search
- Anthropic Advanced Tool Use: https://www.anthropic.com/research/advanced-tool-use
- Toolformer (2023): https://arxiv.org/abs/2302.04761
- Large Language Models as Tool Makers (2023): https://arxiv.org/abs/2305.17126
- Hi-RAG hierarchical tool selection (2026): https://doi.org/10.1111/exsy.70341

Bestaande tool-search- en tool-making-benaderingen zijn **prior art**. De mogelijk nieuwe bijdrage van VIBE-optimizer ligt in de combinatie van *tool-adequacy-diagnose*, contextuele beschikbaarheid, midden-in-de-taak acquisitie, veilige kandidaatontwikkeling en meting van daadwerkelijk gerealiseerde werkcapaciteit. Wetenschappelijke nieuwheid is **nog niet vastgesteld**.

## 10. Voorbereidende onderzoeksdeliverables

1. Een volledige census van tools in de daadwerkelijk geïnstalleerde Vibe-configuratie.
2. Capability-cards met machineleesbaar I/O-contract en beperkingen.
3. Drie realistische scenario's waarbij een nieuwe toolbehoefte pas tijdens het werk ontstaat.
4. Een toetsbaar beslisbeleid voor zoeken, aanpassen, ontwikkelen of niets doen.
5. Een onafhankelijk benchmarkprotocol met kosten- en veiligheidsgrenzen.
6. Een kleine demonstratie met alleen reeds goedgekeurde, read-only tools.

**Conclusie:** het doel is niet dat het model alle tools heeft, maar dat het **kan ontdekken welke vaardigheid ontbreekt en de juiste aanvulling kan organiseren**, zonder zijn veiligheid of betrouwbaarheid te verliezen.
