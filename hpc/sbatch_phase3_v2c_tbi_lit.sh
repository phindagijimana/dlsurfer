#!/bin/bash
#SBATCH -J dlsurfer_v2c
#SBATCH -p interactive
#SBATCH --gres=gpu:l40s.24g:1
#SBATCH -c 8
#SBATCH --mem=48G
#SBATCH -t 08:00:00
#SBATCH -o %x_%j.out
#SBATCH -e %x_%j.err
#
# Literature-best Ready full CSR: V2C-Flow ±LIT on EG.
# Requires conda env `vox2organ` (see Vox2Cortex README) or set V2C_PYTHON.
set -euo pipefail

DLS="${SLURM_SUBMIT_DIR:-}"
if [[ -z "$DLS" || ! -f "${DLS}/env/cluster_containers.sh" ]]; then
  DLS="/mnt/nfs/home/urmc-sh.rochester.edu/pndagiji/Documents/TrackTBI-Sub/dwi_pipeline/methods/others_methods/preprocessing/DL/dlsurfer"
fi
cd "$DLS"
# shellcheck disable=SC1091
source "${DLS}/env/cluster_containers.sh"
export PATH="${DLS}/env/bin:${PATH}"
export PYTHONPATH="${DLS}${PYTHONPATH:+:$PYTHONPATH}"

T1_LIT="${T1_LIT:-/mnt/nfs/home/urmc-sh.rochester.edu/pndagiji/Documents/TrackTBI-Sub/dwi_pipeline/analysis/gugger_eg_lit/fastsurfer_inpainting/standalone/inpaint/inpainting_volumes/inpainting_result.nii.gz}"
T1_RAW="${T1_RAW:-}"  # set for no-LIT arm
SD="${SD:-${DLS}/work/phase3_v2c}"
SID=sub-EG

mkdir -p "$SD/with_lit" "$SD/no_lit"
nvidia-smi || true

if [[ -z "${V2C_PYTHON:-}" ]] && command -v conda >/dev/null 2>&1; then
  # shellcheck disable=SC1091
  source "$(conda info --base)/etc/profile.d/conda.sh" || true
  conda activate vox2organ 2>/dev/null || true
  export V2C_PYTHON="${V2C_PYTHON:-$(command -v python)}"
fi

echo "[v2c] V2C_ROOT=$V2C_ROOT V2C_PYTHON=${V2C_PYTHON:-unset}"
python -m dlsurfer run --profile surf-dl-v2c \
  --t1 "$T1_LIT" --sd "$SD/with_lit" --sid "$SID" \
  --fs-license "$FS_LICENSE" --device cuda \
  --allow-experimental --execute || echo "WARN: with-LIT V2C failed"

if [[ -n "$T1_RAW" && -f "$T1_RAW" ]]; then
  python -m dlsurfer run --profile surf-dl-v2c \
    --t1 "$T1_RAW" --sd "$SD/no_lit" --sid "$SID" \
    --fs-license "$FS_LICENSE" --device cuda \
    --allow-experimental --execute || echo "WARN: no-LIT V2C failed"
fi

echo "DONE — update gates tbi_lit_surfaces when both arms succeed + score."
