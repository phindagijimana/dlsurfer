#!/usr/bin/env bash
# Resume SynthSeg-PC vs JLF/MAPER gate (Hammers). Production PC stays JLF until pass.
# Literature: JLF is the best *deployed* IDEAS PC method today; SynthSeg-PC must beat it.
set -euo pipefail
DLS="$(cd "$(dirname "$0")/.." && pwd)"
# shellcheck disable=SC1091
source "${DLS}/env/cluster_containers.sh"

SSP="${SYNTHSEG_PC_ROOT:?}"
MODEL="${SYNTHSEG_PC_MODEL:?}"
LABELS="${SYNTHSEG_PC_LABELS:?}"
SS_ROOT="${SYNTHSEG_ROOT:?set SYNTHSEG_ROOT via piriform paths.sh}"

GT_DIR="${SSP_GT_DIR:-${SSP}/data/hammers_val_gt}"
IMG_DIR="${SSP_IMG_DIR:-${SSP}/data/hammers_val_img}"
OUT="${SSP_OUT:-${DLS}/work/synthseg_pc_eval/preds}"
JLF_DIR="${JLF_PRED_DIR:-}"   # optional parallel JLF preds for head-to-head
TABLES="${DLS}/work/synthseg_pc_eval"

mkdir -p "$OUT" "$TABLES"
if [[ ! -d "$GT_DIR" || ! -d "$IMG_DIR" ]]; then
  echo "[eval] missing Hammers val dirs:"
  echo "  GT_DIR=$GT_DIR"
  echo "  IMG_DIR=$IMG_DIR"
  echo "Set SSP_GT_DIR / SSP_IMG_DIR when ready; writing status stub."
  cat > "${TABLES}/STATUS.md" <<EOF
# SynthSeg-PC vs JLF — not run

- Model wired: \`$MODEL\`
- Labels: \`$LABELS\`
- Waiting on Hammers val FoV crops (\`SSP_GT_DIR\` / \`SSP_IMG_DIR\`).
- Production PC remains **JLF** until mean Dice/Jaccard ≥ JLF on PC 1/2.
EOF
  exit 2
fi

PY="${SYNTHSEG_ENV:-python3}"
"$PY" "${SSP}/predict_ideas_one.py" \
  --images "$IMG_DIR" \
  --out "$OUT" \
  --model "$MODEL" \
  --seg-labels "$LABELS" \
  --synthseg-root "$SS_ROOT"

"$PY" "${SSP}/score_val.py" \
  --gt "$GT_DIR" \
  --pred "$OUT" \
  --out-dir "$TABLES" || true

if [[ -n "$JLF_DIR" && -d "$JLF_DIR" ]]; then
  "$PY" "${SSP}/score_val.py" \
    --gt "$GT_DIR" \
    --pred "$JLF_DIR" \
    --out-dir "${TABLES}/jlf" || true
fi

echo "Wrote tables under $TABLES — update gates.yaml synthseg_pc_vs_jlf when PC ≥ JLF."
