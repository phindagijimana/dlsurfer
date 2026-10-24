# DLSurfer

[![Docs](https://img.shields.io/badge/docs-GitHub%20Pages-blue)](https://phindagijimana.github.io/dlsurfer/)
[![License](https://img.shields.io/badge/license-Apache%202.0-green)](LICENSE)
[![Python](https://img.shields.io/badge/python-%3E%3D3.9-blue)](pyproject.toml)

**Curated deep-learning morphometry orchestrator** — FreeSurfer-shaped `SUBJECTS_DIR` outputs, lesion + device policy, every engine cited.

> Does **not** replace FreeSurfer / FastSurfer science.  
> Orchestrates validated tools (FastSurfer VINN, neuroLIT, Synth*, TopoFit, …).

**Documentation (QSIPrep-style site):** https://phindagijimana.github.io/dlsurfer/

Local: `pip install -e ".[docs]" && mkdocs serve`

---

## Install / run

```bash
git clone https://github.com/phindagijimana/dlsurfer.git
cd dlsurfer
pip install -e .
source env/cluster_containers.sh   # Apptainer SIFs → doctor READY
dlsurfer doctor
dlsurfer smoke                     # doctor + dry-run core-lesion
```

```bash
dlsurfer run \
  --profile core-lesion \
  --t1 /path/T1.nii.gz \
  --lesion-mask /path/lesion.nii.gz \
  --sd /path/dlsurfer_subjects \
  --sid sub-01 \
  --fs-license /path/license.txt \
  --device auto
# add --execute to run
```

Use a **dedicated `--sd`**. See docs for profiles, HPC, gates, and outputs.

---

## Tests

```bash
pip install -e ".[dev]"
pytest -q
```

---

## Citation

```bash
dlsurfer cite --profile core-lesion
```

Cite **engines**, not DLSurfer as a morphometry method.

---

## License

Apache-2.0 for the orchestrator code and docs. Upstream FastSurfer / FreeSurfer / neuroLIT remain under their own licenses; you need a FreeSurfer license file to run those tools.
