import random

import numpy as np

from anti7ocr.config import resolve_config
from anti7ocr.pipeline import PipelineEngine
from anti7ocr.pipeline.context import PipelineContext


def test_pipeline_stage_contracts():
    cfg = resolve_config(
        overrides={
            "font": {"paths": [], "directories": [], "fallback_to_default": True},
            "canvas": {"width": 420, "height": 240, "supersample": 1},
        }
    )
    ctx = PipelineContext(
        text="pipeline test",
        config=cfg,
        py_rng=random.Random(1),
        np_rng=np.random.default_rng(1),
        seed=1,
    )
    out = PipelineEngine().run(ctx)
    assert out.layout is not None
    assert out.render is not None
    assert out.image is not None

