#!/usr/bin/env python3
"""
Fix figure directives in .md and .ipynb files.

Converts:
  :::{figure} some-label
  <img src="path/to/image.png" alt="Alt text" class="bg-primary" width="800px">
  Caption text
  :::

To:
  :::{figure} path/to/image.png
  :name: some-label
  :alt: Alt text
  :class: bg-primary
  :width: 800px
  Caption text
  :::
"""

import re
import json
import sys
from pathlib import Path

# Regex to match the full figure block
# Label can contain spaces (e.g. "Quality control", "Doublet detection")
# but must not look like a file path (no . extension)
FIGURE_PATTERN = re.compile(
    r'(:{3,4})\{figure\} (?P<label>[^\n]+)\n'
    r'\n?'
    r'<img(?P<attrs>[^>]+)>\n'
    r'(?P<caption>.*?)'
    r'\1',
    re.DOTALL
)



IMG_ATTR_PATTERN = re.compile(r'(\w+)=["\']([^"\']*)["\']')


def parse_img_attrs(attrs_str):
    return dict(IMG_ATTR_PATTERN.findall(attrs_str))


def fix_figure_block(match):
    fence = match.group(1)
    label = match.group('label').strip()
    attrs = parse_img_attrs(match.group('attrs'))
    caption = match.group('caption').strip()

    src = attrs.get('src', '')
    alt = attrs.get('alt', '')
    cls = attrs.get('class', '')
    width = attrs.get('width', '')

    lines = [f'{fence}{{figure}} {src}']
    if label:
        lines.append(f':name: {label}')
    if alt:
        lines.append(f':alt: {alt}')
    if cls:
        lines.append(f':class: {cls}')
    if width:
        lines.append(f':width: {width}')
    if caption:
        lines.append('')
        lines.append(caption)
    lines.append(fence)

    return '\n'.join(lines)


def fix_text(text):
    new_text, count = FIGURE_PATTERN.subn(fix_figure_block, text)
    return new_text, count


def fix_md_file(path):
    text = path.read_text()
    new_text, count = fix_text(text)
    if count:
        path.write_text(new_text)
        print(f'✅ Fixed {count} figure(s) in {path}')
    return count


def fix_ipynb_file(path):
    nb = json.loads(path.read_text())
    total = 0
    for cell in nb['cells']:
        if cell['cell_type'] in ('markdown', 'raw'):
            src = ''.join(cell['source'])
            new_src, count = fix_text(src)
            if count:
                # Preserve the original list structure
                cell['source'] = [line + '\n' for line in new_src.splitlines()]
                # Fix last line (no trailing newline)
                if cell['source']:
                    cell['source'][-1] = cell['source'][-1].rstrip('\n')
                total += count
    if total:
        path.write_text(json.dumps(nb, indent=1, ensure_ascii=False) + '\n')
        print(f'✅ Fixed {total} figure(s) in {path}')
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

    print(f'\n🎉 Total figures fixed: {total}')


if __name__ == '__main__':
    root = sys.argv[1] if len(sys.argv) > 1 else '.'
    main(root)