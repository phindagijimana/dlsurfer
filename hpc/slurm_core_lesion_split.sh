#!/bin/bash
# GPU fill+seg → CPU surf+lit-post for profile core-lesion
# Submit: sbatch hpc/slurm_core_lesion_split.sh
set -euo pipefail

#SBATCH -J dlsurfer_split
#SBATCH -o dlsurfer_split_%j.out

: "${T1:?}" "${LESION:?}" "${SD:?}" "${SID:?}" "${FS_LICENSE:?}"
: "${FASTSURFER_HOME:?}" "${FREESURFER_HOME:?}"
export FS_LICENSE FASTSURFER_HOME FREESURFER_HOME
DLS=${DLSURFER_ROOT:-$(cd "$(dirname "$0")/.." && pwd)}
export PYTHONPATH="${DLS}${PYTHONPATH:+:$PYTHONPATH}"

PART_GPU=${PART_GPU:-gpu}
PART_CPU=${PART_CPU:-cpu}
ACCOUNT=${ACCOUNT:-}

# Stage A — GPU (dry-run first if EXECUTE!=1)
JOBA=$(sbatch --parsable ${ACCOUNT:+-A "$ACCOUNT"} -p "$PART_GPU" --gres=gpu:1 \
  --wrap "cd '$DLS' && PYTHONPATH=. python -m dlsurfer run \
    --profile core-lesion --t1 '$T1' --lesion-mask '$LESION' \
    --sd '$SD' --sid '$SID' --fs-license '$FS_LICENSE' --device cuda \
    --no-post-lit \
    ${EXECUTE:+--execute}")
echo "submitted GPU stage job=$JOBA (fill+seg; post-lit deferred to CPU)"

# Note: full core-lesion plan includes surf+post. For true two-partition split,
# prefer FastSurfer --hpc srun or run seg_only / surf_only plans separately.
# This script documents the intended pattern; set EXECUTE=1 after dry-run review.

JOBB=$(sbatch --parsable ${ACCOUNT:+-A "$ACCOUNT"} -p "$PART_CPU" \
  --dependency=afterok:"$JOBA" \
  --wrap "echo 'CPU stage: re-run surf/post from plan or FastSurfer --surf_only; see LIVE_RUNS.md'")
echo "submitted CPU follow-up job=$JOBB (dependency afterok:$JOBA)"
echo "Review: PYTHONPATH=. python -m dlsurfer smoke --profile core-lesion"
