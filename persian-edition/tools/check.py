"""Structural and preservation checks. Completeness is a separate release gate."""
import argparse
import ast
from collections import Counter
import copy
import csv
import json
from pathlib import Path
import re
import sys

import nbformat

from audit import EDITION, ROOT, BASE, digest, inventory, source
from apply_notebook import UI, load_map, replace_strings
import html


def text(cell):
    return ''.join(cell['source'])


def invariants(value):
    citations = Counter()
    for group in re.findall(r'\{cite(?::[a-z]+)?\}`([^`]+)`', value):
        citations.update(key.strip() for key in group.split(','))
    return {
        'citations': citations,
        'urls': Counter(u.rstrip('.,،;؛') for u in re.findall(r'https?://[^\s<>"\)]+', value)),
        'labels': Counter(re.findall(r'^\(([^\n]+)\)=\s*$', value, re.M)),
        'figure_ids': Counter(re.findall(r'^:name:\s*(.+)$', value, re.M)),
        'images': Counter(re.findall(r'\{(?:figure|image)\}\s+([^\n]+)', value)),
        'code_blocks': Counter(re.findall(r'```(?:python|bash|sh|yaml|r)\n(.*?)```', value, re.S)),
        'math_blocks': Counter(re.findall(r'\$\$(.*?)\$\$', value, re.S)),
    }


def mcq_answers(code):
    code = '\n'.join(line for line in code.splitlines() if not line.startswith('%'))
    tree = ast.parse(code)
    result = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id=='multiple_choice_question':
            names=['question_id','question','options','correct_answer','explanations']
            kw = dict(zip(names,[ast.literal_eval(a) for a in node.args]))
            kw.update({k.arg: ast.literal_eval(k.value) for k in node.keywords})
            result.append((kw['question_id'], kw['options'].index(kw['correct_answer']),
                           len(kw['options']),len(kw['explanations'])))
    return result


