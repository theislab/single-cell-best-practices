from pathlib import Path
MARKDOWN={
0: Path(__file__).with_name('scrna_main.fa.md').read_text(),
1: '### پرسش‌ها\n#### فلش‌کارت‌ها',
3: '#### پرسش‌های چندگزینه‌ای',
5: '''## مشارکت‌کنندگان

از مشارکت افراد زیر صمیمانه سپاسگزاریم:

### نویسندگان

- Lukas Heumos
- Luis Heinzlmeier

### داوران

- Yuexin Chen''',
}
QUIZ={
2:{
'What are the two main categories we introduced for scRNA-seq protocols?':'دو گروه اصلی پروتکل‌های scRNA-seq که معرفی کردیم کدام‌اند؟',
'Separation in droplets and separation in physical compartments.':'جداسازی در قطره‌ها و جداسازی در محفظه‌های فیزیکی.',
'What is the main advantage of droplet-based protocols?':'مزیت اصلی پروتکل‌های مبتنی بر قطره چیست؟',
'High throughput':'توان عملیاتی بالا',
'What characterizes second-generation sequencing?':'ویژگی توالی‌یابی نسل دوم چیست؟',
'High-throughput, short-read sequencing technologies, like Illumina and Ion Torrent.':'فناوری‌های توالی‌یابی با توان عملیاتی بالا و خوانش کوتاه، مانند Illumina و Ion Torrent.',
'What is the key advantage of third-generation sequencing?':'مزیت کلیدی توالی‌یابی نسل سوم چیست؟',
'Long-read sequencing without amplification, as seen in Nanopore and PacBio.':'توالی‌یابی با خوانش بلند بدون تکثیر، مانند Nanopore و PacBio.',
},
4:{
'What is the primary purpose of scRNA-seq?':'هدف اصلی scRNA-seq چیست؟',
'To sequence the genome of a single cell':'توالی‌یابی ژنوم یک سلول منفرد',
'To measure gene expression in individual cells':'اندازه‌گیری بیان ژن در سلول‌های منفرد',
'To capture DNA methylation patterns':'ثبت الگوهای متیلاسیون DNA',
'To determine cell surface markers':'تعیین نشانگرهای سطح سلول',
'What is reverse transcription in the context of scRNA-seq?':'رونوشت‌برداری معکوس در زمینهٔ scRNA-seq چیست؟',
'Converting cDNA to mRNA':'تبدیل cDNA به mRNA',
'Sequencing the DNA':'توالی‌یابی DNA',
'Converting mRNA to cDNA':'تبدیل mRNA به cDNA',
'Labeling cell surface markers':'نشان‌دارکردن نشانگرهای سطح سلول',
'What is the main difference between single-cell and single-nuclei sequencing?':'تفاوت اصلی توالی‌یابی تک‌سلولی و تک‌هسته‌ای چیست؟',
'Single-cell captures whole cells, while single-nuclei captures only nuclei':'روش تک‌سلولی کل سلول را ثبت می‌کند، اما روش تک‌هسته‌ای فقط هسته‌ها را ثبت می‌کند',
'Single-nuclei sequencing has higher throughput':'توالی‌یابی تک‌هسته‌ای توان عملیاتی بیشتری دارد',
'Single-cell is more accurate':'روش تک‌سلولی دقیق‌تر است',
'Single-nuclei sequencing is cheaper':'توالی‌یابی تک‌هسته‌ای ارزان‌تر است',
'Which of the following best describes PIP-seq?':'کدام گزینه PIP-seq را بهتر توصیف می‌کند؟',
'A protocol using microfluidics':'پروتکلی مبتنی بر ریزسیال‌ها',
'A plate-based protocol':'پروتکلی مبتنی بر پلیت',
'A simplified droplet-based method using vortexing':'روشی ساده‌شده و مبتنی بر قطره با استفاده از ورتکس‌کردن',
'A long-read sequencing method':'روشی برای توالی‌یابی با خوانش بلند',
},
}
