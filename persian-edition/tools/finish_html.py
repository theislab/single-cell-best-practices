"""Supply local Persian assets and language metadata after the MyST HTML build."""
import json
from pathlib import Path
import re
import shutil
from audit import EDITION


def main():
    root=EDITION/'_build/preview-source/_build/html'
    static=EDITION/'jupyter-book/_static'
    shutil.copy(static/'persian.css',root/'persian.css')
    shutil.copytree(static/'fonts',root/'fonts',dirs_exist_ok=True)
    pages=list(root.rglob('*.html'))
    for page in pages:
        text=page.read_text(encoding='utf-8')
        text=re.sub(r'<html\b[^>]*>',lambda m: re.sub(r'\s(?:lang|dir)="[^"]*"','',m[0])[:-1]+' lang="fa" dir="rtl">',text,count=1)
        if 'href="/persian.css"' not in text:
            text=text.replace('</head>','<link rel="stylesheet" href="/persian.css"/></head>',1)
        page.write_text(text,encoding='utf-8')
    report={'html_pages':len(pages),'font_files':[p.name for p in (root/'fonts').glob('*.ttf')],
            'preview_only':True,'scientific_notebooks_executed':False}
    (EDITION/'qa/HTML_BUILD.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(report,ensure_ascii=False))


if __name__=='__main__':main()