def main(release=False):
    rows,_,toc = inventory()
    state = json.loads((EDITION/'translation_state.json').read_text())
    failures, warnings, counts = [], [], Counter()
    inherited_schema_issues = []
    def check(condition, message):
        if not condition:
            failures.append(message)
    for row in rows:
        path = row['original_path']
        original = source(path)
        check((ROOT/path).read_bytes()==original, 'English source changed: '+path)
        target = EDITION/Path(row['translated_path']).relative_to('persian-edition')
        check(target.exists(), 'Missing mapped file: '+str(target))
        if not target.exists():
            continue
        if row['role'] in ('asset_preserve','bibliography_preserve','license_preserve'):
            check(target.read_bytes()==original, 'Protected content changed: '+path)
            counts[row['role']]+=1
        record=state.get(path)
        if record:
            check(record['source_sha256']==digest(original), 'Source drift: '+path)
            check(record['target_sha256']==digest(target.read_bytes()),'Translation changed without review record: '+path)
            counts['state_records']+=1
            if record['translation_status']=='translated_draft':counts['translated_draft_files']+=1
        if row['file_type']=='.ipynb':
            en, fa = json.loads(original), json.loads(target.read_bytes())
            counts['valid_json_notebooks']+=1
            try:
                nbformat.validate(copy.deepcopy(fa))
                counts['valid_notebooks']+=1
            except Exception as error:
                try:
                    nbformat.validate(copy.deepcopy(en))
                except Exception as baseline:
                    if getattr(baseline,'message',str(baseline))==getattr(error,'message',str(error)):
                        inherited_schema_issues.append({'path':path,'error':getattr(error,'message',str(error))})
                    else:
                        failures.append('New schema error: '+path+': '+str(error))
                else:
                    failures.append('Notebook validation regression: '+path+': '+str(error))
            check({k:v for k,v in en.items() if k!='cells'}=={k:v for k,v in fa.items() if k!='cells'}, 'Notebook metadata changed: '+path)
            check(len(en['cells'])==len(fa['cells']), 'Cell count changed: '+path)
            module=load_map(EDITION/record['translation_map']) if record and record.get('translation_map') else None
            for i,(a,b) in enumerate(zip(en['cells'],fa['cells'])):
                check(a['cell_type']==b['cell_type'],f'Cell type changed: {path}:{i}')
                check({k:v for k,v in a.items() if k not in ('source','outputs')}=={k:v for k,v in b.items() if k not in ('source','outputs')}, f'Cell metadata/tags/order changed: {path}:{i}')
                if a['cell_type']=='code':
                    if module and i in module.QUIZ:
                        replacements=module.QUIZ[i]
                        check(text(b)==replace_strings(text(a),replacements), f'Unapproved code edit: {path}:{i}')
                        check(mcq_answers(text(a))==mcq_answers(text(b)), f'Quiz answer/index changed: {path}:{i}')
                        # The executable structure must match after reversing only registered UI strings.
                        reversed_code=replace_strings(text(b), {new:old for old,new in replacements.items()})
                        normalized=lambda s: ast.dump(ast.parse('\n'.join(l for l in s.splitlines() if not l.startswith('%'))))
                        check(normalized(text(a))==normalized(reversed_code), f'Quiz logic changed: {path}:{i}')
                        check(len(a.get('outputs',[]))==len(b.get('outputs',[])),f'Quiz outputs removed: {path}:{i}')
                        for old_output,new_output in zip(a.get('outputs',[]),b.get('outputs',[])):
                            restored=copy.deepcopy(new_output)
                            rendered=restored.get('data',{}).get('text/html')
                            if rendered is not None:
                                value=''.join(rendered)
                                for old,new in sorted(replacements.items(),key=lambda pair:-len(pair[1])):
                                    value=value.replace(html.escape(new),html.escape(old)).replace(new,old)
                                for old,new in UI.items():value=value.replace(new,old)
                                value=re.sub(r'>پرسش (\d+)</button>',r'>Q\1</button>',value)
                                restored['data']['text/html']=value.splitlines(keepends=True) if isinstance(rendered,list) else value
                            check(old_output==restored,f'Unapproved quiz output/data edit: {path}:{i}')
                        counts['localized_quiz_cells']+=1
                    else:
                        check(a==b,f'Analysis code/output changed: {path}:{i}')
                        counts['identical_code_and_output_cells']+=1
                elif record and i in record.get('translated_markdown_cells',[]):
                    check(text(a)!=text(b),f'Markdown unchanged but marked translated: {path}:{i}')
                    check(bool(re.search('[\u0600-\u06ff]',text(b))),f'No Persian in translated cell: {path}:{i}')
                    for kind,expected in invariants(text(a)).items():
                        check(expected==invariants(text(b))[kind],f'{kind} mismatch: {path}:{i}')
                    counts['translated_markdown_cells']+=1
        elif record and record['translation_status']!='localized_configuration':
            en=original.decode()
            fa=target.read_text()
            for kind,expected in invariants(en).items():
                # README contains additional translation status links, none of the original URLs are removed.
                actual=invariants(fa)[kind]
                check(not (expected-actual) if path=='README.md' else expected==actual, f'{kind} mismatch: {path}')
    # Full inventory coverage, including supporting notebooks and archived educational files.
    with (EDITION/'TRANSLATION_MANIFEST.csv').open(encoding='utf-8-sig') as f:
        manifest=list(csv.DictReader(f))
    check({r['original_path'] for r in manifest}=={r['original_path'] for r in rows},'Manifest does not cover source tree')
    keys=lambda s: re.findall(r'^([^\n]+)\n:',s,re.M)
    check(keys(source('jupyter-book/glossary.md').decode())==keys((EDITION/'jupyter-book/glossary.md').read_text()),'Glossary reference keys changed')
    counts['toc_translated_draft']=sum(p in state for p in toc)
    counts['toc_total']=len(toc)
    warnings.append('Scientific and Persian editorial review is not independently completed.')
    warnings.append('Embedded English figure labels, source code comments/docstrings and remaining supplementary text still require review/translation.')
    warnings.append('Dataset-backed scientific notebooks were not executed; the checks compare code and stored outputs.')
    preservation_ok=not failures
    incomplete=[r['original_path'] for r in manifest if r['translation_status'] not in ('preserve','translated_reviewed','localized_configuration')]
    figure_review_path=EDITION/'qa/FIGURE_TRANSLATION_REVIEW.csv'
    with figure_review_path.open(encoding='utf-8-sig') as f:
        figures=list(csv.DictReader(f))
    counts['figures_pending_review']=sum(r['review_status']=='pending' for r in figures)
    if release and incomplete:
        failures.append(f'Release blocked: {len(incomplete)} source files are pending or drafts; {len(toc)-counts["toc_translated_draft"]} TOC entries have no translated draft.')
    if release and counts['figures_pending_review']:
        failures.append(f'Release blocked: {counts["figures_pending_review"]} figure/source-artwork files need embedded-text review.')
    report={'source_commit':BASE,'counts':dict(counts),'preservation_checks_pass':preservation_ok,
        'all_notebook_schemas_valid':not inherited_schema_issues,
        'inherited_schema_issues':inherited_schema_issues,
        'release_ready':not incomplete and not failures and not inherited_schema_issues,'release_gate_requested':release,
        'failures':failures,'limitations':warnings,'incomplete_source_files':incomplete}
    name='RELEASE_GATE.json' if release else 'TECHNICAL_QC.json'
    (EDITION/'qa'/name).write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='incomplete_source_files'},ensure_ascii=False,indent=2))
    return 1 if failures else 0


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--release', action='store_true')
    args=parser.parse_args()
    sys.exit(main(args.release))
