# Live runs — remaining ops checklist

Scaffolding is done. This page is what still needs a **human/cluster** pass.

## 1. Bind tools (once per cluster)

**Preferred on this lab cluster** — Apptainer wrappers (no host module):

```bash
cd …/preprocessing/DL/dlsurfer
source env/cluster_containers.sh
PYTHONPATH=. python -m dlsurfer doctor
# expect [READY] core live-run deps present
```

Uses SIFs under `Documents/others/containers/` (`fastsurfer_cu126_v2.6.0`, `lit_0.6.0`, `freesurfer_7.4.1`) + `~/.freesurfer/license.txt`.

Policy: wrap FastSurfer/FS for SUBJECTS_DIR; see [`ENGINE_POLICY.md`](../reference/ENGINE_POLICY.md).  
Optional meta-image scaffold: `containers/dlsurfer.def`.

## 2. EG smoke — **passed**

Evidence: [`EG_SMOKE_EVIDENCE.md`](EG_SMOKE_EVIDENCE.md) · gate `core_lesion_eg_smoke: passed`.

```bash
source env/cluster_containers.sh
bash scripts/eg_core_lesion_smoke.sh                 # dry-run
EXECUTE=1 DEVICE=cuda bash scripts/eg_core_lesion_smoke.sh   # full re-run when GPU available
```

Login-node CPU LIT is impractical (~days); EG standalone FS2.6+LIT already completed on-cluster.

GPU re-run:

```bash
sbatch hpc/sbatch_eg_gpu_core_lesion.sh       # inpainted T1 → core + lit-post (job 191960)
sbatch hpc/sbatch_phase3_topofit_tbi_lit.sh   # TopoFit ±LIT + score JSON — done
```

TopoFit score: `work/phase3_topofit/topofit_tbi_lit_score.json` (`machine_ok=true`).

## 3. Gates

```bash
python -m dlsurfer gates
```

| Gate | Unblocks | Action |
|------|----------|--------|
| `tbi_lit_topofit` | `surf-dl-topofit*` | **passed** (machine) — [`TBI_LIT_SURFACES_REPORT.md`](TBI_LIT_SURFACES_REPORT.md) |
| `tbi_lit_surfaces` | V2C / SUGAR / DL-CTE | **open** until those ±LIT runs |
| `synthseg_pc_vs_jlf` | `structure-piriform-synthseg` | **Skipped** this round |
| `core_lesion_eg_smoke` | (ops marker) | **passed** — [`EG_SMOKE_EVIDENCE.md`](EG_SMOKE_EVIDENCE.md) |

Override only for lab debugging: `--allow-experimental`.

## 4. Schaefer execute

```bash
export SCHAEFER_ANNOT_LH=/path/fsaverage/label/lh.Schaefer2018_*.annot
export SCHAEFER_ANNOT_RH=/path/fsaverage/label/rh.Schaefer2018_*.annot
# or:
python -m dlsurfer run --profile atlas-schaefer \
  --schaefer-annot-lh … --schaefer-annot-rh … \
  --t1 T1.nii.gz --sd SD --sid S --execute
```

## 5. Metrics vs legacy multi-job

After `--execute`, compare:

- `dlsurfer_metrics.tsv` compute seconds (by device)
- SLURM queue time from `.out` / `sacct`
- Failure modes (PATH, OOM, LIT)

See [`PUBLISH.md`](PUBLISH.md).

## Intentionally not remaining as “todo”

`dlsurfer gaps-remaining` — meta-SIF (ops optional), FreeView/manual edits, TRACULA/PET/fMRI, bit-identity, Infant FS, native-LIT+split.
