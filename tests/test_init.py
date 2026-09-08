"""init.py — my.example/ 를 my/ 로 복사하고, 있으면 건드리지 않는다."""

import importlib.util
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent


@pytest.fixture
def init():
    spec = importlib.util.spec_from_file_location("init", ROOT / "scripts" / "init.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_copies_example_into_my(init, tmp_path):
    (tmp_path / "my.example" / "rc").mkdir(parents=True)
    (tmp_path / "my.example" / "profile.md").write_text("p", encoding="utf-8")
    (tmp_path / "my.example" / "rc" / "wrong.md").write_text("w", encoding="utf-8")

    assert init.copy_example(tmp_path) is True
    assert (tmp_path / "my" / "profile.md").read_text(encoding="utf-8") == "p"
    assert (tmp_path / "my" / "rc" / "wrong.md").read_text(encoding="utf-8") == "w"


def test_does_not_overwrite_existing_my(init, tmp_path):
    (tmp_path / "my.example").mkdir()
    (tmp_path / "my.example" / "profile.md").write_text("new", encoding="utf-8")
    (tmp_path / "my").mkdir()
    (tmp_path / "my" / "profile.md").write_text("mine", encoding="utf-8")

    assert init.copy_example(tmp_path) is False
    assert (tmp_path / "my" / "profile.md").read_text(encoding="utf-8") == "mine"


def test_real_example_has_every_file(init):
    expected = {
        "profile.md", "progress.md", "cards.md", "log.md", "tutor-log.md",
        "sessions/README.md", "rc/wrong.md", "rc/paraphrase.md", "rc/vocab.md",
        "speaking/templates.md", "speaking/materials.md",
    }
    have = {str(p.relative_to(ROOT / "my.example")) for p in (ROOT / "my.example").rglob("*.md")}
    assert expected <= have
