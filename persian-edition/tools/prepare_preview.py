"""Build a labelled preview containing only files with a translated draft."""
import json
from pathlib import Path
import shutil
import yaml
from audit import EDITION, source, digest, BASE

LABELS={
'Single-cell best practices':'بهترین روش‌ها در تحلیل تک‌سلولی',
'Introduction':'مقدمه', 'RNA':'RNA', 'Data basics':'مبانی داده',
'Preprocessing and visualization':'پیش‌پردازش و مصورسازی',
'Identifying cellular structure':'شناسایی ساختار سلولی',
'Inferring trajectories':'استنباط مسیرها','Dealing with conditions':'بررسی شرایط',
'Modeling mechanisms':'مدل‌سازی سازوکارها','Deconvolution':'واسازی ترکیب',
'Chromatin Accessibility':'دسترس‌پذیری کروماتین','Spatial omics':'اُمیکس مکانی',
'Surface protein':'پروتئین‌های سطحی',
'Adaptive immune receptor repertoire':'مجموعهٔ گیرنده‌های ایمنی تطبیقی',
'Multimodal integration':'ادغام داده‌های چندوجهی',
'Ecosystem and performance':'زیست‌بوم و کارایی','Appendix':'پیوست',
'Changelog':'تاریخچهٔ تغییرات'}

def localize(nodes):
 for node in nodes:
  if 'title' in node: node['title']=LABELS.get(node['title'],node['title'])
  localize(node.get('children',[]))

def prune(nodes,state):
 result=[]
 for node in nodes:
  node=dict(node)
  if 'file' in node and 'jupyter-book/'+node['file'] not in state: continue
  if 'children' in node:
   node['children']=prune(node['children'],state)
   if not node['children']: continue
  result.append(node)
 return result

def main():
 state=json.loads((EDITION/'translation_state.json').read_text())
 cfg=yaml.safe_load(source('jupyter-book/myst.yml'))
 cfg['project']['title']=LABELS[cfg['project']['title']]
 cfg['project']['github']='Omidbiochem/single-cell-best-practices'
 # Keep upstream author names and bibliography metadata verbatim.
 cfg['project']['exports']=[]
 localize(cfg['project']['toc'])
 (EDITION/'jupyter-book/myst.yml').write_text(yaml.safe_dump(cfg,allow_unicode=True,sort_keys=False))
 dest=EDITION/'_build/preview-source'
 if dest.exists(): shutil.rmtree(dest)
 dest.mkdir(parents=True)
 for sub in ('_static','_templates'):
  shutil.copytree(EDITION/'jupyter-book'/sub,dest/sub)
 shutil.copy(EDITION/'jupyter-book/logo.png',dest/'logo.png')
 for p in (EDITION/'jupyter-book').rglob('*.bib'):
  q=dest/p.relative_to(EDITION/'jupyter-book'); q.parent.mkdir(parents=True,exist_ok=True); shutil.copy(p,q)
 for path,record in state.items():
  if path.startswith('jupyter-book/') and record['translation_status']=='translated_draft':
   src=EDITION/path; dst=dest/Path(path).relative_to('jupyter-book'); dst.parent.mkdir(parents=True,exist_ok=True); shutil.copy(src,dst)
 shutil.copytree(EDITION/'scripts',dest.parent/'scripts',dirs_exist_ok=True)
 cfg['project']['toc']=prune(cfg['project']['toc'],state)
 cfg['project']['toc'].insert(0,{'file':'index.md'})
 cfg['project']['references']={}
 cfg['project']['id']='sc-best-practices-persian-preview'
 if Path('/workspace/book-theme/template.yml').exists():
  cfg['site']['template']='/workspace/book-theme'
 (dest/'index.md').write_text('''# نسخهٔ آزمایشی ترجمهٔ فارسی

این خروجی فقط شامل بخش‌هایی است که پیش‌نویس ترجمهٔ فارسی دارند؛ **کتاب کامل نیست و برای انتشار نهایی آماده نیست**. فایل‌های انگلیسیِ در انتظار ترجمه در این پیش‌نمایش گنجانده نشده‌اند.

نسخهٔ مبنا: `8247f51909752c74fb2cd6d7d88ad2f67d1c11cd`.

این ترجمه غیررسمی است و نویسندگان اثر اصلی آن را بررسی یا تأیید نکرده‌اند. ارجاع‌های متنی به فصل‌های در انتظار ترجمه ممکن است در پیش‌نمایش حل نشوند. بازبینی علمی مستقل و بررسی نهایی تصاویر هنوز باقی است.
''')
 (dest/'myst.yml').write_text(yaml.safe_dump(cfg,allow_unicode=True,sort_keys=False))
 for path in ['jupyter-book/myst.yml','jupyter-book/_static/custom.css']:
  state[path]={'source_commit':BASE,'source_sha256':digest(source(path)),
   'target_sha256':digest((EDITION/path).read_bytes()),
   'translation_status':'localized_configuration','quality_control_status':'build_check_pending',
   'remaining_issues':'نسخهٔ آزمایشی و صفحه‌آرایی باید بررسی شود؛ خروجی نهایی منوط به تکمیل ترجمه است.'}
 (EDITION/'translation_state.json').write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n')
 print(dest)

if __name__=='__main__':main()
