# TBI ± LIT — surface DL gate report (`tbi_lit_surfaces` / `tbi_lit_topofit`)

**Date:** 2026-10-23  
**TopoFit gate:** **passed** (`tbi_lit_topofit`, machine check)  
**Remaining backends gate:** **open** (`tbi_lit_surfaces` — V2C / SUGAR / DL-CTE)  
**Skip:** SynthSeg-PC vs JLF (per request)

## Question

Before promoting `surf-dl-topofit`, `surf-dl-v2c`, `sphere-sugar`, or `thickness-fast` out of experimental: do DL surface / thickness backends remain safe on **lesioned T1** with and without **standalone LIT** vs default **recon-surf**?

## Baseline already available (EG, recon-surf — classical surfaces)

Source: `…/gugger_eg_lit/experiment_abc/COMPARISON_EG.md` (2026-10-23).

| Arm | Path | LIT wiring |
|-----|------|------------|
| **C standalone + LIT** | `standalone/fastsurfer_v2.6/subjects/sub-EG` | Fill outside → ordinary FastSurfer → posthoc LIT (**DLSurfer `core-lesion`**) |
| **A native LIT** | `native_lesion_mask/fastsurfer_v2.6/subjects/sub-EG` | `--lesion_mask` in-recon (`core-lesion-native`) |
| **B standalone 2.4.2** | `standalone/fastsurfer_v2.4.2/…` | Same fill, older FS |

### Key scalars (aseg / method)

| Contrast | Isolates | aseg Dice | Note |
|----------|----------|-----------|------|
| A_native vs C | method @ FS 2.6 | **~0.981** | Close, not bit-identical |
| B vs C | FS 2.4.2 vs 2.6 | **~0.994** | Version effect small on EG |

Surfaces: `lh/rh.white`, `lh/rh.pial`, `recon-surf.done` present on A/B/C.  
Do **not** Jaccard `lh/rh.lesion.label` across arms (non-homologous meshes).

**Baseline conclusion:** For **recon-surf** (default DLSurfer surfaces), standalone LIT (`core-lesion`) is validated on EG against native LIT and is the preferred HPC-split path.

## Phase-3 TopoFit — **machine_ok**

| Profile | Backend | ±LIT protocol | Status |
|---------|---------|---------------|--------|
| `surf-dl-topofit-only` | TopoFit WM | EG with-LIT tree + no-LIT seg→TopoFit | **passed** (`machine_ok=true`) |
| `surf-dl-topofit` | VINN + TopoFit | Full profile | Unblocked with TopoFit gate |
| `surf-dl-v2c` | V2C-Flow WM+pial | Needs V2C install/weights | **Not available** — still blocked |
| `sphere-sugar` | SUGAR | After surfaces exist ±LIT | **Not run** — still blocked |
| `thickness-fast` | DL-CTE | Biomarker only | **Not run** — still blocked |

### Score (`work/phase3_topofit/topofit_tbi_lit_score.json`)

| Arm | `lh/rh.white.topofit` | verts/hemi | Notes |
|-----|----------------------|------------|-------|
| with-LIT | yes / yes | 163842 | On EG standalone FS2.6+LIT tree |
| no-LIT | yes / yes | 163842 | FastSurfer `--seg_only --tal_reg` then TopoFit |
| ref recon-surf white | present | ~110k | Different mesh density — no vertex Jaccard |

`machine_ok=true`. FreeView / Hausdorff vs recon-surf C still **manual**.

### Ops notes (TopoFit on this cluster)

- FastSurfer CLI: `--batch` (not `--batch_size`); use 24G GPU + `--batch 1 --viewagg-device cpu`.
- FS SIF wrapper needs `--nv` for GPU tools; TopoFit **CPU** — torch 2.0+cu117 in `freesurfer_7.4.1.sif` fails `conv3d` on L40S.
- TopoFit needs a **real** `mri/norm.mgz` (surfa rejects symlinks) and `mri/transforms/talairach.lta` → use `--seg_only --tal_reg` + hardlink `orig_nu→norm`.
- Scripts: `hpc/sbatch_phase3_topofit_tbi_lit.sh`, `hpc/sbatch_phase3_topofit_nolit_finish.sh`.

```bash
source env/cluster_containers.sh
sbatch hpc/sbatch_phase3_topofit_tbi_lit.sh
# Score: work/phase3_topofit/topofit_tbi_lit_score.json
```

## Decision

| Item | Decision |
|------|----------|
| Default surfaces | Stay **recon-surf** |
| `core-lesion` standalone LIT | **Production** for lesion morphometry (EG evidence) |
| `surf-dl-topofit*` | Gate **passed** (machine); FreeView QC recommended before production science use |
| `surf-dl-v2c` / SUGAR / DL-CTE | Remain **experimental** / blocked |
| SynthSeg-PC vs JLF | **Skipped** (this round) |
