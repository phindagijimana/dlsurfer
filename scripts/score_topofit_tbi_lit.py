#!/usr/bin/env python3
"""Score Phase-3 TopoFit ±LIT arms vs recon-surf reference (file + vertex stats)."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def _surf_stats(path: Path) -> dict:
    if not path.is_file():
        return {"exists": False, "path": str(path)}
    out: dict = {"exists": True, "path": str(path), "bytes": path.stat().st_size}
    try:
        import nibabel.freesurfer.io as fsio  # type: ignore

        coords, faces = fsio.read_geometry(str(path))
        out["n_vertices"] = int(coords.shape[0])
        out["n_faces"] = int(faces.shape[0])
        out["xyz_mean"] = [float(x) for x in coords.mean(axis=0)]
        out["xyz_std"] = [float(x) for x in coords.std(axis=0)]
    except Exception as exc:  # noqa: BLE001
        out["load_error"] = str(exc)
    return out


def _arm(root: Path) -> dict:
    surf = root / "surf"
    return {
        "root": str(root),
        "aseg": (root / "mri" / "aseg.mgz").is_file()
        or (root / "mri" / "aseg.auto_noCCseg.mgz").is_file(),
        "lh_white": _surf_stats(surf / "lh.white"),
        "rh_white": _surf_stats(surf / "rh.white"),
        "lh_white_topofit": _surf_stats(surf / "lh.white.topofit"),
        "rh_white_topofit": _surf_stats(surf / "rh.white.topofit"),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--with-lit", type=Path, required=True)
    ap.add_argument("--no-lit", type=Path, required=True)
    ap.add_argument("--ref-white-dir", type=Path, required=True, help="recon-surf EG ref subject")
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()

    report = {
        "with_lit": _arm(args.with_lit),
        "no_lit": _arm(args.no_lit),
        "ref_recon_surf": {
            "lh_white": _surf_stats(args.ref_white_dir / "surf" / "lh.white"),
            "rh_white": _surf_stats(args.ref_white_dir / "surf" / "rh.white"),
        },
        "pass_criteria": {
            "topofit_both_hemis_with_lit": False,
            "topofit_both_hemis_no_lit": False,
            "note": "Hausdorff/FreeView QC still manual; this file is machine check only.",
        },
    }
    w = report["with_lit"]
    n = report["no_lit"]
    report["pass_criteria"]["topofit_both_hemis_with_lit"] = bool(
        w["lh_white_topofit"].get("exists") and w["rh_white_topofit"].get("exists")
    )
    report["pass_criteria"]["topofit_both_hemis_no_lit"] = bool(
        n["lh_white_topofit"].get("exists") and n["rh_white_topofit"].get("exists")
    )
    report["machine_ok"] = (
        report["pass_criteria"]["topofit_both_hemis_with_lit"]
        and report["pass_criteria"]["topofit_both_hemis_no_lit"]
    )

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report["pass_criteria"], indent=2))
    print(f"wrote {args.out} machine_ok={report['machine_ok']}")
    return 0 if report["machine_ok"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
