#!/usr/bin/env bash
set -euo pipefail
echo "Running AIDLC quality gate / 正在执行AIDLC质量门禁"
python -m unittest discover -s tests -v

