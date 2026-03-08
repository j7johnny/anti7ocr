import json

from click.testing import CliRunner

from anti7ocr.cli import cli


def test_cli_preset_list():
    runner = CliRunner()
    result = runner.invoke(cli, ["preset", "list"])
    assert result.exit_code == 0
    payload = json.loads(result.output.strip())
    assert "tw_readable" in payload["presets"]


def test_cli_generate_and_batch(tmp_path):
    runner = CliRunner()
    out_image = tmp_path / "single.png"
    generate_result = runner.invoke(
        cli,
        ["generate", "--text", "hello", "--output", str(out_image), "--format", "PNG"],
    )
    assert generate_result.exit_code == 0
    assert out_image.exists()

    input_file = tmp_path / "batch.txt"
    input_file.write_text("a\nb\n", encoding="utf-8")
    out_dir = tmp_path / "batch_out"
    batch_result = runner.invoke(
        cli,
        ["batch", "--input-file", str(input_file), "--output-dir", str(out_dir)],
    )
    assert batch_result.exit_code == 0
    payload = json.loads(batch_result.output.strip())
    assert payload["items"] == 2

