from pathlib import Path

from anti7ocr import generate, generate_batch
from anti7ocr.config import resolve_config


def test_generate_seed_reproducible():
    cfg = {
        "font": {"paths": [], "directories": [], "fallback_to_default": True},
        "canvas": {"width": 420, "height": 240, "supersample": 1},
    }
    out1 = generate("Hello OCR", config=cfg, seed=12345)
    out2 = generate("Hello OCR", config=cfg, seed=12345)
    assert out1.image.tobytes() == out2.image.tobytes()


def test_config_precedence(tmp_path: Path):
    yaml_path = tmp_path / "cfg.yaml"
    yaml_path.write_text(
        "canvas:\n"
        "  width: 300\n"
        "text:\n"
        "  char_to_pinyin_ratio: 0.01\n",
        encoding="utf-8",
    )
    config = resolve_config(
        preset="tw_readable",
        yaml_path=yaml_path,
        overrides={"text": {"char_to_pinyin_ratio": 0.99}},
    )
    assert config["canvas"]["width"] == 300
    assert config["text"]["char_to_pinyin_ratio"] == 0.99


def test_generate_batch_manifest(tmp_path: Path):
    input_file = tmp_path / "input.txt"
    input_file.write_text("line one\nline two\n", encoding="utf-8")
    result = generate_batch(
        input_source=input_file,
        output_dir=tmp_path / "out",
        output_format="PNG",
        base_seed=100,
        config={"font": {"paths": [], "directories": [], "fallback_to_default": True}},
    )
    assert len(result.items) == 2
    assert result.manifest_path is not None
    assert result.manifest_path.exists()

