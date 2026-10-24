# DLSurfer: curated deep-learning morphometry

**DLSurfer** configures and runs validated FreeSurfer / FastSurfer deep-learning tools to produce **FreeSurfer-shaped `SUBJECTS_DIR` outputs** (surfaces, labels, stats) suitable for downstream analysis (including QSIRecon-style consumers).

Full documentation: use the tabs above. Source: [github.com/phindagijimana/dlsurfer](https://github.com/phindagijimana/dlsurfer).

## About

DLSurfer is an **orchestrator**, not a new morphometry method. Main features:

1. **Profile-driven plans** — choose `core`, `core-lesion`, `seg-quick`, specialty modules, etc.; preview the exact commands before running.
2. **Lesion-aware default** — standalone neuroLIT fill → ordinary FastSurfer → optional LIT postprocessing, preserving GPU seg / CPU surf HPC split.
3. **Cited engines** — every step points at the upstream tool (VINN, CerebNet, HypVINN, SynthStrip, TopoFit, …); cite engines, not DLSurfer as anatomy science.
4. **Gates** — experimental surface backends stay blocked until TBI±LIT validation evidence exists.

### Morphometry (default)

The default path wraps **FastSurfer 2.6** (VINN + modules + recon-surf) via Apptainer, optionally with **neuroLIT** lesion inpainting. Outputs are a standard FreeSurfer subject tree.

### Specialty / experimental

Optional profiles cover SynthSR preprocess, Mauri claustrum, HippUnfold, HA/BS/thalamic subfields, atlases (DK / Destrieux / Schaefer), and Phase-3 surface DL (TopoFit gated; V2C/SUGAR still open).

## Note

DLSurfer **does not replace** FreeSurfer or FastSurfer. Docs layout is inspired by QSIPrep; this project is T1 morphometry orchestration, not dMRI preprocessing.

**BIDS App:** we are **short of** a full BIDS App — see [BIDS App status](bids_app.md). Use `dlsurfer run` today; `dlsurfer bids-app` is a stub toward the standard interface.

**Citations:** every method’s CLI/resource and papers — [Methods](methods/index.md).

## Quick start

```bash
git clone https://github.com/phindagijimana/dlsurfer.git
cd dlsurfer
pip install -e .
source env/cluster_containers.sh   # Apptainer SIFs + license
dlsurfer doctor                    # expect [READY]
dlsurfer run --profile core-lesion \
  --t1 T1.nii.gz --lesion-mask lesion.nii.gz \
  --sd ./subjects --sid sub-01 --fs-license $FS_LICENSE
```

## Where to go next

| Topic | Page |
|-------|------|
| Containers & install | [Installation](installation/index.md) |
| Inputs / lesion / SUBJECTS_DIR | [Preparing data](preparing/inputs.md) |
| Minimal run & profiles | [Running](usage/minimal.md) |
| CLI flags | [Command-line reference](cli.md) |
| What is written | [Outputs](outputs/layout.md) |
| Why wrap FS/FastSurfer | [Engine policy](workflows/engine_policy.md) |
