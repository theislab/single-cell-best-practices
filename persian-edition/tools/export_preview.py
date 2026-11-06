"""Export actual translated chapters, explicitly labelled as an incomplete draft.

MyST resolves citations/figures first. Quiz display strings are exported as static
questions and answers, since interactive HTML output is not printable in Word.
Never use this script to bypass the final edition's completeness gate.
"""
import ast
import html
import json
from pathlib import Path
import re
import subprocess

from bs4 import BeautifulSoup
from docx import Document
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt

from audit import EDITION


def quiz_html(code):
    tree=ast.parse('\n'.join(l for l in code.splitlines() if not l.startswith('%')))
    chunks=[]
    for call in ast.walk(tree):
        if not isinstance(call,ast.Call) or not isinstance(call.func,ast.Name):continue
        if call.func.id=='flip_card':
            args=[ast.literal_eval(a) for a in call.args]
            chunks.append('<div class="question"><p><strong>'+html.escape(args[1])+'</strong></p><p>پاسخ: '+html.escape(args[2])+'</p></div>')
        elif call.func.id=='multiple_choice_question':
            names=['question_id','question','options','correct_answer','explanations']
            kw=dict(zip(names,[ast.literal_eval(a) for a in call.args]))
            kw.update({k.arg:ast.literal_eval(k.value) for k in call.keywords})
            chunks.append('<div class="question"><p><strong>'+html.escape(kw['question'])+'</strong></p><ol>')
            chunks.extend('<li>'+html.escape(o)+'</li>' for o in kw['options'])
            chunks.append('</ol><p><strong>پاسخ درست: </strong>'+html.escape(kw['correct_answer'])+'</p>')
            chunks.extend('<p>'+html.escape(k)+': '+html.escape(v)+'</p>' for k,v in kw['explanations'].items())
            chunks.append('</div>')
    return ''.join(chunks)


def property_xml(parent,tag,value=None):
    child=parent.find(qn('w:'+tag))
    if child is None:
        child=OxmlElement('w:'+tag); parent.append(child)
    if value is not None:child.set(qn('w:val'),value)
    return child


def format_word(path):
    doc=Document(path)
    for style in doc.styles:
        if style.type in (1,2):
            style.font.name='Noto Naskh Arabic'
            rpr=style.element.get_or_add_rPr()
            fonts=property_xml(rpr,'rFonts')
            for key in list(fonts.attrib):
                if key.endswith('Theme'):
                    del fonts.attrib[key]
            for key in ['ascii','hAnsi','cs','eastAsia']:fonts.set(qn('w:'+key),'Noto Naskh Arabic')
    doc.styles['Normal'].font.size=Pt(12)
    doc.styles['Normal'].paragraph_format.space_after=Pt(6)
    doc.styles['Normal'].paragraph_format.line_spacing=1.35
    def paragraphs():
        yield from doc.paragraphs
        for table in doc.tables:
            for row in table.rows:
                for cell in row.cells:yield from cell.paragraphs
    for p in paragraphs():
        code=p.style.name in ('Source Code','SourceCode','Verbatim Char')
        persian=bool(re.search('[\u0600-\u06ff]',p.text)) and not code
        property_xml(p._p.get_or_add_pPr(),'bidi','1' if persian else '0')
        property_xml(p._p.get_or_add_pPr(),'jc','start')
        if p.style.name.startswith('Heading'):
            p.paragraph_format.keep_with_next=True
            if p.style.name=='Heading 1':
                p.paragraph_format.page_break_before=True
        for run in p.runs:
            rpr=run._r.get_or_add_rPr()
            property_xml(rpr,'lang','fa-IR' if persian else 'en-US')
            if code:
                run.font.name='DejaVu Sans Mono'; run.font.size=Pt(8)
                fonts=property_xml(rpr,'rFonts')
                for key in ('ascii','hAnsi','cs'):fonts.set(qn('w:'+key),'DejaVu Sans Mono')
    for section in doc.sections:
        section.page_width=Cm(21);section.page_height=Cm(29.7)
        section.top_margin=Cm(2.2);section.bottom_margin=Cm(2.2)
        section.left_margin=Cm(2);section.right_margin=Cm(2)
        header=section.header.paragraphs[0]
        header.text='بهترین روش‌ها در تحلیل تک‌سلولی — پیش‌نویس ناقص فارسی'
        property_xml(header._p.get_or_add_pPr(),'bidi','1')
        footer=section.footer.paragraphs[0]
        footer.alignment=1
        field=OxmlElement('w:fldSimple');field.set(qn('w:instr'),'PAGE');footer._p.append(field)
    settings=doc.settings.element
    property_xml(settings,'updateFields','true')
    doc.core_properties.title='بهترین روش‌ها در تحلیل تک‌سلولی — پیش‌نویس ناقص'
    doc.core_properties.subject='فقط بخش‌های ترجمه‌شده؛ نسخهٔ کامل کتاب نیست'
    doc.save(path)


