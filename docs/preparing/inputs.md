# Inputs

## Required

| Input | Flag | Notes |
|-------|------|--------|
| T1w NIfTI | `--t1` | 3D T1; FastSurfer will conform |
| SUBJECTS_DIR | `--sd` | **Dedicated** tree owned by DLSurfer |
| Subject ID | `--sid` | FreeSurfer-style, e.g. `sub-01` |
| FS license | `--fs-license` or `FS_LICENSE` | Required for FS/FastSurfer tools |

## Optional

| Input | Flag | When |
|-------|------|------|
| Lesion mask | `--lesion-mask` | `core-lesion` / native lesion profiles |
| Device | `--device auto\|cpu\|cuda` | Default `auto` |
| Threads | `--threads` | FastSurfer / recon-surf |
| Atlas | `--atlas dkt\|dk\|…` | Default DKT labeling |

## Not BIDS-app (yet)

Unlike QSIPrep, DLSurfer currently takes **explicit paths** (`--t1`, `--sd`, `--sid`), not a BIDS root. Keep layouts simple and reproducible.
