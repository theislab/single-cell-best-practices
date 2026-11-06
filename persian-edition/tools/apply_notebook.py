"""Apply explicit translation maps without changing notebook structure or analysis."""
import ast
import html
import importlib.util
import io
import json
from pathlib import Path
import sys
import tokenize

from audit import BASE, EDITION, digest, source


def load_map(path):
    spec = importlib.util.spec_from_file_location('translation_map', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def replace_strings(code, mapping):
    lines = code.splitlines(keepends=True)
    offsets = [0]
    for line in lines:
        offsets.append(offsets[-1] + len(line))
    changes = []
    used = set()
    for token in tokenize.generate_tokens(io.StringIO(code).readline):
        if token.type != tokenize.STRING:
            continue
        value = ast.literal_eval(token.string)
        if value in mapping:
            used.add(value)
            start = offsets[token.start[0]-1] + token.start[1]
            end = offsets[token.end[0]-1] + token.end[1]
            changes.append((start, end, json.dumps(mapping[value], ensure_ascii=False)))
    if used != set(mapping):
        raise ValueError('Unmatched translation strings: ' + repr(set(mapping)-used))
    for start, end, replacement in reversed(changes):
        code = code[:start] + replacement + code[end:]
    return code


UI = {
    '✔ Correct Answer:': '✔ پاسخ درست:',
    '✅ Correct!': '✅ درست است!',
    '❌ Incorrect!': '❌ نادرست است!',
    '<strong>Q:</strong>': '<strong>پرسش:</strong>',
    '<strong>Answer:</strong>': '<strong>پاسخ:</strong>',
    'text-align: left;': 'text-align: right; direction: rtl;',
}


def main(path, module_path):
    module = load_map(module_path)
    nb = json.loads(source(path))
    expected = {i for i,c in enumerate(nb['cells']) if c['cell_type']=='markdown'}
    structural = {i for i in expected if ''.join(nb['cells'][i]['source']).strip().startswith('---')
                  and ''.join(nb['cells'][i]['source']).strip().endswith('---')}
    if set(module.MARKDOWN) | structural != expected:
        raise ValueError('Markdown map is incomplete: ' + repr(expected-set(module.MARKDOWN)-structural))
    state_path = EDITION / 'translation_state.json'
    state = json.loads(state_path.read_text()) if state_path.exists() else {}
    target = EDITION / path
    existing = state.get(path, {})
    if existing and existing.get('target_sha256') != digest(target.read_bytes()):
        raise ValueError('Existing edited translation must be preserved: ' + path)
    for i, text in module.MARKDOWN.items():
        nb['cells'][i]['source'] = text.splitlines(keepends=True)
    for i, replacements in module.QUIZ.items():
        cell = nb['cells'][i]
        cell['source'] = replace_strings(''.join(cell['source']), replacements).splitlines(keepends=True)
        for output in cell.get('outputs', []):
            value = output.get('data',{}).get('text/html')
            if value is None:
                continue
            rendered = ''.join(value)
            for old, new in sorted(replacements.items(), key=lambda pair: -len(pair[0])):
                rendered = rendered.replace(html.escape(old), html.escape(new)).replace(old, new)
            for old, new in UI.items():
                rendered = rendered.replace(old, new)
            import re
            rendered = re.sub(r'>Q(\d+)</button>', r'>پرسش \1</button>', rendered)
            cell_output = rendered.splitlines(keepends=True)
            output['data']['text/html'] = cell_output if isinstance(value, list) else rendered
    target.write_text(json.dumps(nb, ensure_ascii=False, indent=1)+'\n')
    state[path] = dict(source_commit=BASE, source_sha256=digest(source(path)),
        target_sha256=digest(target.read_bytes()), translation_status='translated_draft',
        quality_control_status='technical_review_pending',
        remaining_issues='بازبینی مستقل علمی و زبانی، توضیح کامل فارسی برای متن داخل تصاویر و بررسی بصری باقی است.',
        translated_markdown_cells=sorted(module.MARKDOWN),
        structural_markdown_cells=sorted(structural),
        approved_quiz_cells=sorted(module.QUIZ),
        translation_map=str(Path(module_path).resolve().relative_to(EDITION)))
    state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2)+'\n')
    print(f'Translated {len(module.MARKDOWN)} Markdown cells and {len(module.QUIZ)} quiz cells: {path}')


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
