"""Local tool-discovery proxy experiment, not an LLM or Vibe performance test.

Handwritten capability catalog and tasks. Gold annotations are for evaluation,
never passed to candidate selection. Uses Python stdlib SQLite FTS5.
"""
from __future__ import annotations
import json, re, sqlite3, time, statistics
from pathlib import Path

TOOLS = [
 ('repo_symbols', 'locate find symbols functions classes definitions python source code repository', None, True),
 ('repo_references', 'find call sites references and callers for python functions repository', None, True),
 ('python_tests', 'execute run python unit tests pytest regression tests', None, True),
 ('python_types', 'check static python typing with mypy type annotations', None, True),
 ('python_lint', 'lint and format python source code ruff diagnostics', None, True),
 ('json_schema', 'validate JSON payload and JSON schema structured documents', None, True),
 ('xml_xsd', 'validate XML files against XSD schemas', None, True),
 ('csv_transform', 'parse convert CSV tabular text into JSON records', None, True),
 ('sqlite_plan', 'inspect SQLite query plan explain analyze SQL SQLite performance', 'sqlite', True),
 ('postgres_plan', 'inspect PostgreSQL query plan explain analyze SQL Postgres performance', 'postgres', True),
 ('api_contract', 'validate OpenAPI endpoint schema API contract requests response', None, True),
 ('api_client', 'generate Python client bindings from OpenAPI specification', None, True),
 ('http_smoke', 'run HTTP endpoint smoke integration tests client requests status', None, True),
 ('dependency_versions', 'inspect dependency versions lockfiles migration changelog compatibility', None, True),
 ('pydantic_v1', 'validate Pydantic model parse_obj dict schema version 1 api', 'pydantic1', True),
 ('pydantic_v2', 'validate Pydantic model model_validate model_dump version 2 api', 'pydantic2', True),
 ('pdf_text', 'extract searchable text from PDF document pages', None, True),
 ('container_build', 'build Docker container image from Dockerfile', None, False),
 ('container_lint', 'validate lint Dockerfile container definition syntax', None, True),
 ('secret_scan', 'scan repository for leaked credentials secrets and tokens', None, True),
 ('git_diff', 'inspect compare Git revisions diff changed files', None, True),
 ('sql_migrations', 'check SQL schema migrations and rollback database change', None, True),
 ('markdown_links', 'check Markdown documentation broken links', None, True),
 ('docs_search', 'search external library API documentation version manuals', None, True),
]
# id, natural-language task, environment scope, required tool IDs (evaluator only)
TASKS = [
 ('t01','Find the Python function definition called parse_event','any',['repo_symbols']),
 ('t02','Show all references and callers of the invoice routine','any',['repo_references']),
 ('t03','Run Python unit regression tests for the patch','any',['python_tests']),
 ('t04','Detect incorrect type annotations in Python modules','any',['python_types']),
 ('t05','Check a JSON object against its schema','any',['json_schema']),
 ('t06','Validate a batch of XML documents against XSD','any',['xml_xsd']),
 ('t07','Export CSV rows into a JSON collection','any',['csv_transform']),
 ('t08','Diagnose a slow SQLite query and inspect its execution plan','sqlite',['sqlite_plan']),
 ('t09','Diagnose an inefficient Postgres SQL query plan','postgres',['postgres_plan']),
 ('t10','Inspect the required API usage in Pydantic version 1','pydantic1',['pydantic_v1']),
 ('t11','Check Pydantic version 2 model validation and serialization','pydantic2',['pydantic_v2']),
 ('t12','Extract text content from a PDF attachment','any',['pdf_text']),
 ('t13','Check a Dockerfile for syntax and style violations','any',['container_lint']),
 ('t14','Scan a Git repository for accidental API tokens','any',['secret_scan']),
 ('t15','Review the Git diff from the preceding revision','any',['git_diff']),
 ('t16','Find Python function symbols and identify its callers','any',['repo_symbols','repo_references']),
 ('t17','Run Python unit tests and check static types','any',['python_tests','python_types']),
 ('t18','Validate OpenAPI endpoint contracts and run HTTP smoke tests','any',['api_contract','http_smoke']),
 ('t19','Inspect SQLite query plan and check schema migration safety','sqlite',['sqlite_plan','sql_migrations']),
 ('t20','Compare dependency versions and search API documentation for migration changes','any',['dependency_versions','docs_search']),
 ('t21','Generate OpenAPI Python client and validate resulting JSON schema','any',['api_client','json_schema']),
 ('t22','Inspect Pydantic version 2 validation and run Python unit tests','pydantic2',['pydantic_v2','python_tests']),
 ('t23','Find Python callers and inspect Git code differences','any',['repo_references','git_diff']),
 ('t24','Check Dockerfile syntax and scan secrets and validate HTTP endpoint','any',['container_lint','secret_scan','http_smoke']),
 ('t25','Explain what a relational database is without running software','any',[]),
 ('t26','Summarize the existing design discussion without executing code','any',[]),
 ('t27','Describe principles of accessible UI design, no code changes','any',[]),
 ('t28','Think through an alternative research hypothesis without tools','any',[]),
]
STOP={'a','an','the','to','of','for','in','on','and','or','with','from','against',
      'into','its','all','called','show','check','find','run','inspect','review',
      'detect','compare','version','required','resulting','existing','without',
      'no','what','is','code','documents','project','changes','batch'}

