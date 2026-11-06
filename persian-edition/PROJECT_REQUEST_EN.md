# PROJECT: COMPLETE PERSIAN TRANSLATION OF SINGLE-CELL BEST PRACTICES

## Role and expertise

Act as a senior scientific translator, computational biologist, single-cell RNA-seq expert, Persian scientific editor, Jupyter Book developer, and professional document publishing engineer.

I want you to transform my GitHub repository into a complete, professionally translated Persian edition of the book:

**Single-cell Best Practices**

Original repository:
https://github.com/theislab/single-cell-best-practices

My personal fork:
https://github.com/Omidbiochem/single-cell-best-practices

This is a complete book translation project, not a summary, simplified tutorial, or selective translation.

## IMPORTANT LANGUAGE INSTRUCTIONS

Communicate with me in Persian (Farsi).

All educational and scientific content in the Persian edition must be translated into professional, fluent, academically accurate Persian.

Keep scientific terminology precise and consistent with established terminology in molecular biology, bioinformatics, genomics, and computational biology.

Where appropriate, introduce the Persian translation followed by the original English technical term in parentheses at its first occurrence.

For example:

- تحلیل تک‌سلولی (Single-cell analysis)
- توالی‌یابی RNA تک‌سلولی (Single-cell RNA sequencing)
- تغییرات بیان ژن (Differential gene expression)
- کاهش ابعاد (Dimensionality reduction)
- تصحیح اثر دسته‌ای (Batch effect correction)
- تحلیل غنی‌سازی مجموعه ژنی (Gene set enrichment analysis)
- ماتریس بیان ژن (Gene expression matrix)

Create a consistent scientific terminology glossary and use it throughout the entire book.

Do not translate technical terminology inconsistently between chapters.

# PART 1 — COMPLETE SOURCE REPOSITORY AUDIT

Before translating anything, inspect my entire fork.

Identify and inventory every relevant source file, including:

- All Jupyter notebooks (.ipynb).
- Markdown files (.md).
- Text files (.txt).
- Book configuration files.
- Table of contents.
- Glossary.
- Chapter summaries and key takeaways.
- Quizzes and flashcards.
- Figure captions.
- Tables.
- Explanatory text associated with code.
- Image descriptions and alternative text.
- Relevant documentation and README files.

Do not translate only the first few chapters.

Do not overlook supplementary educational material.

Create a complete translation inventory named:

`TRANSLATION_MANIFEST.csv`

It must include:

- Original file path.
- File type.
- Chapter or section name.
- Number of text sections or notebook Markdown cells.
- Translation status.
- Translated file path.
- Quality-control status.
- Remaining issues.

Also create:

`TRANSLATION_PROGRESS.md`

Use it to track completed chapters, pending chapters, quality checks, and the exact point where work should resume if interrupted.

# PART 2 — TRANSLATION RULES

Translate ALL educational content without summarizing or omitting information.

This includes:

1. Chapter titles.
2. Section headings.
3. Paragraphs.
4. Scientific explanations.
5. Step-by-step tutorials.
6. Tables and their contents.
7. Figure captions.
8. Explanatory notes.
9. Warnings and technical recommendations.
10. Key takeaways.
11. Quizzes and their answers.
12. Flashcards.
13. Glossary definitions.
14. Installation instructions.
15. README documentation.
16. Learning objectives.
17. Descriptions of algorithms and computational methods.
18. Interpretations of scientific results.

Maintain the original scientific meaning, technical detail, examples, and pedagogical structure.

Do not shorten long explanations.

Do not replace technical discussions with simplified summaries.

Do not invent additional scientific claims.

## Important: Preserve executable code

This book contains many Python examples and Jupyter notebooks.

The following must remain functional and must NOT be translated or altered:

- Python syntax.
- Function names.
- Variable names.
- Class names.
- Package names.
- API calls.
- Import statements.
- File paths used by code.
- Command-line commands.
- Mathematical expressions.
- Dataset identifiers.
- URLs.
- Database identifiers.
- Gene symbols.
- Scientific accession numbers.

