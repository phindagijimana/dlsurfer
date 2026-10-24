# BIDS App status

!!! warning "Not a BIDS App yet"
    DLSurfer **0.1** is an explicit-path orchestrator (`--t1`, `--sd`, `--sid`).
    It is **short of** the [BIDS Apps](https://bids.neuroimaging.io/faq/bids-apps.html) standard.
    A thin `bids-app` entrypoint is provided so we can grow into the interface without
    pretending full compliance.

## Gap vs BIDS App checklist

| Requirement | Status |
|-------------|--------|
| CLI: `bids_dir output_dir analysis_level` | **Stub** — `dlsurfer bids-app` |
| `--participant_label` | **Stub** |
| `--version` / `--help` | Package has `--version`; subcommand has `--help` |
| Container entrypoint (Docker/Apptainer) as sole UI | **Partial** — SIFs for tools; no single BIDS App image yet |
| BIDS validator / layout discovery | **Minimal** — finds `sub-*/anat/*T1w.nii.gz` |
| Derivatives BIDS layout under `output_dir` | **No** — still FreeSurfer `SUBJECTS_DIR` |
| Boutiques / execution-spec descriptor | **No** |
| `participant` + `group` levels | `participant` only (group = no-op stub) |

## Target interface (QSIPrep-like)

```bash
# Preview (default — no execute)
dlsurfer bids-app /data/bids /data/out participant \
  --participant_label 01 \
  --profile core-lesion \
  --fs-license $FS_LICENSE

# Run
dlsurfer bids-app /data/bids /data/out participant \
  --participant_label 01 \
  --profile core \
  --fs-license $FS_LICENSE \
  --execute
```

Maps to internal:

| BIDS | DLSurfer |
|------|----------|
| `bids_dir` | Scan for T1w (+ optional lesion) |
| `output_dir` | `--sd` (SUBJECTS_DIR root) |
| `sub-<label>` | `--sid` |
| `--profile` | Same profiles as `dlsurfer run` |

## Roadmap to a real BIDS App

1. Freeze `bids-app` argv (done as stub).  
2. Emit BIDS-ish derivatives sidecar + dataset_description.json.  
3. Single Apptainer/Docker entrypoint `dlsurfer bids-app …`.  
4. Optional Boutiques descriptor (`--bids-exec-spec`).  
5. CI with a tiny BIDS fixture (one T1w).

Until then, production use remains **`dlsurfer run --t1 … --sd … --sid …`**.
