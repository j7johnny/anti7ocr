import json
from pathlib import Path

from anti7ocr import evaluate, generate, generate_batch


def test_end_to_end_workflow(tmp_path: Path):
    single = generate(
        "整合測試 sample one",
        seed=11,
        output_options={"path": tmp_path / "single.png", "format": "PNG"},
    )
    assert single.output_path is not None
    assert single.output_path.exists()

    source = tmp_path / "inputs.txt"
    source.write_text("第一行測試\nsecond line\n", encoding="utf-8")
    batch = generate_batch(
        source,
        base_seed=20,
        seed_strategy="incremental",
        output_dir=tmp_path / "batch",
    )
    assert batch.manifest_path is not None
    assert batch.manifest_path.exists()
    assert len(batch.items) == 2

    images = [item.output_path for item in batch.items if item.output_path is not None]
    labels = [item.text for item in batch.items]
    report = evaluate(images, labels, backends=["static:mocked_ocr"])
    assert len(report.samples) == 2
    assert "static" in report.avg_cer

    payload = {"avg_cer": report.avg_cer, "samples": len(report.samples)}
    (tmp_path / "report.json").write_text(json.dumps(payload), encoding="utf-8")
    assert (tmp_path / "report.json").exists()

