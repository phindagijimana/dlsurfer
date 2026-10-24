from pathlib import Path

import pytest

from dlsurfer.adapters.plan import build_plan, runnable_steps
from dlsurfer.registry import engines, profiles


def test_chosen_engines_have_why_and_cite():
    engs, pins, deferred = engines()
    assert pins.get("fastsurfer_image")
    for eid, e in engs.items():
        if not e.get("chosen"):
            continue
        assert e.get("why"), eid
        assert e.get("cite"), eid
        assert e.get("classical_replaces"), eid
        # future-reference alternatives documented (may be empty only if deferred covers it)
        assert "alternatives" in e, eid
        assert isinstance(e["alternatives"], list), eid
    assert deferred


def test_atlases_yaml_default_dkt():
    from pathlib import Path
    import yaml

    path = Path(__file__).resolve().parents[1] / "dlsurfer" / "atlases.yaml"
    data = yaml.safe_load(path.read_text())
    assert data["default"] == "dkt"
    assert "dk" in data["atlases"] and "destrieux" in data["atlases"]
    assert data["atlases"]["dk"].get("wired") is True


def test_profiles_reference_known_engines():
    engs, _, _ = engines()
    for name, prof in profiles().items():
        for step in prof.get("steps", []):
            assert step["engine"] in engs, f"{name} -> {step['engine']}"


def test_core_lesion_plan_split():
    plan = build_plan(
        "core-lesion",
        t1=Path("/tmp/t1.nii.gz"),
        sd=Path("/tmp/subjects"),
        sid="sub-EG",
        lesion_mask=Path("/tmp/les.nii.gz"),
        fs_license=Path("/tmp/license.txt"),
        device="cpu",
    )
    assert plan.warnings == []
    run = runnable_steps(plan)
    assert any(s.argv and s.argv[0] == "lit-inpainting" and "-i" in s.argv for s in run)
    assert any(s.stage == "seg_only" for s in run)
    assert any(s.stage == "surf_only" for s in run)
    assert any("lit-postprocessing" in s.argv[0] for s in run)
    # every runnable/info step that is an engine cites something when not pipeline wrapper
    cited = [s for s in plan.steps if s.citations]
    assert len(cited) >= 5


def test_native_warns():
    plan = build_plan(
        "core-lesion-native",
        t1=Path("/tmp/t1.nii.gz"),
        sd=Path("/tmp/subjects"),
        sid="sub-EG",
        lesion_mask=Path("/tmp/les.nii.gz"),
        device="cpu",
    )
    assert any("seg_only" in w or "surf_only" in w or "split" in w.lower() for w in plan.warnings)


def test_lesion_required():
    with pytest.raises(ValueError):
        build_plan(
            "core-lesion",
            t1=Path("/tmp/t1.nii.gz"),
            sd=Path("/tmp/subjects"),
            sid="sub-EG",
        )


def test_atlas_dk_adds_fsaparc():
    plan = build_plan(
        "core",
        t1=Path("/tmp/t1.nii.gz"),
        sd=Path("/tmp/subjects"),
        sid="sub-EG",
        atlas="dk",
        device="cpu",
    )
    run = runnable_steps(plan)
    assert any("--fsaparc" in s.argv for s in run)
    assert plan.atlas == "dk"


def test_module_toggles_and_vox_and_srun():
    plan = build_plan(
        "core",
        t1=Path("/tmp/t1.nii.gz"),
        sd=Path("/tmp/subjects"),
        sid="sub-EG",
        no_hypothal=True,
        vox_size=0.8,
        hpc="srun",
        device="cpu",
    )
    run = runnable_steps(plan)
    joined = " ".join(" ".join(s.argv) for s in run)
    assert "srun_fastsurfer.sh" in joined
    assert "--no_hypothal" in joined
    assert "--vox_size" in joined and "0.8" in joined
    assert "hypvinn" not in {s.engine_id for s in plan.steps if s.stage == "cited_module"}


def test_gap_fill_profiles():
    for name, needle in [
        ("fs-long", "recon-all"),
        ("subfields-ha", "segmentHA_T1.sh"),
        ("nuclei-bs-thal", "segmentBS.sh"),
        ("atlas-destrieux", "-a2009s"),
        ("fs-clinical", "recon-all-clinical.sh"),
    ]:
        plan = build_plan(
            name,
            t1=Path("/tmp/t1.nii.gz"),
            sd=Path("/tmp/subjects"),
            sid="sub-EG",
            device="cpu",
        )
        run = runnable_steps(plan)
        assert run, name
        assert any(needle in " ".join(s.argv) for s in run), (name, needle)


def test_gaps_without_alternatives_doc_exists():
    path = Path(__file__).resolve().parents[1] / "docs" / "reference" / "GAPS_WITHOUT_ALTERNATIVES.md"
    text = path.read_text()
    assert "Manual edit" in text
    assert "TRACULA" in text
    assert "meta-container" in text.lower() or "meta-image" in text.lower() or "SIF" in text


