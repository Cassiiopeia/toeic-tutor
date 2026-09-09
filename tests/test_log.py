"""log.py — 풀이 기록 추가와 유형·함정별 정답률, 약점 판정, 기간 필터."""

import importlib.util
from datetime import date
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent


@pytest.fixture
def log(tmp_path, monkeypatch):
    spec = importlib.util.spec_from_file_location("log", ROOT / "scripts" / "log.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    monkeypatch.setattr(mod, "LOG", tmp_path / "log.md")
    return mod


def test_add_writes_row_with_today(log):
    log.cmd_add("rc", "P5", "품사", "T-03", "x", "형용사 자리에 부사")
    (row,) = log.load()
    assert row["날짜"] == date.today().isoformat()
    assert row["트랙"] == "rc" and row["문항"] == "P5" and row["유형"] == "품사"
    assert row["함정"] == "T-03" and row["결과"] == "x" and row["메모"] == "형용사 자리에 부사"


def test_add_rejects_bad_track_or_mark(log):
    with pytest.raises(SystemExit):
        log.cmd_add("lc", "P1", "-", "-", "o")
    with pytest.raises(SystemExit):
        log.cmd_add("rc", "P5", "품사", "-", "ok")


def test_pipe_is_escaped(log):
    log.cmd_add("spk", "Q11", "-", "-", "t", "3/5 | 이유 하나")
    (row,) = log.load()
    assert "|" not in row["메모"]


def test_rate_counts_half_for_t(log):
    for m in ["o", "t", "x", "o"]:
        log.cmd_add("rc", "P5", "동사", "-", m)
    s = log.compute_stats(log.load())
    n, rate = s["by_kind"]["동사"]
    assert n == 4 and rate == pytest.approx(0.625)


def test_weak_needs_four_and_under_70(log):
    for m in ["x", "x", "o"]:
        log.cmd_add("rc", "P7D", "연계", "T-23", m)
    assert log.compute_stats(log.load())["weak"] == []      # n=3 — 아직 아니다
    log.cmd_add("rc", "P7D", "연계", "T-23", "x")
    assert log.compute_stats(log.load())["weak"] == ["연계"]  # n=4, 25%
    for _ in range(4):
        log.cmd_add("rc", "P5", "품사", "-", "o")
    assert "품사" not in log.compute_stats(log.load())["weak"]


def test_track_filter(log):
    log.cmd_add("rc", "P5", "품사", "-", "o")
    log.cmd_add("spk", "Q11", "-", "-", "x")
    assert log.compute_stats(log.load(), track="rc")["n"] == 1
    assert log.compute_stats(log.load(), track="spk")["n"] == 1
    assert log.compute_stats(log.load())["n"] == 2


def test_days_filter_and_trend(log):
    rows = [
        {"날짜": "2026-09-01", "트랙": "rc", "문항": "P5", "유형": "품사", "함정": "-", "결과": "x", "메모": ""},
        {"날짜": "2026-09-08", "트랙": "rc", "문항": "P5", "유형": "품사", "함정": "-", "결과": "o", "메모": ""},
    ]
    today_ = date(2026, 9, 8)
    s = log.compute_stats(rows, days=7, today_=today_)
    assert s["n"] == 1                                  # 9/1 은 7일 밖
    s_all = log.compute_stats(rows, today_=today_)
    assert s_all["recent"] == {"n": 1, "rate": 1.0}
    assert s_all["before"] == {"n": 1, "rate": 0.0}


def test_trap_counts(log):
    log.cmd_add("rc", "P5", "전접", "T-07", "x")
    log.cmd_add("rc", "P6", "P6-연결", "T-07", "x")
    log.cmd_add("rc", "P5", "품사", "-", "o")
    s = log.compute_stats(log.load())
    assert s["by_trap"]["T-07"] == (2, 0.0)
    assert "-" not in s["by_trap"]