Translate natural-language explanations, Markdown cells, educational comments, and docstrings where safe.

Translate user-facing strings, quiz questions, and explanatory labels only when doing so does not change the expected behavior of the code.

Never modify executable code merely to make it look Persian.

Preserve notebook cell types, ordering, metadata, tags, and computational logic.

Do not modify scientific data or numeric outputs.

## References and citations

Preserve:

- Original author names.
- Publication titles.
- Journal names.
- DOI identifiers.
- URLs.
- Citation keys.
- Bibliographic metadata.

Translate explanatory text around references, but do not fabricate or modify citation information.

# PART 3 — CREATE A SEPARATE PERSIAN EDITION

Do not overwrite the original English book.

Do not modify the upstream repository.

Create a separate working branch in my fork:

`persian-translation`

Create a separate directory:

`persian-edition/`

The proposed structure should be:

persian-edition/

    README_FA.md

    LICENSE

    TRANSLATION_CREDITS.md

    TRANSLATION_MANIFEST.csv

    TRANSLATION_PROGRESS.md

    glossary_fa.md

    jupyter-book/

        _config.yml

        _toc.yml

        introduction/

        preprocessing/

        quality_control/

        dimensionality_reduction/

        clustering/

        annotation/

        differential_expression/

        conditions/

        integration/

        visualization/

        other_original_sections/

        _static/

            images/

            fonts/

    output/

        Single_Cell_Best_Practices_FA.docx

        Single_Cell_Best_Practices_FA.pdf

Adapt this structure to the actual source repository. Do not assume that all listed chapter folders exist.

Preserve the original English edition in its original location.

# PART 4 — PROFESSIONAL PERSIAN TYPOGRAPHY AND RTL DESIGN

The Persian edition must have a professional book layout.

Requirements:

- Full right-to-left Persian text direction.
- Correct Persian character shaping.
- Correct punctuation and paragraph direction.
- Correct mixed Persian-English text rendering.
- Proper formatting of mathematical equations.
- English code blocks displayed left-to-right.
- URLs and technical identifiers displayed left-to-right.
- Consistent heading hierarchy.
- Professional chapter-opening pages.
- Readable tables.
- Correct figure placement and captions.
- Page numbering.
- Table of contents.
- Consistent margins and spacing.

Use a suitable Persian font such as Vazirmatn or Noto Naskh Arabic, subject to availability and licensing.

Do not allow Persian and English text to overlap or reverse incorrectly.

Maintain the visual identity and scientific structure of the original book while creating an elegant Persian publication.

# PART 5 — FIGURES, DIAGRAMS AND IMAGES

Preserve all original scientific figures, illustrations, diagrams, and plots.

Translate:

- Figure titles.
- Figure captions.
- Legends.
- Explanatory labels.
- Alternative text.

If a figure contains embedded English text, create a separate Persian-labelled version when technically feasible.

Do not alter scientific plots, axes, values, or data.

Keep the original image as well.

If embedded text cannot be translated reliably, retain the original image and provide a complete Persian explanation below it.

# PART 6 — CREATE THE WORD DOCUMENT

Generate a complete, professionally formatted Microsoft Word document:

`Single_Cell_Best_Practices_FA.docx`

Requirements:

- All chapters included.
- Fully editable text.
- Persian RTL formatting.
- Professional scientific typography.
- Automatic table of contents.
- Heading styles.
- Figure and table captions.
- Proper page breaks.
- Headers and footers.
- Page numbering.
- Hyperlinks.
- Correct scientific equations.
- Preserved code blocks with monospaced English formatting.
- Proper bibliography formatting.

The Word file must be a complete translated book, not a short report.

# PART 7 — CREATE THE PDF BOOK

Generate:

`Single_Cell_Best_Practices_FA.pdf`

The PDF must:

