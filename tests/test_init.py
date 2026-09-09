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
    # as_posix() — Windows 에서 str() 은 "rc\wrong.md" 가 되어 비교가 깨진다
    have = {p.relative_to(ROOT / "my.example").as_posix() for p in (ROOT / "my.example").rglob("*.md")}
    assert expected <= have


def test_ensure_gitignore_adds_missing_patterns(init, tmp_path):
    (tmp_path / ".gitignore").write_text("/my/\n__pycache__/\n", encoding="utf-8")

    added = init.ensure_gitignore(tmp_path)

    assert "/my/" not in added, "이미 있는 줄은 다시 넣지 않는다"
    assert "/private/" in added and "/*.pdf" in added
    body = (tmp_path / ".gitignore").read_text(encoding="utf-8")
    assert body.count("/my/") == 1


def test_ensure_gitignore_is_idempotent(init, tmp_path):
    (tmp_path / ".gitignore").write_text("/my/\n", encoding="utf-8")

    init.ensure_gitignore(tmp_path)
    first = (tmp_path / ".gitignore").read_text(encoding="utf-8")
    assert init.ensure_gitignore(tmp_path) == []
    assert (tmp_path / ".gitignore").read_text(encoding="utf-8") == first


def test_ensure_gitignore_creates_file_when_absent(init, tmp_path):
    added = init.ensure_gitignore(tmp_path)

    assert "/my/" in added
    assert (tmp_path / ".gitignore").exists()


def test_ensure_gitignore_never_writes_inline_comments(init, tmp_path):
    """gitignore 에서 '#' 는 줄 맨 앞에서만 주석이다 — 패턴 뒤에 붙으면 패턴이 죽는다."""
    init.ensure_gitignore(tmp_path)

    for line in (tmp_path / ".gitignore").read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped and not stripped.startswith("#"):
            assert "#" not in stripped, "패턴 줄에 인라인 주석이 붙었다: %r" % line


def test_real_gitignore_blocks_personal_files(init):
    """실제 레포의 .gitignore 가 개인 자료 경로를 전부 막고 있어야 한다."""
    present = {
        line.split("#")[0].strip()
        for line in (ROOT / ".gitignore").read_text(encoding="utf-8").splitlines()
    }
    for pattern, _note in init.PRIVATE_PATTERNS:
        assert pattern in present, "%s 가 .gitignore 에 없다" % pattern
