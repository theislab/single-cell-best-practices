# Local MyST / Jupyter Book reader

Use `persian-translation`. This builds the actual Jupyter Book 2.1.6 site using saved notebook outputs. It does not publish a website or execute scientific notebooks.

Windows prerequisites: Python 3.11+, Node.js LTS (including npm), and Git for Windows, all on PATH. Internet is required during setup/build. Double-click `SETUP_PERSIAN_BOOK.bat`, then `BUILD_PERSIAN_BOOK.bat`, then `START_PERSIAN_BOOK.bat` **inside persian-edition**. Keep the server console open; Ctrl+C stops it. The start launcher prints the loopback URL and opens the default browser. An occupied port produces a visible error. Use `python tools/local_book.py start --port 8766` to choose another port.

The launchers resolve their own directory, preserve exit codes, pause on completion/error, and keep setup/build/diagnostic output in `logs`. Run `DIAGNOSE_PERSIAN_BOOK.bat` after a failure. Do not run a BAT from the repository root unless you move the whole edition folder structure with it.

Dependencies live in `.local/venv`; the official theme and its locked npm dependencies live in `.local/book-theme`. These and generated HTML/logs are ignored by Git. The portable web build does not require LibreOffice, Pandoc, a cloud proxy package, or Linux paths. Document exports remain separate legacy tools and are not yet Windows-portable.

The site includes only translation records marked `translated_draft` or `translated_reviewed`. Newly translated chapters enter the navigation on rebuild. Source translations, notebook outputs and tracked configuration/state are not rewritten by the local build. English main remains unchanged.

Offline support is not yet certified: `logs/build-report.json` inventories external asset URLs. Math fonts/CSS and some theme integrations still require offline packaging and browser verification. Saved scientific outputs do not provide an executable Python kernel; remote data access and notebook execution require their original environments/services.

Testing limitations: Linux build/server tests are recorded separately. BAT execution and fresh dependency installation on Windows have not been tested. No claim of complete localization, final document export, or a passed final second-pass audit is made.

## Multiple Python installations

Launchers probe the actual interpreter version before selection. A working `python` on PATH at version 3.11+ takes priority; otherwise explicit `py` versions are tried (3.14, 3.13, 3.12, 3.11, then the generic Python 3 selection). An installed `py` launcher alone does not establish that its default Python is suitable. This fixes systems where `py -3` selects Visual Studio Python 3.9 while `python` selects uv-managed Python 3.12. The direct workaround is `python tools/local_book.py setup`, followed by `build` and `start`. Native Windows execution of these BAT changes has not been tested in the Linux cloud environment.
