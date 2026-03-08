from anti7ocr import generate


def test_pixel_perturbation_toggle_changes_pixels():
    base_cfg = {
        "font": {"paths": [], "directories": [], "fallback_to_default": True},
        "canvas": {"width": 360, "height": 200, "supersample": 1},
        "background": {"enable": False},
        "fragment": {"enable": False},
    }
    no_perturb = generate(
        "pixel test",
        seed=42,
        config={**base_cfg, "perturb": {"enable": False}},
    )
    with_perturb = generate(
        "pixel test",
        seed=42,
        config={
            **base_cfg,
            "perturb": {
                "enable": True,
                "edge_jitter_strength": 0.3,
                "edge_brightness_noise": 50,
                "local_contrast_noise": 0.3,
                "local_contrast_patches": 20,
                "adversarial_watermark_enable": True,
            },
        },
    )
    assert no_perturb.image.tobytes() != with_perturb.image.tobytes()

