#!/usr/bin/env python3
"""
Convert HTML anchor tags to MyST labels in .md and .ipynb files.

Converts:
  <a id="some-label"></a>
  <a id = some-label></a>
  <a id='some-label'></a>

To:
  (some-label)=
"""

import re
import json
import sys
from pathlib import Path

# Match <a id="label"></a> in various formats (quotes optional, spaces around =)
ANCHOR_PATTERN = re.compile(
    r'<a\s+id\s*=\s*["\']?\s*([^"\'>\s]+)\s*["\']?\s*>\s*</a>'
)

def fix_text(text):
    def replace(match):
        label = match.group(1).strip()
        return f'({label})='
    new_text, count = ANCHOR_PATTERN.subn(replace, text)
    return new_text, count


def fix_md_file(path):
    text = path.read_text()
    new_text, count = fix_text(text)
    if count:
        path.write_text(new_text)
        print(f'✅ Fixed {count} anchor(s) in {path}')
    return count


def fix_ipynb_file(path):
    nb = json.loads(path.read_text())
    total = 0
    for cell in nb['cells']:
        if cell['cell_type'] in ('markdown', 'raw'):
            src = ''.join(cell['source'])
            new_src, count = fix_text(src)
            if count:
                cell['source'] = [line + '\n' for line in new_src.splitlines()]
                if cell['source']:
                    cell['source'][-1] = cell['source'][-1].rstrip('\n')
                total += count
    if total:
        path.write_text(json.dumps(nb, indent=1, ensure_ascii=False) + '\n')
        print(f'✅ Fixed {total} anchor(s) in {path}')
    return total


def main(root='.'):
    root = Path(root)
    total = 0

    for path in sorted(root.rglob('*.md')):
        if '_build' in path.parts or path.name.startswith('.'):
            continue
        total += fix_md_file(path)

    for path in sorted(root.rglob('*.ipynb')):
        if '_build' in path.parts or path.name.startswith('.'):
            continue
        total += fix_ipynb_file(path)

    print(f'\n🎉 Total anchors fixed: {total}')


if __name__ == '__main__':
    root = sys.argv[1] if len(sys.argv) > 1 else '.'
    main(root)