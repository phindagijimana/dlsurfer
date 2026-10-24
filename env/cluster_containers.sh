# Source before dlsurfer doctor / run on this cluster (Apptainer SIFs).
#   source env/cluster_containers.sh
set -a

_DLS_ENV="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
_DLS_ROOT="$(cd "${_DLS_ENV}/.." && pwd)"

# --- SIFs (lab Documents/others/containers) ---
DLSURFER_CONTAINERS="${DLSURFER_CONTAINERS:-/mnt/nfs/home/urmc-sh.rochester.edu/pndagiji/Documents/others/containers}"
DLSURFER_SIF_FASTSURFER="${DLSURFER_SIF_FASTSURFER:-${DLSURFER_CONTAINERS}/fastsurfer_cu126_v2.6.0.sif}"
DLSURFER_SIF_FREESURFER="${DLSURFER_SIF_FREESURFER:-${DLSURFER_CONTAINERS}/freesurfer_7.4.1.sif}"
DLSURFER_SIF_LIT="${DLSURFER_SIF_LIT:-${DLSURFER_CONTAINERS}/lit_0.6.0.sif}"

# --- License ---
FS_LICENSE="${FS_LICENSE:-/mnt/nfs/home/urmc-sh.rochester.edu/pndagiji/.freesurfer/license.txt}"

# --- Homes for doctor / plan expansion ---
FASTSURFER_HOME="${_DLS_ENV}/fastsurfer_home"
FREESURFER_HOME="${_DLS_ENV}/freesurfer_home"

# Wrappers on PATH (lit-*, recon-all, mri_*)
PATH="${_DLS_ENV}/bin:${PATH}"

# Broad bind for NFS data + license
DLSURFER_APPTAINER_BINDS="${DLSURFER_APPTAINER_BINDS:--B /mnt/nfs -B ${FS_LICENSE}:${FS_LICENSE}:ro}"

# --- Schaefer annots (Yeo/CBIG 400 parcels / 17 networks on fsaverage) ---
_SCH_LABEL="${_DLS_ROOT}/resources/schaefer2018/fsaverage/label"
SCHAEFER_ANNOT_LH="${SCHAEFER_ANNOT_LH:-${_SCH_LABEL}/lh.Schaefer2018_400Parcels_17Networks_order.annot}"
SCHAEFER_ANNOT_RH="${SCHAEFER_ANNOT_RH:-${_SCH_LABEL}/rh.Schaefer2018_400Parcels_17Networks_order.annot}"

# --- V2C-Flow (literature-best Ready full CSR) ---
V2C_ROOT="${V2C_ROOT:-/mnt/nfs/home/urmc-sh.rochester.edu/pndagiji/Documents/others/Vox2Cortex}"

# --- SynthSeg-PC (experimental vs JLF; production PC stays JLF until gate) ---
SYNTHSEG_PC_ROOT="${SYNTHSEG_PC_ROOT:-/mnt/nfs/home/urmc-sh.rochester.edu/pndagiji/Documents/piriform/synthseg_pc}"
if [[ -f "${SYNTHSEG_PC_ROOT}/paths.sh" ]]; then
  # shellcheck disable=SC1091
  source "${SYNTHSEG_PC_ROOT}/paths.sh"
fi
SYNTHSEG_PC_MODEL="${SYNTHSEG_PC_MODEL:-${SYNTHSEG_PC_ROOT}/models/fold0/dice_016.h5}"
SYNTHSEG_PC_LABELS="${SYNTHSEG_PC_LABELS:-${SYNTHSEG_PC_ROOT}/config/segmentation_labels.npy}"

set +a

export DLSURFER_ROOT="$_DLS_ROOT"
export DLSURFER_CONTAINERS DLSURFER_SIF_FASTSURFER DLSURFER_SIF_FREESURFER DLSURFER_SIF_LIT
export FS_LICENSE FASTSURFER_HOME FREESURFER_HOME PATH DLSURFER_APPTAINER_BINDS
export SCHAEFER_ANNOT_LH SCHAEFER_ANNOT_RH V2C_ROOT
export SYNTHSEG_PC_ROOT SYNTHSEG_PC_MODEL SYNTHSEG_PC_LABELS
export SYNTHSEG_ROOT="${SYNTHSEG_ROOT:-}"

echo "[dlsurfer env] containers ready"
echo "  FASTSURFER_HOME=$FASTSURFER_HOME"
echo "  FREESURFER_HOME=$FREESURFER_HOME"
echo "  FS_LICENSE=$FS_LICENSE"
echo "  SIF_FASTSURFER=$DLSURFER_SIF_FASTSURFER"
echo "  SIF_LIT=$DLSURFER_SIF_LIT"
echo "  SIF_FREESURFER=$DLSURFER_SIF_FREESURFER"
echo "  SCHAEFER_ANNOT_LH=$SCHAEFER_ANNOT_LH"
echo "  V2C_ROOT=$V2C_ROOT"
echo "  SYNTHSEG_PC_MODEL=$SYNTHSEG_PC_MODEL"
