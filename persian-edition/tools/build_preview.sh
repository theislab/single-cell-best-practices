#!/usr/bin/env bash
set -euo pipefail
edition_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
fa_python="${FA_PYTHON:-/workspace/translation-tools/bin/python}"
fa_book="${FA_JUPYTER_BOOK:-/workspace/translation-tools/bin/jupyter-book}"
"$fa_python" "$edition_dir/tools/audit.py"
"$fa_python" "$edition_dir/tools/check.py"
"$fa_python" "$edition_dir/tools/prepare_preview.py"
cd "$edition_dir/_build/preview-source"
# All external requests continue through the inherited session proxy, with TLS verification.
if [[ -n "${HTTPS_PROXY:-}" && -f /workspace/translation-node/node_modules/global-agent/bootstrap.js ]]; then
  export GLOBAL_AGENT_HTTP_PROXY="$HTTPS_PROXY"
  export GLOBAL_AGENT_NO_PROXY='localhost,127.0.0.1'
  export NODE_OPTIONS="${NODE_OPTIONS:+$NODE_OPTIONS }--require /workspace/translation-node/node_modules/global-agent/bootstrap"
fi
"$fa_book" build --html --ci > "$edition_dir/qa/preview-build.log" 2>&1
"$fa_python" "$edition_dir/tools/finish_html.py"
"$fa_python" "$edition_dir/tools/export_preview.py"
"$fa_python" "$edition_dir/tools/word_to_pdf.py"
