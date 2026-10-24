# DLSurfer — curated deep-learning morphometry orchestrator

DLSurfer turns a **T1w** (± lesion mask) into a **FreeSurfer-shaped `SUBJECTS_DIR`** using validated FastSurfer / FreeSurfer DL tools. With a lesion mask and profile `core-lesion`, the same plan can **inpaint T1w** (neuroLIT) then run ordinary FastSurfer so surfaces and labels are estimated on a filled anatomy. It is study-agnostic: lesion steps stay off unless you choose a lesion profile and pass a mask.

Sibling connectomics pipeline: **[DKT Connectome](https://dkt-connectome.readthedocs.io/)** (BIDS DWI → DKT connectome). DLSurfer is **isolated** morphometry orchestration — it does not import or modify the DKT workflow; handoff is optional print-only notes.

Linux + Apptainer (FreeSurfer license required). Release: **v0.1.0**.

**Next:** [What DLSurfer does](getting_started/what.md) · [Installation](installation/index.md) · [Tutorial](getting_started/tutorial.md) · [Outputs](outputs/layout.md)

This package orchestrates FastSurfer, FreeSurfer, and neuroLIT (and optional specialty tools). **Cite those papers** — [Methods / engines](methods/engines.md).

---

## Quick start

License, SIFs, and `dlsurfer doctor` are on [Installation](installation/index.md). Then the [Tutorial](getting_started/tutorial.md) (dry-run + EG evidence).

```bash
source env/cluster_containers.sh
dlsurfer doctor
dlsurfer run --profile core-lesion \
  --t1 T1.nii.gz --lesion-mask lesion.nii.gz \
  --sd ./subjects --sid sub-01 --fs-license $FS_LICENSE
# add --execute when the plan looks right
```

HPC examples: `hpc/sbatch_*.sh`. Flags: [Usage](usage/minimal.md) · full CLI: [Command-line reference](cli.md).

!!! warning "Short of a BIDS App"
    Unlike [DKT Connectome](https://dkt-connectome.readthedocs.io/) (`./run bids out participant`), DLSurfer’s production API is still explicit paths. A stub exists — [BIDS App status](bids_app.md).

---

## Contact

- GitHub: [phindagijimana/dlsurfer](https://github.com/phindagijimana/dlsurfer) · open an issue  
- Related: [DKT Connectome docs](https://dkt-connectome.readthedocs.io/) · [repo](https://github.com/phindagijimana/dkt_connectome)  
- [FAQ](troubleshooting/faq.md) · [Troubleshooting](troubleshooting/cluster.md) · [Citation](citation.md)
