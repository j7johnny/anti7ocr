import json

from click.testing import CliRunner

from anti7ocr.cli import cli


def test_cli_preset_list():
    runner = CliRunner()
    result = runner.invoke(cli, ["preset", "list"])
    assert result.exit_code == 0
    payload = json.loads(result.output.strip())
    assert "tw_readable" in payload["presets"]
    assert "tw_balanced" in payload["presets"]
    assert "tw_hardened" in payload["presets"]


def test_cli_generate_and_batch(tmp_path):
    runner = CliRunner()
    out_image = tmp_path / "single.png"
    generate_result = runner.invoke(
        cli,
        [
            "generate",
            "--text",
            "hello",
            "--output",
            str(out_image),
            "--format",
            "PNG",
            "--sensitive-check",
            "--sensitive-keyword",
            "hello",
            "--sensitive-backend",
            "static:hello",
            "--sensitive-mode",
            "warn",
        ],
    )
    assert generate_result.exit_code == 0
    assert out_image.exists()

    input_file = tmp_path / "batch.txt"
    input_file.write_text("a\nb\n", encoding="utf-8")
    out_dir = tmp_path / "batch_out"
    batch_result = runner.invoke(
        cli,
        [
            "batch",
            "--input-file",
            str(input_file),
            "--output-dir",
            str(out_dir),
            "--sensitive-check",
            "--sensitive-keyword",
            "blocked",
            "--sensitive-backend",
            "static:ok",
        ],
    )
    assert batch_result.exit_code == 0
    payload = json.loads(batch_result.output.strip())
    assert payload["items"] == 2

    eval_result = runner.invoke(
        cli,
        ["eval", "--manifest", payload["manifest_path"], "--backend", "static:mocked"],
    )
    assert eval_result.exit_code == 0
    eval_payload = json.loads(eval_result.output.strip())
    assert eval_payload["sample_count"] == 2
