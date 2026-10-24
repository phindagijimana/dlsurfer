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

set +a

export DLSURFER_ROOT="$_DLS_ROOT"
export DLSURFER_CONTAINERS DLSURFER_SIF_FASTSURFER DLSURFER_SIF_FREESURFER DLSURFER_SIF_LIT
export FS_LICENSE FASTSURFER_HOME FREESURFER_HOME PATH DLSURFER_APPTAINER_BINDS

echo "[dlsurfer env] containers ready"
echo "  FASTSURFER_HOME=$FASTSURFER_HOME"
echo "  FREESURFER_HOME=$FREESURFER_HOME"
echo "  FS_LICENSE=$FS_LICENSE"
echo "  SIF_FASTSURFER=$DLSURFER_SIF_FASTSURFER"
echo "  SIF_LIT=$DLSURFER_SIF_LIT"
echo "  SIF_FREESURFER=$DLSURFER_SIF_FREESURFER"