- Contain the entire translated book.
- Preserve the Word document's layout and scientific structure.
- Support Persian fonts correctly.
- Have correct RTL text rendering.
- Include a clickable table of contents where feasible.
- Preserve figures, tables, mathematical expressions, and code blocks.
- Be searchable and selectable.
- Avoid missing glyphs, broken characters, blank pages, and text overflow.

Embed appropriate fonts if licensing permits.

# PART 8 — QUALITY ASSURANCE

Translation completeness is critical.

Perform the following checks:

1. Compare the original source inventory against the translated inventory.
2. Confirm that every educational chapter has been translated.
3. Check for missing paragraphs and untranslated Markdown cells.
4. Check that scientific terminology is consistent.
5. Check citations and bibliography integrity.
6. Validate every translated Jupyter notebook as valid JSON.
7. Compare executable code cells against the original.
8. Confirm that Python code has not been accidentally translated or corrupted.
9. Check all image and file references.
10. Build the Persian Jupyter Book.
11. Validate the generated DOCX.
12. Validate the generated PDF.
13. Inspect Persian RTL rendering in both documents.
14. Verify that the final documents contain all chapters.

Create a final quality-control report.

Do not mark the project as complete until every source chapter has been accounted for.

# PART 9 — COPYRIGHT AND ATTRIBUTION

The original book is distributed under the Apache License 2.0.

Preserve the original LICENSE file and applicable copyright notices.

Include a clear attribution statement identifying:

- Original book title.
- Original authors and contributors.
- Original repository.
- Original book website.
- Original license.
- The fact that this is a Persian translation and derivative edition.
- The date and version or commit of the source used.

Clearly state:

"This Persian edition is an unofficial translation of Single-cell Best Practices. It is not an official publication of Theis Lab and has not been reviewed or endorsed by the original authors."

Do not remove original author attribution.

# PART 10 — EXECUTION STRATEGY

This is a large book. Do not attempt to translate the entire repository in a single uncontrolled response.

Work systematically, chapter by chapter.

Use the following stages:

Stage 1: Complete source inventory and translation plan.

Stage 2: Establish the Persian terminology glossary and typography system.

Stage 3: Translate the introductory chapters.

Stage 4: Translate all preprocessing and quality-control chapters.

Stage 5: Translate all dimensionality reduction, clustering, and visualization chapters.

Stage 6: Translate all annotation and differential-expression chapters.

Stage 7: Translate all condition-specific and advanced analysis chapters.

Stage 8: Translate all remaining chapters, appendices, quizzes, and supplementary material.

Stage 9: Build the complete Persian Jupyter Book.

Stage 10: Generate the complete Word and PDF editions.

Stage 11: Perform completeness, scientific, technical, and visual quality control.

After every completed chapter:

- Save all translated files.
- Update TRANSLATION_MANIFEST.csv.
- Update TRANSLATION_PROGRESS.md.
- Preserve completed work.
- Create a meaningful Git commit when appropriate.

If your usage limit is reached or execution is interrupted, resume from the last recorded incomplete chapter.

Do not restart or overwrite completed work.

# PART 11 — FINAL DELIVERABLES

I expect:

1. A complete Persian translation of the entire book.
2. A separate Persian Jupyter Book source directory.
3. A Persian scientific terminology glossary.
4. A complete translation manifest.
5. A progress and quality-control report.
6. A fully editable Word book.
7. A professionally formatted searchable PDF book.
8. All original scientific figures and executable code preserved.
9. A separate branch in my GitHub fork containing the Persian edition.

## FINAL INSTRUCTION

Do not give me another proposal or a general explanation of how translation could be done.

I want you to actually perform the complete translation, build the Persian edition, and generate both final documents.

Start by inspecting my fork, creating the translation manifest, and preparing the Persian edition architecture.

Then proceed chapter by chapter until the entire book is translated and both final documents have been successfully generated and validated.

Communicate with me in Persian throughout the process.