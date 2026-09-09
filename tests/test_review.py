"""review.py 의 카드 추가·채점·복습 일정을 검증한다. 임시 디렉터리를 저장소로 쓴다."""

import importlib.util
from datetime import date, timedelta
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent


@pytest.fixture
def review(tmp_path, monkeypatch):
    spec = importlib.util.spec_from_file_location("review", ROOT / "scripts" / "review.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    # 실제 my/cards.md 를 건드리지 않도록 저장 위치를 바꾼다
    monkeypatch.setattr(mod, "CARDS", tmp_path / "cards.md")
    return mod


def test_add_makes_id_from_area(review):
    review.cmd_add("P5", "품사 자리 — 관사와 명사 사이", "W-001")
    review.cmd_add("P5", "두 번째", "W-002")
    review.cmd_add("T-07", "despite 뒤에 절이 오면?", "T-07")
    review.cmd_add("Q8-10", "Q9 정정 문장 첫 마디", "templates v1")
    review.cmd_add("vocab", "complimentary 뜻은?", "paraphrase")
    ids = [r["id"] for r in review.load()]
    # save() 는 (다음복습, id) 로 정렬한다 — 모두 오늘 날짜라 id 알파벳순으로 재배열된다
    assert ids == ["p5-01", "p5-02", "q810-01", "t07-01", "voca-01"]


def test_new_card_is_due_today(review):
    review.cmd_add("Q11", "역할 경계 첫 문장?", "W-001")
    (row,) = review.load()
    assert row["다음복습"] == date.today().isoformat()
    assert row["단계"] == "0"


def test_grade_o_moves_up_and_x_resets(review):
    review.cmd_add("Q11", "q", "src")
    review.cmd_grade("q11-01", "o")
    (row,) = review.load()
    assert row["단계"] == "1"
    assert row["다음복습"] == (date.today() + timedelta(days=3)).isoformat()

    review.cmd_grade("q11-01", "x")
    (row,) = review.load()
    assert row["단계"] == "0"
    assert row["다음복습"] == (date.today() + timedelta(days=1)).isoformat()


def test_grade_t_keeps_stage(review):
    review.cmd_add("Q11", "q", "src")
    review.cmd_grade("q11-01", "o")
    review.cmd_grade("q11-01", "t")
    (row,) = review.load()
    assert row["단계"] == "1"


def test_pipe_in_question_is_escaped(review):
    review.cmd_add("P7", "A | B 중 뭐가 맞나?", "W-002")
    (row,) = review.load()
    assert "|" not in row["질문"]
    assert row["근거"] == "W-002"


def test_unknown_card_exits(review):
    with pytest.raises(SystemExit):
        review.cmd_grade("nope-01", "o")


def test_add_creates_missing_parent_dir(review, tmp_path, monkeypatch):
    # my/ 가 아직 없는 첫 실행에서도 add 가 폴더까지 만들어야 한다
    monkeypatch.setattr(review, "CARDS", tmp_path / "my" / "cards.md")
    review.cmd_add("P5", "첫 카드", "W-001")
    assert (tmp_path / "my" / "cards.md").exists()
