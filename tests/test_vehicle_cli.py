from argparse import Namespace

from tools.test_vehicle import _provider_names, run


def test_vin_cascade_is_free_first(monkeypatch):
    monkeypatch.setenv("VEHICLE_PROVIDER", "autoways")
    monkeypatch.setenv("FALLBACK_PROVIDER", "matriculapt")
    assert _provider_names("vin", "cascade")[0] == "vpic"
    assert "matriculapt" not in _provider_names("vin", "cascade")


def test_plate_cascade_excludes_vpic(monkeypatch):
    monkeypatch.setenv("VEHICLE_PROVIDER", "autoways")
    monkeypatch.setenv("FALLBACK_PROVIDER", "matriculapt")
    names = _provider_names("registration", "cascade")
    assert "vpic" not in names
    assert names[:2] == ["autoways", "matriculapt"]


def test_explicit_unconfigured_provider_reports_waiting(monkeypatch):
    monkeypatch.delenv("AUTOWAYS_API_KEY", raising=False)
    monkeypatch.delenv("AUTOWAYS_API_TOKEN", raising=False)
    output, code = run(Namespace(plate="AB-12-CD", vin=None, country="PT", provider="autoways"))
    assert code == 2
    assert output["attempts"][0]["status"] == "NOT_CONFIGURED"
    assert output["next_action"].startswith("WAITING_FOR_PROVIDER")
