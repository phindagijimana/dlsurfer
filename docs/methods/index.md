# Methods & citations

DLSurfer **orchestrates** upstream tools. Every default engine has a CLI/resource and paper list in the registry.

| Page | Contents |
|------|----------|
| [Engines — resources & citations](engines.md) | Concise table + per-engine cite (from `engines.yaml`) |
| [Citation boilerplate](../citation.md) | How to cite a profile run |
| [BIDS App status](../bids_app.md) | What we still need for a BIDS App |

```bash
dlsurfer engines              # registry dump
dlsurfer cite --profile core-lesion
python scripts/gen_methods_docs.py   # refresh engines.md after YAML edits
```
