#!/bin/bash
set -euo pipefail
TOOL="$(basename "$0")"
: "${DLSURFER_SIF_FREESURFER:?source env/cluster_containers.sh}"
: "${FS_LICENSE:?}"
NV=()
# GPU tools (TopoFit / SynthSeg / SynthSR / …) need host NVIDIA driver bind.
if [[ "${DLSURFER_FS_NV:-1}" == "1" ]] && command -v nvidia-smi >/dev/null 2>&1; then
  NV=(--nv)
fi
exec apptainer exec \
  "${NV[@]}" \
  -B /mnt/nfs \
  -B "${FS_LICENSE}:${FS_LICENSE}:ro" \
  --env "FS_LICENSE=${FS_LICENSE}" \
  "$DLSURFER_SIF_FREESURFER" \
  "$TOOL" "$@"