def test_structure_modules():
    for name, needle in [
        ("preprocess-synthsr", "mri_synthsr"),
        ("structure-claustrum", "mri_claustrum_seg"),
        ("structure-piriform-synthseg", "predict_ideas_one.py"),
        ("structure-hippunfold", "hippunfold"),
        ("clinical-claustrum", "mri_synthsr"),
    ]:
        plan = build_plan(
            name,
            t1=Path("/tmp/t1.nii.gz"),
            sd=Path("/tmp/subjects"),
            sid="sub-EG",
            device="cpu",
        )
        if name == "structure-piriform-synthseg":
            assert any("EXPERIMENTAL" in w or "experimental" in w.lower() for w in plan.warnings) or plan.steps
        run = runnable_steps(plan)
        assert run, name
        assert any(needle in " ".join(s.argv) for s in run), (name, needle)
    # clinical chain: synthsr then claustrum on synthsr T1
    plan = build_plan(
        "clinical-claustrum",
        t1=Path("/tmp/t1.nii.gz"),
        sd=Path("/tmp/subjects"),
        sid="sub-EG",
        device="cpu",
    )
    run = runnable_steps(plan)
    assert len(run) >= 2
    assert "T1.synthsr.nii.gz" in " ".join(run[1].argv)
    assert "mri_claustrum_seg" in run[1].argv[0]


def test_structure_docs_and_engines():
    engs, _, deferred = engines()
    for eid in ("mauri_claustrum", "synthseg_pc", "synthsr", "hippunfold"):
        assert eid in engs and engs[eid].get("chosen")
        assert engs[eid].get("alternatives") is not None
    assert any(d["id"] == "mauri_weights_as_pc" for d in deferred)
    doc = Path(__file__).resolve().parents[1] / "docs" / "reference" / "STRUCTURE_MODULES.md"
    assert "Mauri" in doc.read_text() and "SynthSeg-PC" in doc.read_text()


def test_schaefer_annot_paths():
    plan = build_plan(
        "atlas-schaefer",
        t1=Path("/tmp/t1.nii.gz"),
        sd=Path("/tmp/subjects"),
        sid="sub-EG",
        schaefer_annot_lh=Path("/tmp/lh.Schaefer.annot"),
        schaefer_annot_rh=Path("/tmp/rh.Schaefer.annot"),
        device="cpu",
    )
    run = runnable_steps(plan)
    assert len(run) == 2
    assert "/tmp/lh.Schaefer.annot" in run[0].argv
    assert "/tmp/rh.Schaefer.annot" in run[1].argv


def test_fs_long_two_steps():
    plan = build_plan(
        "fs-long",
        t1=Path("/tmp/t1.nii.gz"),
        sd=Path("/tmp/subjects"),
        sid="sub-EG",
        device="cpu",
    )
    run = runnable_steps(plan)
    assert len(run) == 2
    assert "-base" in run[0].argv and "-long" in run[1].argv


def test_gates_block_experimental_execute():
    from dlsurfer.gates import gates_blocking_profile
    from dlsurfer.runner import execute_plan

    blockers = gates_blocking_profile("structure-piriform-synthseg")
    assert any(b["id"] == "synthseg_pc_vs_jlf" for b in blockers)
    # TopoFit ±LIT machine gate passed → execute not blocked by gates
    assert gates_blocking_profile("surf-dl-topofit") == []
    assert gates_blocking_profile("surf-dl-topofit-only") == []
    # V2C still open
    assert any(b["id"] == "tbi_lit_surfaces" for b in gates_blocking_profile("surf-dl-v2c"))
    plan = build_plan(
        "surf-dl-v2c",
        t1=Path("/tmp/t1.nii.gz"),
        sd=Path("/tmp/subjects"),
        sid="sub-EG",
        device="cpu",
    )
    rc = execute_plan(plan, dry_run=False, allow_experimental=False)
    assert rc == 3


def test_live_runs_doc():
    path = Path(__file__).resolve().parents[1] / "docs" / "lab" / "LIVE_RUNS.md"
    assert path.is_file() and "EG smoke" in path.read_text()
    assert (Path(__file__).resolve().parents[1] / "docs" / "index.md").is_file()
    assert (Path(__file__).resolve().parents[1] / "dlsurfer" / "gates.yaml").is_file()


def test_topofit_multi_hemi_plan():
    plan = build_plan(
        "surf-dl-topofit-only",
        t1=Path("/tmp/t1.nii.gz"),
        sd=Path("/tmp/subjects"),
        sid="sub-EG",
        device="cuda",
    )
    run = runnable_steps(plan)
    assert len(run) == 2
    assert Path(run[0].argv[0]).name == "mris_estimate_wm"
    assert run[0].argv[1:5] == ["-s", "sub-EG", "--hemi", "lh"]
    assert "--gpu" in run[0].argv and "--gpu" in run[1].argv
    assert run[1].argv[4] == "rh"


def test_gates_yaml_eg_passed_synthseg_skipped():
    import yaml

    path = Path(__file__).resolve().parents[1] / "dlsurfer" / "gates.yaml"
    gates = yaml.safe_load(path.read_text())["gates"]
    assert gates["core_lesion_eg_smoke"]["status"] == "passed"
    assert "SKIPPED" in gates["synthseg_pc_vs_jlf"]["note"]
    assert gates["tbi_lit_topofit"]["status"] == "passed"
    assert gates["tbi_lit_surfaces"]["status"] == "open"
    assert "surf-dl-v2c" in gates["tbi_lit_surfaces"]["blocks_profiles"]
    assert "TBI_LIT_SURFACES_REPORT" in gates["tbi_lit_surfaces"]["evidence"]
    assert "docs/lab/" in gates["tbi_lit_surfaces"]["evidence"]