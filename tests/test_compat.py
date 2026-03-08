from anti7ocr import AntiOcr, AntiOcrCompat


def test_compat_call_returns_image():
    anti = AntiOcrCompat()
    image = anti(
        "Hello anti7ocr",
        font_fp="missing-font-file.ttf",
        seed=7,
        min_font_size=14,
        max_font_size=22,
    )
    assert image.size[0] > 0
    assert image.size[1] > 0


def test_compat_split_and_alias():
    chunks = AntiOcr.split("ABC測試123")
    assert chunks
    assert chunks[0]["type"] == "en"