def tokens(s):
    return [w for w in re.findall(r'[a-z0-9_]+', s.lower()) if w not in STOP][:16]

def index():
    con=sqlite3.connect(':memory:')
    con.execute('CREATE TABLE registry (id TEXT PRIMARY KEY, env TEXT, usable INTEGER)')
    con.execute('CREATE VIRTUAL TABLE registry_fts USING fts5(id UNINDEXED, text)')
    for name,description,env,usable in TOOLS:
        con.execute('INSERT INTO registry VALUES(?,?,?)',(name,env,int(usable)))
        con.execute('INSERT INTO registry_fts VALUES(?,?)',
                    (name,name.replace('_',' ')+' '+description))
    return con

def retrieve(con,query,scope,k=3,filter_scope=False):
    words=tokens(query)
    if not words:return []
    match=' OR '.join('"'+w+'"' for w in words)
    rows=con.execute(
        'SELECT f.id, r.env, r.usable, bm25(registry_fts) AS score '
        'FROM registry_fts AS f JOIN registry AS r ON r.id=f.id '
        'WHERE registry_fts MATCH ? ORDER BY score LIMIT 50',(match,)).fetchall()
    ranked=[]
    for name,env,usable,score in rows:
        if filter_scope and env and scope != env:
            continue
        if filter_scope and not usable:
            continue
        ranked.append(name)
        if len(ranked)>=k:break
    return ranked

def choose(con,task,policy,k=3):
    tid,query,scope,gold=task
    if policy=='static':return ['repo_symbols','python_tests','json_schema'][:k]
    if policy=='bm25':return retrieve(con,query,scope,k,False)
    if policy=='filtered':return retrieve(con,query,scope,k,True)
    if policy=='plan':
        if re.search(r'\b(explain|summarize|describe|think through)\b',query.lower()) and not re.search(
                r'\b(run|validate|check|find|inspect|scan|generate)\b',query.lower()):
            return []
        clauses=re.split(r'\s+and\s+|\s+then\s+',query,flags=re.I)
        if len(clauses)<=1:return retrieve(con,query,scope,k,True)
        picks=[]
        for clause in clauses:
            for tool in retrieve(con,clause,scope,1,True):
                if tool not in picks and len(picks)<k:picks.append(tool)
        for tool in retrieve(con,query,scope,k,True):
            if tool not in picks and len(picks)<k:picks.append(tool)
        return picks
    raise ValueError(policy)

def evaluate(k=3):
    con=index()
    variants={}
    lookup={row[0]:row for row in TOOLS}
    for policy in ('static','bm25','filtered','plan'):
        records=[]
        start=time.perf_counter_ns()
        for task in TASKS:
            tid,query,scope,gold=task
            picked=choose(con,task,policy,k)
            bad=[t for t in picked if (lookup[t][2] not in (None,scope)) or not lookup[t][3]]
            complete=all(g in picked for g in gold) if gold else not picked
            valid=complete and not bad
            records.append({'id':tid,'scope':scope,'required':gold,
                'picked':picked,'complete':complete,'usable':valid,'wrong_or_unusable':bad})
        elapsed_ms=(time.perf_counter_ns()-start)/1e6
        variants[policy]={
            'n':len(TASKS),
            'complete_n':sum(t['complete'] for t in records),
            'usable_n':sum(t['usable'] for t in records),
            'no_tool_correct_n':sum(not t['picked'] for t in records if not t['required']),
            'no_tool_total_n':sum(not t['required'] for t in records),
            'bad_tool_selections_n':sum(len(t['wrong_or_unusable']) for t in records),
            'avg_selected_tools':round(statistics.mean(len(t['picked']) for t in records),2),
            'elapsed_ms_total':round(elapsed_ms,3),
            'observations':records
        }
    con.close()
    return {'design':'handwritten synthetic capability catalog, gold annotations evaluator only',
            'tools':len(TOOLS),'tasks':len(TASKS),'top_k':k,'variants':variants}

if __name__=='__main__':
    result=evaluate()
    print(json.dumps({k:{field:value for field,value in v.items() if field!='observations'}
          for k,v in result['variants'].items()},indent=2))
    (Path(__file__).parent/'workbench_pilot_results.json').write_text(
        json.dumps(result,indent=2)+'\n',encoding='utf-8')
