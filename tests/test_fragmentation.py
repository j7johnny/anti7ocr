from anti7ocr import generate


def test_fragment_toggle_changes_pixels():
    base_cfg = {
        "font": {"paths": [], "directories": [], "fallback_to_default": True},
        "canvas": {"width": 360, "height": 200, "supersample": 1},
        "background": {"enable": False},
        "perturb": {"enable": False},
    }
    no_fragment = generate(
        "fragment test",
        seed=99,
        config={**base_cfg, "fragment": {"enable": False}},
    )
    with_fragment = generate(
        "fragment test",
        seed=99,
        config={**base_cfg, "fragment": {"enable": True, "stroke_fragmentation_prob": 1.0}},
    )
    assert no_fragment.image.tobytes() != with_fragment.image.tobytes()

