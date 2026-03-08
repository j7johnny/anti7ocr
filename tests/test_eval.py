from anti7ocr import evaluate, generate
from anti7ocr.evaluation.backends.base import OCRBackend
from anti7ocr.evaluation.service import evaluate_images


class EchoBackend(OCRBackend):
    name = "echo"

    def recognize(self, image):
        return "hello"


class BrokenBackend(OCRBackend):
    name = "broken"

    def recognize(self, image):
        raise RuntimeError("backend failure")


def test_eval_service_with_custom_backend():
    img = generate("hello", seed=1).image
    report = evaluate_images(images=[img], gt_texts=["hello"], backends=[EchoBackend()])
    assert report.avg_cer["echo"] == 0.0


def test_eval_service_records_backend_error():
    img = generate("hello", seed=3).image
    report = evaluate_images(images=[img], gt_texts=["hello"], backends=[BrokenBackend()])
    assert report.avg_cer["broken"] == 1.0
    assert "broken" in report.samples[0].errors


def test_public_evaluate_rejects_unknown_metric(tmp_path):
    img_path = tmp_path / "one.png"
    generate("hello", seed=2, output_options={"path": img_path}).image
    try:
        evaluate([img_path], ["hello"], backends=["tesseract"], metrics=["wer"])
    except ValueError:
        assert True
    else:
        assert False, "expected ValueError for unsupported metric"