def main():
    htmlroot=EDITION/'_build/preview-source/_build/html'
    state=json.loads((EDITION/'translation_state.json').read_text())
    order=['preamble','introduction/prior-art','introduction/fundamental-data-structures-and-frameworks',
           'introduction/advanced-data-structures-and-frameworks','introduction/scrna-seq','outlook','acknowledgements','glossary']
    chunks=['<h1>بهترین روش‌ها در تحلیل تک‌سلولی</h1><p><strong>پیش‌نویس ناقص فارسی؛ کتاب کامل نیست.</strong></p><p>این فایل فقط برای بررسی بخش‌های ترجمه‌شده و صفحه‌آرایی تولید شده است. بازبینی علمی و زبانی مستقل انجام نشده است.</p><p>Single-cell Best Practices — Copyright 2021 Theislab — Apache License 2.0</p><p>This Persian edition is an unofficial translation of Single-cell Best Practices. It is not an official publication of Theis Lab and has not been reviewed or endorsed by the original authors.</p><p>Source commit: 8247f51909752c74fb2cd6d7d88ad2f67d1c11cd</p>']
    stats=[]
    for slug in order:
        page=htmlroot/slug/'index.html'
        if not page.exists():continue
        soup=BeautifulSoup(page.read_text(),'html.parser')
        article=soup.find('article')
        if not article:raise ValueError('Missing rendered chapter: '+slug)
        for pre in article.select('pre'):
            if 'quiz_tabs()' in pre.get_text():
                container=pre.find_parent(class_='myst-jp-nb-block')
                if container:
                    container.replace_with(BeautifulSoup(quiz_html(pre.get_text()),'html.parser'))
        for element in article.select('script,style,svg,button,.myst-fm-block-header,.myst-footer-links,.myst-primary-sidebar'):
            element.decompose()
        for anchor in article.select('a'):
            if anchor.get_text().strip()=='¶':anchor.decompose()
        for details in article.select('details'):details['open']='open'
        for el in article.select('[id]'):
            el['id']=slug.replace('/','-')+'-'+el['id']
        for a in article.select('a[href]'):
            href=a['href']
            if href.startswith('#'):a['href']='#'+slug.replace('/','-')+'-'+href[1:]
            elif href.startswith('/'):a['href']='https://sc-best-practices.org'+href
        for img in article.select('img[src]'):
            if img['src'].startswith('/'):
                local=htmlroot/img['src'].lstrip('/')
                if not local.exists():raise FileNotFoundError(local)
                img['src']=str(local)
        for pre in article.select('pre'):pre['dir']='ltr'
        stats.append({'chapter':slug,'images':len(article.select('img')),'characters':len(article.get_text())})
        chunks.append('<section class="chapter">'+str(article)+'</section>')
    if len(stats)!=8:raise ValueError('Expected all eight drafted TOC files in this preview')
    output=EDITION/'output/preview';output.mkdir(parents=True,exist_ok=True)
    combined=EDITION/'_build/preview-print.html'
    combined.write_text('<!doctype html><html lang="fa" dir="rtl"><head><meta charset="utf-8"><title>پیش‌نویس ناقص فارسی</title></head><body>'+''.join(chunks)+'</body></html>')
    docx=output/'Single_Cell_Best_Practices_FA_PREVIEW.docx'
    subprocess.run(['pandoc',str(combined),'-f','html','-t','docx','--toc','--toc-depth=2','-M','toc-title=فهرست مطالب','-o',str(docx)],check=True)
    format_word(docx)
    (EDITION/'qa/DOCUMENT_PREVIEW.json').write_text(json.dumps({'preview_only':True,'chapters':stats,'docx':str(docx.relative_to(EDITION))},ensure_ascii=False,indent=2)+'\n')
    print(docx)


if __name__=='__main__':main()
