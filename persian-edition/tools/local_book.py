"""Portable setup, build, diagnostics and loopback-only reading of the MyST book."""
import argparse
import functools
import http.server
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import threading
import venv
import webbrowser

EDITION = Path(__file__).resolve().parents[1]
LOCAL = EDITION / '.local'
PYTHON = LOCAL / 'venv' / ('Scripts/python.exe' if os.name == 'nt' else 'bin/python')
SITE = EDITION / '_build/preview-source/_build/html'
THEME_COMMIT = '23f2df5493e23dfb1d9433c8aa64c87beb4232a3'


def run(args, cwd=EDITION):
    print('Running:', ' '.join(map(str,args)), flush=True)
    subprocess.run(list(map(str,args)), cwd=cwd, check=True)


def setup():
    if sys.version_info < (3,11):
        raise RuntimeError('Python 3.11 or newer is required.')
    for name in ('git','node','npm'):
        if not shutil.which(name):
            raise RuntimeError(f'{name} is missing. Install Git for Windows and Node.js LTS, then reopen this launcher.')
    major=int(subprocess.check_output(['node','--version'],text=True).strip().lstrip('v').split('.')[0])
    if major<18:raise RuntimeError('Node.js 18 or newer is required; use a supported LTS release.')
    if not PYTHON.exists():venv.EnvBuilder(with_pip=True).create(LOCAL/'venv')
    run([PYTHON,'-m','pip','install','-r',EDITION/'tools/requirements.txt'])
    theme=LOCAL/'book-theme'
    if not theme.exists():
        run(['git','clone','--no-checkout','https://github.com/myst-templates/book-theme.git',theme])
    run(['git','checkout','--detach',THEME_COMMIT],cwd=theme)
    run([shutil.which('npm'),'ci','--ignore-scripts','--no-audit','--no-fund'],cwd=theme)
    run([PYTHON,'-m','jupyter_book','--version'])


def build():
    python=Path(os.environ.get('FA_PYTHON',str(PYTHON)))
    if not python.exists():raise RuntimeError('Run SETUP_PERSIAN_BOOK.bat first.')
    env=dict(os.environ)
    theme=Path(env.get('FA_BOOK_THEME',str(LOCAL/'book-theme')))
    if not (theme/'template.yml').exists():raise RuntimeError('The official book theme is missing. Run setup first.')
    env['FA_BOOK_THEME']=str(theme.resolve())
    subprocess.run([str(python),str(EDITION/'tools/prepare_preview.py'),'--local'],env=env,check=True)
    subprocess.run([str(python),'-m','jupyter_book','build','--html','--ci'],cwd=EDITION/'_build/preview-source',env=env,check=True)
    run([python,EDITION/'tools/finish_html.py'])
    validate()


def validate():
    from html.parser import HTMLParser
    from urllib.parse import urlsplit,unquote
    missing=[];external=[]
    class Assets(HTMLParser):
        def handle_starttag(self,tag,attrs):
            a=dict(attrs)
            url=a.get('src') if tag in ('img','script') else a.get('href') if tag=='link' else None
            if not url or url.startswith(('data:','#')):return
            parsed=urlsplit(url)
            if parsed.scheme or parsed.netloc:external.append(url);return
            path=SITE/unquote(parsed.path).lstrip('/') if parsed.path.startswith('/') else self.page.parent/unquote(parsed.path)
            if not path.exists():missing.append({'page':str(self.page.relative_to(SITE)),'asset':url})
    if not (SITE/'index.html').exists():raise RuntimeError('No generated index.html was found.')
    pages=list(SITE.rglob('*.html'))
    for page in pages:
        parser=Assets();parser.page=page;parser.feed(page.read_text(encoding='utf-8'))
    report={'html_pages':len(pages),'missing_assets':missing,'external_asset_urls':sorted(set(external)),
            'offline_complete':False,'windows_tested':False,'scientific_notebooks_executed':False}
    (EDITION/'logs').mkdir(exist_ok=True)
    (EDITION/'logs/build-report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    if missing:raise RuntimeError('Missing local assets; see logs/build-report.json')
    print('MyST HTML build validated. External assets and offline coverage are listed in logs/build-report.json.')


def make_server(port):
    return http.server.ThreadingHTTPServer(('127.0.0.1',port),functools.partial(http.server.SimpleHTTPRequestHandler,directory=str(SITE)))


def start(port):
    if not (SITE/'index.html').exists():build()
    with make_server(port) as server:
        url=f'http://127.0.0.1:{server.server_port}/'
        print(f'Local book: {url}\nPress Ctrl+C to stop the server.',flush=True)
        threading.Timer(1,lambda:webbrowser.open(url)).start()
        try:server.serve_forever()
        except KeyboardInterrupt:print('\nServer stopped.')


def main():
    p=argparse.ArgumentParser();p.add_argument('action',choices=['setup','build','start','diagnose']);p.add_argument('--port',type=int,default=8765)
    args=p.parse_args()
    if args.action=='setup':setup()
    elif args.action=='build':build()
    elif args.action=='start':start(args.port)
    else:print(json.dumps({'platform':sys.platform,'python':sys.version,'venv_exists':PYTHON.exists(),'site_exists':(SITE/'index.html').exists(),'git':shutil.which('git'),'node':shutil.which('node'),'npm':shutil.which('npm')},indent=2))


if __name__=='__main__':
    try:main()
    except Exception as error:
        print(f'ERROR: {error}',file=sys.stderr)
        sys.exit(1)
