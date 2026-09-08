#!/usr/bin/env python3
"""풀이 기록. 문제 하나를 풀 때마다 한 줄 남기고, 유형·함정별 정답률로 약점을 낸다.

    python3 scripts/log.py add <rc|spk> <문항> <유형> <함정> o|t|x ["메모"]
    python3 scripts/log.py stats [rc|spk] [--days N]

문항 P5 P6 P7S P7D P7T / Q3 ~ Q11. 유형은 카탈로그 코드(품사·동사·연계·NOT …), 함정은 T-번호 또는 -.
결과 o(맞음) t(반만 — 정답인데 근거 틀림, 토스 △) x(틀림). 정답률 = (o + 0.5·t) / n.
n ≥ 4 이고 정답률 < 70% 면 약점이다 — 세 문제로 약점을 단정하면 우연에 흔들린다.

저장은 my/log.md 한 파일. 사람이 열어 읽을 수 있게 마크다운 표로 둔다.
"""

import sys
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LOG = ROOT / "my" / "log.md"

COLS = ["날짜", "트랙", "문항", "유형", "함정", "결과", "메모"]
TRACKS = ("rc", "spk")
MARKS = {"o": 1.0, "t": 0.5, "x": 0.0}
WEAK_MIN_N = 4
WEAK_RATE = 0.70
RECENT_DAYS = 7

HEADER = """# 풀이 기록

문제 하나를 풀 때마다 한 줄. `python3 scripts/log.py stats` 가 유형·함정별 정답률을 내고 약점을 표시한다.
결과 o(맞음) · t(반만 — 정답인데 근거 틀림, 토스 △) · x(틀림). 정답률 = (o + 0.5·t) / n.

이 표는 `scripts/log.py` 가 읽고 쓴다.

"""


def today():
    return date.today().isoformat()


def esc(s):
    return str(s).replace("|", "/").replace("\n", " ").strip()


def load():
    if not LOG.exists():
        return []
    rows = []
    for line in LOG.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) != len(COLS):
            continue
        if cells[0] == COLS[0] or set(cells[0]) <= {"-", ":"}:
            continue
        rows.append(dict(zip(COLS, cells)))
    return rows


def save(rows):
    out = [HEADER, "| " + " | ".join(COLS) + " |", "|" + "---|" * len(COLS)]
    for r in rows:
        out.append("| " + " | ".join(esc(r[c]) for c in COLS) + " |")
    out.append("")
    LOG.parent.mkdir(parents=True, exist_ok=True)
    LOG.write_text("\n".join(out), encoding="utf-8")


def cmd_add(track, item, kind, trap, mark, memo=""):
    if track not in TRACKS:
        print(f"트랙은 {'/'.join(TRACKS)} 중 하나다: {track}", file=sys.stderr)
        raise SystemExit(2)
    if mark not in MARKS:
        print("결과는 o(맞음) / t(반만) / x(틀림) 중 하나다.", file=sys.stderr)
        raise SystemExit(2)
    rows = load()
    rows.append({
        "날짜": today(), "트랙": track, "문항": item, "유형": kind,
        "함정": trap or "-", "결과": mark, "메모": memo,
    })
    save(rows)
    print(f"[+] {track} {item} {kind} {trap or '-'} {mark}  {memo}".rstrip())


def _rate(rows):
    """(n, 정답률). 빈 목록이면 (0, None)."""
    if not rows:
        return 0, None
    return len(rows), sum(MARKS[r["결과"]] for r in rows) / len(rows)


def _group(rows, col, skip=("-", "")):
    groups = {}
    for r in rows:
        k = r[col]
        if k in skip:
            continue
        groups.setdefault(k, []).append(r)
    return {k: _rate(v) for k, v in groups.items()}


def compute_stats(rows, track=None, days=None, today_=None):
    """순수 함수 — 표를 받아 통계를 낸다. 출력은 cmd_stats 가 맡는다."""
    today_ = today_ or date.today()
    if track:
        rows = [r for r in rows if r["트랙"] == track]
    if days:
        cut = (today_ - timedelta(days=days)).isoformat()
        rows = [r for r in rows if r["날짜"] > cut]
    recent_cut = (today_ - timedelta(days=RECENT_DAYS)).isoformat()
    recent = [r for r in rows if r["날짜"] > recent_cut]
    before = [r for r in rows if r["날짜"] <= recent_cut]
    by_kind = _group(rows, "유형")
    weak = sorted(k for k, (n, rate) in by_kind.items() if n >= WEAK_MIN_N and rate < WEAK_RATE)
    return {
        "n": len(rows),
        "by_item": _group(rows, "문항"),
        "by_kind": by_kind,
        "by_trap": _group(rows, "함정"),
        "weak": weak,
        "recent": dict(zip(("n", "rate"), _rate(recent))),
        "before": dict(zip(("n", "rate"), _rate(before))),
    }


def _pct(rate):
    return "  —" if rate is None else f"{rate * 100:3.0f}%"


def cmd_stats(track=None, days=None):
    s = compute_stats(load(), track=track, days=days)
    if not s["n"]:
        print("기록이 없다. 문제를 풀고 log.py add 부터.")
        return
    label = track or "rc+spk"
    span = f"최근 {days}일" if days else "전체"
    print(f"{label} · {span} {s['n']}문제 · 최근 {RECENT_DAYS}일 {_pct(s['recent']['rate'])} ({s['recent']['n']}) / 이전 {_pct(s['before']['rate'])} ({s['before']['n']})\n")
    for title, key in (("문항별", "by_item"), ("유형별", "by_kind"), ("함정별", "by_trap")):
        if not s[key]:
            continue
        print(title)
        for k, (n, rate) in sorted(s[key].items(), key=lambda kv: (kv[1][1] if kv[1][1] is not None else 1, kv[0])):
            flag = "  ★약점" if key == "by_kind" and k in s["weak"] else ""
            print(f"  {k:<10} {n:3}문제 {_pct(rate)}{flag}")
        print()
    if s["weak"]:
        print("약점 (n ≥ 4 · 정답률 < 70%): " + " · ".join(s["weak"]))
    else:
        print("약점으로 확정된 유형 없음 (n ≥ 4 · 정답률 < 70% 기준).")


def main():
    a = sys.argv[1:]
    if not a:
        print(__doc__)
        raise SystemExit(2)
    cmd = a[0]
    if cmd == "add" and 6 <= len(a) <= 7:
        cmd_add(a[1], a[2], a[3], a[4], a[5], a[6] if len(a) == 7 else "")
    elif cmd == "stats":
        track = None
        days = None
        rest = a[1:]
        if rest and rest[0] in TRACKS:
            track = rest.pop(0)
        if len(rest) == 2 and rest[0] == "--days" and rest[1].isdigit():
            days = int(rest[1])
        elif rest:
            print(__doc__)
            raise SystemExit(2)
        cmd_stats(track, days)
    else:
        print(__doc__)
        raise SystemExit(2)


if __name__ == "__main__":
    main()
