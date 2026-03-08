from anti7ocr import generate


def test_sensitive_check_disabled_by_default():
    result = generate("normal text", seed=1)
    info = result.metadata.get("sensitive_check", {})
    assert info.get("enabled") is False


def test_sensitive_check_warn_mode_detects_keyword():
    cfg = {
        "sensitive_check": {
            "enable": True,
            "backend": "static:contains_secret_keyword",
            "keywords": ["secret_keyword"],
            "mode": "warn",
            "max_attempts": 5,
        }
    }
    result = generate("test", seed=2, config=cfg)
    info = result.metadata["sensitive_check"]
    assert info["enabled"] is True
    assert info["detected"] is True
    assert "secret_keyword" in info["detected_keywords"]
    assert result.metadata["attempt_count"] == 1


def test_sensitive_check_retry_mode_retries_until_limit():
    cfg = {
        "sensitive_check": {
            "enable": True,
            "backend": "static:always_hit",
            "keywords": ["always_hit"],
            "mode": "retry",
            "max_attempts": 3,
        }
    }
    result = generate("test", seed=3, config=cfg)
    info = result.metadata["sensitive_check"]
    assert info["detected"] is True
    assert result.metadata["attempt_count"] == 3

