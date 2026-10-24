"""Thin BIDS App–style entrypoint (stub). Not full BIDS App compliance yet."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

from dlsurfer.adapters.plan import build_plan
from dlsurfer.runner import execute_plan


def _find_t1(bids_dir: Path, label: str) -> Path | None:
    anat = bids_dir / f"sub-{label}" / "anat"
    if not anat.is_dir():
        # try ses-*
        sub = bids_dir / f"sub-{label}"
        if sub.is_dir():
            hits = sorted(sub.glob("ses-*/anat/*T1w.nii*"))
            if hits:
                return hits[0]
        return None
    hits = sorted(anat.glob("*T1w.nii*"))
    return hits[0] if hits else None


def _find_lesion(bids_dir: Path, label: str) -> Path | None:
    sub = bids_dir / f"sub-{label}"
    patterns = (
        "anat/*lesion*.nii*",
        "anat/*Lesion*.nii*",
        "ses-*/anat/*lesion*.nii*",
    )
    for pat in patterns:
        hits = sorted(sub.glob(pat))
        if hits:
            return hits[0]
    return None


def _labels(bids_dir: Path, requested: list[str] | None) -> list[str]:
    if requested:
        return [x.removeprefix("sub-") for x in requested]
    return sorted(
        p.name.removeprefix("sub-")
        for p in bids_dir.glob("sub-*")
        if p.is_dir()
    )


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="dlsurfer bids-app",
        description=(
            "BIDS App–style stub (short of full BIDS App standard). "
            "Positional: bids_dir output_dir analysis_level."
        ),
    )
    p.add_argument("bids_dir", type=Path, help="BIDS dataset root")
    p.add_argument("output_dir", type=Path, help="Output root (used as SUBJECTS_DIR)")
    p.add_argument(
        "analysis_level",
        choices=["participant", "group"],
        help="participant = per-subject morphometry; group = stub",
    )
    p.add_argument(
        "--participant_label",
        nargs="+",
        default=None,
        help="Participant id(s) without 'sub-' prefix",
    )
    p.add_argument("--profile", default="core", help="DLSurfer profile (default: core)")
    p.add_argument("--fs-license", type=Path, default=None)
    p.add_argument("--device", default="auto", choices=["auto", "cpu", "cuda"])
    p.add_argument("--threads", type=int, default=4)
    p.add_argument(
        "--lesion-mask",
        type=Path,
        default=None,
        help="Override lesion path (else search anat/*lesion*)",
    )
    p.add_argument("--execute", action="store_true", help="Run (default: dry-run plan)")
    p.add_argument(
        "--allow-experimental",
        action="store_true",
        help="Pass through to execute_plan for gated profiles",
    )
    return p


def run_bids_app(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    bids = args.bids_dir.resolve()
    out = args.output_dir.resolve()
    if not bids.is_dir():
        print(f"[dlsurfer bids-app] missing bids_dir: {bids}", file=sys.stderr)
        return 2

    if args.analysis_level == "group":
        print("[dlsurfer bids-app] group level is a no-op stub (SUBJECTS_DIR already written).")
        return 0

    labels = _labels(bids, args.participant_label)
    if not labels:
        print("[dlsurfer bids-app] no participants found", file=sys.stderr)
        return 2

    lic = args.fs_license or (
        Path(os.environ["FS_LICENSE"]) if os.environ.get("FS_LICENSE") else None
    )
    out.mkdir(parents=True, exist_ok=True)
    rc_all = 0
    for lab in labels:
        t1 = _find_t1(bids, lab)
        if t1 is None:
            print(f"[dlsurfer bids-app] no T1w for sub-{lab}", file=sys.stderr)
            rc_all = max(rc_all, 2)
            continue
        lesion = args.lesion_mask or _find_lesion(bids, lab)
        sid = f"sub-{lab}"
        print(f"[dlsurfer bids-app] {sid} t1={t1} lesion={lesion} -> sd={out}")
        plan = build_plan(
            args.profile,
            t1=t1,
            sd=out,
            sid=sid,
            lesion_mask=lesion,
            fs_license=lic,
            device=args.device,
            threads=args.threads,
        )
        rc = execute_plan(
            plan,
            dry_run=not args.execute,
            allow_experimental=args.allow_experimental,
        )
        rc_all = max(rc_all, rc)
    return rc_all
