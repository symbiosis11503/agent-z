#!/usr/bin/env bash
# AgentZ — combine 20 chapters into one PDF via pandoc + xelatex
# Usage: bash _scripts/build_pdf.sh [output_path]
#
# Requires: pandoc + xelatex (TeX Live) + a CJK font (Noto Sans CJK TC preferred)
# macOS:   brew install pandoc && brew install --cask mactex
# Ubuntu:  apt install pandoc texlive-xetex texlive-fonts-recommended texlive-fonts-extra fonts-noto-cjk
#
# CI uses Ubuntu via .github/workflows/release.yml
set -euo pipefail

OUT="${1:-AgentZ_v1.pdf}"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

ORDERED_CHAPTERS=(
  "chapters/ch-1_zero_basics/README.md"
  "chapters/ch00_setup/README.md"
  "chapters/ch01_llm_basics/README.md"
  "chapters/ch02_prompt/README.md"
  "chapters/ch03_what_is_agent/README.md"
  "chapters/ch04_cli_agents/README.md"
  "chapters/ch05_cli_workflow/README.md"
  "chapters/ch06_mcp/README.md"
  "chapters/ch07_skills_plugins/README.md"
  "chapters/ch08_cost_observability/README.md"
  "chapters/ch09_function_calling/README.md"
  "chapters/ch10_react_paradigms/README.md"
  "chapters/ch11_frameworks/README.md"
  "chapters/ch12_mini_framework/README.md"
  "chapters/ch13_memory_rag/README.md"
  "chapters/ch14_multi_agent/README.md"
  "chapters/ch15_deploy_audit_replay/README.md"
  "chapters/ch16_researcher/README.md"
  "chapters/ch17_builder_advanced/README.md"
  "chapters/ch18_maker_educator/README.md"
)

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
COMBINED="$TMP/combined.md"

# Cover page
cat > "$COMBINED" <<'MD'
---
title: "AgentZ — 從零到 AI Agent 構建者"
subtitle: "繁中 first-class · vendor-neutral · Claude Code 生態深 · 真零基礎 onramp · V3 sandbox-ready"
author: "Symbiosis (SBS) 團隊 + 社群貢獻者"
date: "2026-05-11"
documentclass: book
mainfont: "Noto Sans CJK TC"
sansfont: "Noto Sans CJK TC"
monofont: "Noto Sans Mono CJK TC"
CJKmainfont: "Noto Sans CJK TC"
geometry: "a4paper,margin=2cm"
fontsize: 11pt
linkcolor: blue
toc: true
toc-depth: 2
numbersections: false
---

\newpage

# 前言

這份 PDF 是 AgentZ v1 完整 20 章的離線版（2026-05-11 sealed）。

完整互動體驗請到 **https://symbiosis11503.github.io/agent-z/**——線上版有：
- 4-provider 即時試 API（key 留瀏覽器、直連 vendor）
- 互動進度檢核（localStorage 存進度）
- 本地搜尋（繁中 i18n）
- 深色 / 淺色切換

GitHub: https://github.com/symbiosis11503/agent-z
License: MIT — 章節內容跟 starter code 都可以 copy 進你自己的商業專案。

\newpage

MD

# Strip the `<LLMTryout ... />` Vue tags before pandoc (they don't render in PDF)
strip_vue() {
  python3 - "$1" <<'PY'
import sys, re, pathlib
p = pathlib.Path(sys.argv[1])
s = p.read_text(encoding="utf-8")
# Remove <LLMTryout ... /> single tag
s = re.sub(r"<LLMTryout\s+[^/]*/>", "", s, flags=re.DOTALL)
# Remove <LLMTryout> ... </LLMTryout> block (defensive)
s = re.sub(r"<LLMTryout[^>]*>.*?</LLMTryout>", "", s, flags=re.DOTALL)
# Remove <ProgressTracker /> (only on /progress page; chapters don't have it but defensive)
s = re.sub(r"<ProgressTracker\s*/>", "", s)
sys.stdout.write(s)
PY
}

for ch in "${ORDERED_CHAPTERS[@]}"; do
  if [ -f "$ch" ]; then
    echo "" >> "$COMBINED"
    echo "\\newpage" >> "$COMBINED"
    echo "" >> "$COMBINED"
    strip_vue "$ch" >> "$COMBINED"
  else
    echo "WARN: $ch not found" >&2
  fi
done

echo "[build_pdf] Combined markdown size: $(wc -c < "$COMBINED") bytes"

# Pandoc → PDF
pandoc "$COMBINED" \
  -o "$OUT" \
  --pdf-engine=xelatex \
  --toc \
  --toc-depth=2 \
  --highlight-style=tango \
  -V CJKmainfont="Noto Sans CJK TC" \
  -V mainfont="Noto Sans CJK TC" \
  -V monofont="Noto Sans Mono CJK TC" \
  -V geometry:margin=2cm \
  -V linkcolor:blue \
  --metadata title="AgentZ — 從零到 AI Agent 構建者"

echo "[build_pdf] Output: $OUT ($(du -h "$OUT" | cut -f1))"
