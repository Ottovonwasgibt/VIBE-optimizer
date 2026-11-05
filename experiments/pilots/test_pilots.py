"""Optional pilot regression checks: run from experiments/pilots directory.

Requires pydantic>=2 with pydantic.v1 compatibility API.
"""
import unittest
from workbench_pilot import TOOLS, TASKS, choose, evaluate, index
from pydantic_packs_pilot import evaluate as evaluate_pydantic

class PilotChecks(unittest.TestCase):
    def test_catalog_and_gold_ids(self):
        ids=[tool[0] for tool in TOOLS]
        self.assertEqual(len(ids),len(set(ids)))
        self.assertTrue(all(set(task[3]).issubset(ids) for task in TASKS))
        self.assertEqual(len(TASKS),28)

    def test_gold_labels_do_not_enter_selection(self):
        con=index()
        task=TASKS[15]
        alternative=(task[0],task[1],task[2],['bogus_gold'])
        self.assertEqual(choose(con,task,'plan'), choose(con,alternative,'plan'))
        con.close()

    def test_filtered_selection_avoids_incompatible_tools(self):
        results=evaluate()
        raw=results['variants']['bm25']
        filtered=results['variants']['filtered']
        planned=results['variants']['plan']
        self.assertEqual(raw['usable_n'],18)
        self.assertEqual(filtered['usable_n'],25)
        self.assertEqual(planned['usable_n'],26)
        self.assertGreater(raw['bad_tool_selections_n'],filtered['bad_tool_selections_n'])

    def test_pydantic_contract_asymmetry(self):
        results=evaluate_pydantic()['aggregates']
        self.assertEqual(results['v1__legacy']['passed'],7)
        self.assertEqual(results['v1__modern']['passed'],0)
        self.assertEqual(results['v2__legacy']['passed'],7)
        self.assertEqual(results['v2__modern']['passed'],7)
        self.assertGreater(results['v2__legacy']['deprecation_warnings'],0)
        self.assertEqual(results['v2__modern']['deprecation_warnings'],0)

if __name__=='__main__':
    unittest.main()
