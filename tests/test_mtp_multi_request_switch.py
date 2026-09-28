# SPDX-License-Identifier: Apache-2.0
"""OMLX_MTP_MULTI_REQUEST=0 keeps multi-request batches on ordinary decode."""

from types import SimpleNamespace

from omlx.patches.mlx_lm_mtp import batch_generator as bg


def _model():
    return SimpleNamespace(_omlx_mtp_multi_request=True)


def test_switch_off_rejects_multi_request_mtp(monkeypatch):
    monkeypatch.setattr(bg, "_MULTI_REQUEST_DISABLED", True)
    assert bg._model_supports_batch_mtp(_model()) is False


def test_default_keeps_validated_adapters(monkeypatch):
    monkeypatch.setattr(bg, "_MULTI_REQUEST_DISABLED", False)
    assert bg._model_supports_batch_mtp(_model()) is True
    assert bg._model_supports_batch_mtp(SimpleNamespace()) is False


def test_switch_off_leaves_singletons_to_the_singleton_path(monkeypatch):
    monkeypatch.setattr(bg, "_MULTI_REQUEST_DISABLED", True)
    monkeypatch.setattr(bg, "_mtp_common_eligible", lambda batch: True)
    two_rows = SimpleNamespace(model=_model(), uids=[1, 2])
    assert bg._is_mtp_batch_eligible(two_rows) is False
