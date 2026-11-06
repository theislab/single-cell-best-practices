"""Inventory the immutable English commit; never infer translation from copying."""
from pathlib import Path
import csv
import hashlib
import json
import re
import subprocess
import yaml

EDITION = Path(__file__).resolve().parents[1]
ROOT = EDITION.parent
BASE = '8247f51909752c74fb2cd6d7d88ad2f67d1c11cd'


def source(path):
    return subprocess.check_output(['git', '-C', str(ROOT), 'show', f'{BASE}:{path}'])


def digest(data):
    return hashlib.sha256(data).hexdigest()


def toc_files(nodes):
    for node in nodes:
        if 'file' in node:
            yield 'jupyter-book/' + node['file']
        yield from toc_files(node.get('children', []))


def inventory():
    paths = subprocess.check_output(
        ['git', '-C', str(ROOT), 'ls-tree', '-rz', '--name-only', BASE]
    ).decode().strip('\0').split('\0')
    toc = list(toc_files(yaml.safe_load(source('jupyter-book/myst.yml'))['project']['toc']))
    rows, cells = [], []
    for path in paths:
        data = source(path)
        ext = Path(path).suffix
        text = data.decode('utf-8', errors='replace')
        role = 'supporting_source'
        if path in toc:
            role = 'book_chapter'
        elif ext == '.ipynb':
            role = 'supplementary_notebook'
        elif ext == '.txt':
            role = 'key_takeaways'
        elif ext == '.bib':
            role = 'bibliography_preserve'
        elif ext in ('.png', '.jpg', '.jpeg', '.svg', '.gif', '.ico', '.key', '.pt'):
            role = 'asset_preserve'
        elif ext == '.bak':
            role = 'archived_source_review'
        elif 'LICENSE' in path:
            role = 'license_preserve'
        elif ext in ('.yml', '.yaml', '.toml') or Path(path).name == 'Makefile':
            role = 'configuration_preserve'
        sections = len([b for b in re.split(r'\n\s*\n', text) if b.strip()])
        nb = None
        title = next(iter(re.findall(r'^#\s+(.+)', text, re.M)), Path(path).stem)
        if ext == '.ipynb':
            nb = json.loads(data)
            sections = sum(c['cell_type'] == 'markdown' for c in nb['cells'])
            md = '\n'.join(''.join(c['source']) for c in nb['cells'] if c['cell_type'] == 'markdown')
            title = next(iter(re.findall(r'^#\s+(.+)', md, re.M)), title)
            for i, cell in enumerate(nb['cells']):
                content = ''.join(cell['source'])
                cells.append(dict(original_path=path, cell_index=i,
                    cell_type=cell['cell_type'], source_sha256=digest(content.encode()),
                    word_count=len(content.split()),
                    has_quiz=bool(re.search(r'flip_card\(|multiple_choice_question\(', content)),
                    has_comment_or_docstring=bool(re.search(r'#|"""|\'\'\'', content)),
                    output_count=len(cell.get('outputs', [])),
                    translation_status='pending' if cell['cell_type'] == 'markdown' else 'preserve_review_text'))
        target = path
        if path == 'README.md':
            target = 'README_FA.md'
        row = dict(original_path=path, file_type=ext or 'extensionless',
            chapter_or_section=title, text_section_count=sections if role not in ('asset_preserve','bibliography_preserve') else 0,
            translation_status='preserve' if role.endswith('_preserve') else 'pending',
            translated_path='persian-edition/' + target,
            quality_control_status='not_checked', remaining_issues='', role=role,
            source_sha256=digest(data), source_bytes=len(data),
            notebook_code_cells=sum(c['cell_type']=='code' for c in nb['cells']) if nb else 0)
        rows.append(row)
    return rows, cells, toc


def main():
    rows, cells, toc = inventory()
    state_path = EDITION / 'translation_state.json'
    state = json.loads(state_path.read_text()) if state_path.exists() else {}
    for row in rows:
        record = state.get(row['original_path'], {})
        if record:
            if record.get('source_sha256') != row['source_sha256']:
                raise ValueError('Source fingerprint mismatch: ' + row['original_path'])
            for key in ('translation_status','quality_control_status','remaining_issues'):
                if key in record:
                    row[key] = record[key]
        if row['translation_status'] == 'pending':
            row['remaining_issues'] = 'ترجمه و بازبینی باقی است؛ وجود نسخهٔ کپی‌شده به معنی ترجمه نیست.'
    with (EDITION / 'TRANSLATION_MANIFEST.csv').open('w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    for cell in cells:
        record = state.get(cell['original_path'], {})
        if cell['cell_type'] == 'markdown' and cell['cell_index'] in record.get('translated_markdown_cells', []):
            cell['translation_status'] = 'translated_draft'
        elif cell['cell_index'] in record.get('structural_markdown_cells', []):
            cell['translation_status'] = 'preserve_author_metadata'
    (EDITION / 'qa/CELL_MANIFEST.json').write_text(json.dumps(cells, ensure_ascii=False, indent=2)+'\n')
    summary = dict(source_commit=BASE, source_files=len(rows), toc_entries=len(toc),
        notebooks=sum(r['file_type']=='.ipynb' for r in rows),
        markdown_cells=sum(c['cell_type']=='markdown' for c in cells),
        code_cells=sum(c['cell_type']=='code' for c in cells),
        quiz_code_cells=sum(c['has_quiz'] for c in cells),
        toc=toc, files=rows)
    (EDITION / 'qa/SOURCE_INVENTORY.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in summary.items() if k not in ('toc','files')},indent=2))


if __name__ == '__main__':
    main()
