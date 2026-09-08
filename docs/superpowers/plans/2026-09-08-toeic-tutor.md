# toeic-tutor 구현 계획

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 누구나 fork 해서 `/toeic init` 한 번으로 자기 수준에 맞는 토익 RC · 토익스피킹 훈련을 시작하는 공개 튜터 레포를 만든다.

**Architecture:** 규칙(CLAUDE.md)·유형·함정 카탈로그·생성 규격서·스크립트는 공개 템플릿이고, 사람마다 달라지는 것은 전부 `my/` 에 있으며 gitignore 된다. 문제는 은행에 두지 않고 규격서(`rc/generation.md`)에 따라 조수가 매번 새로 만든다. 채점 근거는 카탈로그 유형 코드와 함정 번호(T-01 …)다.

**Tech Stack:** Python 3 표준 라이브러리만 (스크립트 3개). pytest 는 테스트에만. 나머지는 전부 마크다운.

**Spec:** `docs/superpowers/specs/2026-09-08-toeic-tutor-design.md`

## Global Constraints

- 레포 루트 `/Users/suhsaechan/Desktop/Programming/project/toeic-tutor`. `main` 단일 브랜치. push 하지 않는다.
- **커밋 메시지에 Co-Authored-By 등 트레일러를 넣지 않는다.** 형식 `{영역} : {타입} : {무엇}`. 영역 `rules` · `catalog` · `gen` · `speaking` · `scripts` · `docs` · `chore`, 타입 `seed` · `fix` · `add` · `chore`.
- `my/` 는 커밋하지 않는다. `.gitignore` 에 `/my/`. `my.example/` 은 커밋한다.
- 모든 문서는 한국어. 문제·지문·템플릿 문장은 영어. 파일 안 주석은 WHY 중심의 간결한 한국어.
- 실제 기출·시중 교재 문제(와 그 변형)를 옮기지 않는다. 예시는 전부 새로 쓴다.
- 스크립트는 외부 의존성 없음. `python3 -m pytest -q` 가 항상 통과해야 한다.
- 함정 번호 T-01 ~ T-30, 유형 코드는 Task 4 의 표가 정본이다. 다른 파일은 그 코드만 쓴다.
- 어떤 파일도 "TBD" · "추후 작성" 을 남기지 않는다.

---

## 파일 구조

| 파일 | 책임 | Task |
|---|---|---|
| `.gitignore` · `README.md` · `my.example/**` | 뼈대. fork 한 사람의 첫 화면과 개인 폴더 원형 | 1 |
| `scripts/init.py` · `tests/test_init.py` | `my.example/` → `my/` 복사 | 1 |
| `scripts/review.py` · `tests/test_review.py` | 복습 카드 (interview-prep 이식) | 2 |
| `scripts/log.py` · `tests/test_log.py` | 풀이 기록 · 약점 산출 | 3 |
| `rc/format.md` · `rc/traps.md` | 시험 형식 · 함정 카탈로그 (정본 번호) | 4 |
| `rc/catalog/part5.md` | Part 5 유형 카탈로그 | 5 |
| `rc/catalog/part6.md` · `rc/catalog/part7.md` | Part 6 · 7 카탈로그 | 6 |
| `rc/generation.md` · `rc/prescriptions.md` | 생성 규격서 · 점수대별 처방 | 7 |
| `speaking/format.md` · `rubric.md` · `q1-2-read-aloud.md` · `prescriptions.md` | 토스 형식 · 잣대 · 자습 · 처방 | 8 |
| `speaking/templates/*.md` (4) · `speaking/generation.md` | 문항별 뼈대 v0 · 재료 생성 규격 | 9 |
| `tutor/playbook.md` | 검증된 튜터 방식 (이식) | 10 |
| `CLAUDE.md` · `.claude/commands/toeic.md` | 튜터 규칙 · 세션 커맨드 | 11 |
| README 최종 · 링크 점검 | 통합 | 12 |

---

### Task 1: 뼈대 — .gitignore · README 초안 · my.example · init.py

**Files:**
- Create: `.gitignore`, `README.md`, `my.example/profile.md`, `my.example/progress.md`, `my.example/cards.md`, `my.example/log.md`, `my.example/sessions/README.md`, `my.example/rc/wrong.md`, `my.example/rc/paraphrase.md`, `my.example/rc/vocab.md`, `my.example/speaking/templates.md`, `my.example/speaking/materials.md`, `my.example/tutor-log.md`
- Create: `scripts/init.py`
- Test: `tests/test_init.py`

**Interfaces:**
- Produces: `init.copy_example(root: Path) -> bool` — `my/` 가 없으면 `my.example/` 를 복사하고 True, 있으면 False.
- Produces: `my/cards.md` · `my/log.md` 의 표 머리 (Task 2 · 3 의 `load()` 가 읽는다).

- [ ] **Step 1: .gitignore**

```gitignore
# 개인 기록 — 점수·오답·세션은 로컬에만. private 로 쓰면 아래 한 줄을 지운다
/my/

# 파이썬
__pycache__/
*.pyc
.pytest_cache/
.venv/

# OS · IDE
.DS_Store
.idea/
*.iml
.vscode/
```

- [ ] **Step 2: my.example/ 열한 파일**

`my.example/profile.md`:

```markdown
# 내 프로필

`/toeic init` 이 채운다. 조수가 세션마다 읽고, debrief 뒤 갱신한다.

## 점수 · 목표

| 항목 | 값 |
|---|---|
| 최근 LC / RC | — / — (날짜: —) |
| 목표 RC | — |
| RC 시험일 | — |
| 토스 경험 | 없음 / 있음 (최근 등급 —) |
| 목표 토스 등급 | — |
| 토스 시험일 | — |

## 진단 결과 (init)

| 트랙 | 결과 |
|---|---|
| RC 진단 22문제 | — / 22 · 걸린 시간 — 분 |
| 토스 Q7 · Q11 | 추정 등급 — (발음 제외) |

## 레벨 · 약점

- RC 레벨: — (`rc/prescriptions.md` 의 구간)
- 약점 유형: — (`python3 scripts/log.py stats` 가 갱신한다)
- 스스로 느끼는 약점: —

## 처방

- 우선 파트: —
- 세션 구성: —
- 시간 목표: —
- 토스 우선 문항: —
```

`my.example/progress.md`:

```markdown
# 진도

세션이 끊겨도 여기만 보면 이어서 할 수 있다. 조수가 세션을 열 때 가장 먼저 읽는다.

## 지금 할 일

> `/toeic init` 을 아직 안 했다. init 부터.

## 일정

| 시험 | 날짜 | D-day |
|---|---|---|
| RC | — | — |
| 토스 | — | — |

## 이력

| 날짜 | 무엇 |
|---|---|
```

`my.example/cards.md` — Task 2 의 `review.py` `HEADER` 와 같은 문구 + 빈 표 머리:

```markdown
# 인출 카드

훈련에서 막힌 자리·걸린 함정·무너진 뼈대가 여기 쌓이고, 정해진 날에 다시 돌아온다.
**답은 적지 않는다** — 질문과 근거만 둔다. 카드는 같은 문제가 아니라 **같은 유형·같은 함정의 새 문제**로 묻는다.

`단계` 는 맞힌 횟수다. 0→1일, 1→3일, 2→7일, 3→21일, 4→60일 뒤에 다시 묻는다. 틀리면 0 으로.
`영역` 은 P5 · P6 · P7 · T-07(함정) · Q11 · Q8-10 · vocab · phrase 중 하나다.

이 표는 `scripts/review.py` 가 읽고 쓴다. 손으로 고쳐도 되지만 열 개수는 지킨다.

| id | 영역 | 질문 | 근거 | 단계 | 다음복습 | 이력 |
|---|---|---|---|---|---|---|
```

`my.example/log.md` — Task 3 의 `log.py` `HEADER` 와 같은 문구 + 빈 표 머리:

```markdown
# 풀이 기록

문제 하나를 풀 때마다 한 줄. `python3 scripts/log.py stats` 가 유형·함정별 정답률을 내고 약점을 표시한다.
결과 o(맞음) · t(반만 — 정답인데 근거 틀림, 토스 △) · x(틀림). 정답률 = (o + 0.5·t) / n.

이 표는 `scripts/log.py` 가 읽고 쓴다.

| 날짜 | 트랙 | 문항 | 유형 | 함정 | 결과 | 메모 |
|---|---|---|---|---|---|---|
```

`my.example/sessions/README.md`:

```markdown
# 세션 기록

세션마다 `YYYY-MM-DD.md` 하나. 조수가 닫을 때 쓴다.

문제별로 **문제 요약 · 답1 · 피드백 · 답2 · 판정**. 사용자 문장은 다듬지 않고 그대로 둔다.
못 넘긴 자리는 파일 끝 「막힌 자리」에. 그 자리는 카드가 된다.
```

`my.example/rc/wrong.md`:

```markdown
# 오답 노트

✗·△ 가 난 문제가 여기 쌓인다. **오답 이유는 내가 쓴다.** 조수는 그 문장이 카탈로그와 맞는지만 본다.
카드의 근거에 `W-번호` 를 적으면 조수가 같은 유형·같은 함정의 변형 문제를 만든다.

## W-001 · (날짜) · (문항 P5/P6/P7) · (유형) · (함정 T-번호)

**문제**
(지문·문장·선지 원문)

**내 답** — · **정답** —

**내가 쓴 오답 이유**
—
```

`my.example/rc/paraphrase.md`:

```markdown
# 패러프레이징 노트

Part 7 에서 내가 걸린 것만. 지문 표현 → 선지 표현. **일반화 방향**(구체 → 추상)을 같이 적는다.

| 날짜 | 지문에서 | 선지에서 | 방향 | 출처 (W-번호) |
|---|---|---|---|---|
```

`my.example/rc/vocab.md`:

```markdown
# 어휘

문제에서 막힌 단어. **뜻은 내가 내 말로 쓴다.** 조수가 채우지 않는다. 연어(같이 쓰는 짝)를 같이 적는다.

| 단어 | 뜻 (내 말) | 연어 · 예문 | 출처 |
|---|---|---|---|
```

`my.example/speaking/templates.md`:

```markdown
# 내 템플릿

`speaking/templates/` 의 v0 는 남이 쓴 뼈대다. 여기에 **내 문장**으로 다시 쓴 v1 부터 쌓는다. 버전은 지우지 않는다.
두 번 ○ 면 '확정'. 시험 전날엔 확정 아닌 것만 본다.

| 문항 | 상태 | 최신 버전 | 마지막 갱신 |
|---|---|---|---|
| Q3-4 사진 묘사 | 초안 | v0 | — |
| Q5-7 듣고 답하기 | 초안 | v0 | — |
| Q8-10 표 보고 답하기 | 초안 | v0 | — |
| Q11 의견 말하기 | 초안 | v0 | — |

## Q3-4

### v1 (날짜)
—

## Q5-7

## Q8-10

## Q11
```

`my.example/speaking/materials.md`:

```markdown
# 내 소재 뱅크

Q11 과 Q7 의 이유는 늘 여기서 꺼낸다. "할 말이 없다" 는 소재가 없어서다.
init 에서 대여섯 개를 캐고, 세션마다 하나씩 **영어 문장 2~3개**로 굳힌다.

| # | 소재 (한 줄) | 영어 문장 | 쓴 문항 | 상태 |
|---|---|---|---|---|
| 1 | — | — | — | 초안 |
```

`my.example/tutor-log.md`:

```markdown
# 튜터 로그 (이 사용자)

세션마다 조수가 적는다. **무엇을 시도했고, 사용자가 뭐라고 했고(말 그대로), 어떻게 판단했나** (○ 효과 / ✗ 버림 / ? 더 볼 것).
같은 시도가 두 번 ○ 면 「검증됨」, ✗ 는 즉시 「버린 것」. 공통 결함이면 `CLAUDE.md` 를 고친다.

## 검증됨 (이 사용자)

## 버린 것 (이 사용자)

## 세션 로그
```

- [ ] **Step 3: README 초안** (Task 12 에서 최종화)

```markdown
# toeic-tutor

토익 RC 와 토익스피킹을 **문제 풀이 → 근거 말하기 → 직접 교정 → 다시 → 카드 → 복습** 으로 훈련하는 Claude Code 튜터.
fork 해서 `/toeic init` 한 번이면 자기 수준에 맞게 시작한다.

## 하는 것 / 못 하는 것

- **RC(Reading)** — Part 5·6·7. 조수가 매번 새 문제를 만들고, 답이 아니라 **근거**를 채점한다.
- **토익스피킹** — Q3~Q11 을 **타이핑**으로. 내용·구조·문법·어휘·분량을 본다.
- 못 하는 것 — **리스닝 없음. 발음·억양 없음.** 조수가 소리를 못 낸다.

## 시작

```bash
git clone <this repo> && cd toeic-tutor
claude
```

```
/toeic init            점수 · 목표 · 진단 22문제 · 토스 2문항 · 소재 캐기
/toeic rc              RC 훈련 — 복습 카드 먼저, 문제 하나씩
/toeic speaking        토스 훈련
/toeic mock rc         미니 모의 (26문항 22분)  ·  /toeic mock speaking
/toeic debrief         실제 시험 뒤 점수 입력
```

## 내 기록은 어디에

`my/` 에만 쌓이고 git 에 올라가지 않는다. private 로 쓰려면 `.gitignore` 의 `/my/` 한 줄을 지운다.
```

- [ ] **Step 4: 실패하는 테스트 `tests/test_init.py`**

```python
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
```

- [ ] **Step 5: 실패 확인**

Run: `cd /Users/suhsaechan/Desktop/Programming/project/toeic-tutor && python3 -m pytest tests/test_init.py -q`
Expected: FAIL — `scripts/init.py` 없음.

- [ ] **Step 6: `scripts/init.py`**

```python
#!/usr/bin/env python3
"""my/ 뼈대를 만든다. my.example/ 를 그대로 복사한다.

    python3 scripts/init.py

질문(점수·목표·약점)은 여기서 하지 않는다 — 조수가 채팅으로 묻고 my/profile.md 에 적는다.
my/ 가 이미 있으면 아무것도 건드리지 않는다. 남의 기록을 덮어쓰는 일은 없어야 한다.
"""

import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def copy_example(root):
    """my.example/ → my/. 이미 있으면 False."""
    src, dst = root / "my.example", root / "my"
    if dst.exists():
        return False
    shutil.copytree(src, dst)
    return True


def main():
    if copy_example(ROOT):
        print("[+] my/ 를 만들었다. 이제 조수가 점수·목표·약점을 묻는다 (/toeic init).")
    else:
        print("my/ 가 이미 있다. 건드리지 않았다.", file=sys.stderr)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
```

- [ ] **Step 7: 통과 확인**

Run: `python3 -m pytest tests/test_init.py -q`
Expected: 3 passed.

- [ ] **Step 8: 실제로 돌려 my/ 생성 확인 후 되돌리기**

Run: `python3 scripts/init.py && ls my && git status --short` — `my/` 가 status 에 안 보여야 한다 (gitignore). 확인 뒤 `rm -rf my` 는 하지 않는다 — 본인 init 에 그대로 쓴다.

- [ ] **Step 9: 커밋**

```bash
git add .gitignore README.md my.example scripts/init.py tests/test_init.py
git commit -m "chore : seed : 뼈대 — .gitignore(my/ 제외) · README 초안 · my.example 11파일 · init.py"
```

---

### Task 2: review.py 이식

**Files:**
- Create: `scripts/review.py` (원본 `../interview-prep/scripts/review.py`)
- Test: `tests/test_review.py` (원본 `../interview-prep/tests/test_review.py`)

**Interfaces:**
- Produces: CLI `review.py due | add <영역> "질문" "근거" | grade <id> o|t|x | list [<영역>] | stats`. 저장 `my/cards.md`.
- Consumes: Task 1 의 `my.example/cards.md` 표 머리 (열 7개 `id 영역 질문 근거 단계 다음복습 이력`).

- [ ] **Step 1: 원본 복사**

```bash
cp ../interview-prep/scripts/review.py scripts/review.py
cp ../interview-prep/tests/test_review.py tests/test_review.py
```

- [ ] **Step 2: 바꿀 곳 — 저장 위치 · 문구 · 영역 예시**

`scripts/review.py`:
- 모듈 docstring 첫 줄을 `"""인출 카드와 복습 일정. interview-prep 의 review.py 를 이식했다 — 저장 위치와 영역 값만 다르다.` 로, 사용법의 `<영역>` 설명을 `(영역: P5 · P6 · P7 · T-07 · Q11 · Q8-10 · vocab · phrase)` 로.
- `CARDS = ROOT / "knowledge" / "cards.md"` → `CARDS = ROOT / "my" / "cards.md"`.
- `HEADER` 를 Task 1 의 `my.example/cards.md` 머리글(표 머리 제외)과 **같은 문구**로.
- `save()` 의 `CARDS.parent.mkdir(exist_ok=True)` → `CARDS.parent.mkdir(parents=True, exist_ok=True)`.
- 다른 로직은 손대지 않는다.

`tests/test_review.py`:
- `test_add_makes_id_from_area` 를 이 레포의 영역 값으로:

```python
def test_add_makes_id_from_area(review):
    review.cmd_add("P5", "품사 자리 — 관사와 명사 사이", "W-001")
    review.cmd_add("P5", "두 번째", "W-002")
    review.cmd_add("T-07", "despite 뒤에 절이 오면?", "T-07")
    review.cmd_add("Q8-10", "Q9 정정 문장 첫 마디", "templates v1")
    review.cmd_add("vocab", "complimentary 뜻은?", "paraphrase")
    ids = [r["id"] for r in review.load()]
    assert ids == ["p5-01", "p5-02", "t07-01", "q810-01", "voca-01"]
```

- 나머지 테스트의 `"S-03"` · `"Q-11"` · `"facts"` 는 각각 `"P5"` · `"Q11"` · `"P7"` 로 바꾸고 기대 id 도 맞춘다 (`q11-01`).

- [ ] **Step 3: 테스트**

Run: `python3 -m pytest tests/test_review.py -q`
Expected: 6 passed.

- [ ] **Step 4: `my/` 없이도 add 가 폴더를 만드는지**

Run: `mv my my.bak 2>/dev/null; python3 scripts/review.py add P5 "테스트" "x" && cat my/cards.md | tail -2 && rm -rf my && mv my.bak my 2>/dev/null; true`
Expected: `[+] p5-01  테스트` 와 표 한 줄.

- [ ] **Step 5: 커밋**

```bash
git add scripts/review.py tests/test_review.py
git commit -m "scripts : seed : review.py 이식 — 저장 my/cards.md, 영역 P5·T-07·Q11"
```

---

### Task 3: log.py — 풀이 기록과 약점 산출

**Files:**
- Create: `scripts/log.py`
- Test: `tests/test_log.py`

**Interfaces:**
- Produces: CLI `log.py add <rc|spk> <문항> <유형> <함정> <o|t|x> ["메모"]`, `log.py stats [rc|spk] [--days N]`.
- Produces: `compute_stats(rows, track=None, days=None, today_=None) -> dict` with keys `n`, `by_item`, `by_kind`, `by_trap` (each `{key: (n, rate)}`), `weak` (list of kinds), `recent` / `before` (`{"n": int, "rate": float|None}`).
- Consumes: Task 1 의 `my.example/log.md` 표 머리 (열 7개).

- [ ] **Step 1: 실패하는 테스트**

```python
"""log.py — 풀이 기록 추가와 유형·함정별 정답률, 약점 판정, 기간 필터."""

import importlib.util
from datetime import date, timedelta
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
```

- [ ] **Step 2: 실패 확인**

Run: `python3 -m pytest tests/test_log.py -q`
Expected: FAIL — `scripts/log.py` 없음.

- [ ] **Step 3: `scripts/log.py`**

```python
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
```

- [ ] **Step 4: 통과 확인**

Run: `python3 -m pytest tests/test_log.py -q`
Expected: 8 passed.

- [ ] **Step 5: 손으로 한 번**

Run: `python3 scripts/log.py add rc P5 품사 T-03 x "시험" && python3 scripts/log.py stats rc && python3 scripts/log.py stats rc --days 1`
Expected: 표 출력, 약점 없음 문구. 확인 뒤 `my/log.md` 의 시험 줄을 지운다 (표 머리만 남긴다).

- [ ] **Step 6: 커밋**

```bash
git add scripts/log.py tests/test_log.py
git commit -m "scripts : add : log.py — 풀이 기록 add/stats, 유형·함정별 정답률, n≥4·70% 미만 약점"
```

---

### Task 4: rc/format.md · rc/traps.md (함정 카탈로그 — 정본 번호)

**Files:**
- Create: `rc/format.md`, `rc/traps.md`

**Interfaces:**
- Produces: 함정 번호 T-01 ~ T-30 과 유형 코드. **이후 모든 파일은 이 코드만 쓴다.**

유형 코드 (log.py `유형` 열 · 카탈로그 제목 · CLAUDE.md 채점 근거):

| 파트 | 코드 |
|---|---|
| Part 5 | `품사` `동사` `준동사` `전접` `대명` `어휘` `구문` |
| Part 6 | `P6-문법` `P6-어휘` `P6-연결` `P6-삽입` |
| Part 7 | `세부` `추론` `NOT` `동의어` `삽입위치` `의도` `목적` `연계` |

- [ ] **Step 1: 웹 확인 (10분 한도)**

WebSearch 두 번: `"토익 파트5 출제 유형 비율 품사 동사 어휘 2025 2026"`, `"토익 파트7 문제 유형 비율 세부사항 추론 동의어 문장삽입 의도파악"`. 얻을 것 — 유형별 대략 출제 비율 (Part 5 에서 어휘 ≈ 1/3, 품사 ≈ 1/4 등). 비율이 확인되면 `format.md` 에 "대략" 으로 적고 출처 링크. 확인 안 되면 적지 않는다.

- [ ] **Step 2: `rc/format.md`**

내용 (전부 있어야 한다):
- 75분 100문항 · 파트별 문항 수와 번호 (5: 101~130 · 6: 131~146 · 7: 147~200 — 단일 10지문 29문항 147~175, 이중 2세트 176~185, 삼중 3세트 186~200).
- 권장 시간 배분 표 (Part 5 10분 · Part 6 8분 · Part 7 55분 · 마킹 2분) 와 문항당 목표 초 (20 · 30 · 60).
- Part 7 지문 종류 9가지 목록.
- 점수 환산의 대략 (RC 원점수 → 환산 5~495, 문항당 약 5점, 정확한 환산표는 회차마다 다름 — 이 한 줄).
- "이 레포가 다루지 않는 것: LC" 한 줄.
- Step 1 에서 확인된 유형 비율 (있으면).
- 출처 링크 (toeic.ai/reading · 990prep · 토익스토리).

- [ ] **Step 3: `rc/traps.md`**

머리말 세 줄 (함정 번호는 채점 근거다 · 문제를 만들 때 반드시 하나 심는다 · 오답 노트와 카드가 이 번호를 쓴다) 뒤에 표. **열: `번호 | 이름 | 어떻게 속이나 | 빠져나오는 신호 | 파트`.** 30개 전부, 아래 이름과 순서 그대로:

| 번호 | 이름 | 파트 |
|---|---|---|
| T-01 | 형태 유사 오답 — 같은 어근 다른 품사 | 5·6 |
| T-02 | 명사 둘 — 사람/사물 · 가산/불가산 | 5·6 |
| T-03 | 형용사 vs 부사 자리 (be 뒤 · 명사 앞 · -ly 형용사) | 5·6 |
| T-04 | 주어-동사 사이 긴 수식어 (수일치) | 5·6 |
| T-05 | 시간 단서가 문장 끝 (시제) | 5·6 |
| T-06 | 태 — 뒤에 목적어 있으면 능동, 자동사는 수동 불가 | 5·6 |
| T-07 | 뜻 같고 자리 다른 짝 (despite/although · during/while · because/because of) | 5·6 |
| T-08 | 앞 동사가 정하는 준동사 형태 (enjoy -ing · decide to · 사역) | 5·6 |
| T-09 | 재귀·소유 대명사 (own 앞 소유격 · by oneself) | 5·6 |
| T-10 | 관계사 — 선행사 사람/사물 · 완전/불완전 절 · whose | 5·6 |
| T-11 | 연어 — 뜻은 맞는데 짝이 틀림 (make a decision · meet a deadline) | 5·6 |
| T-12 | 비슷한 뜻 어휘 쌍 (rise/raise · affect/effect · borrow/lend) | 5·6 |
| T-13 | 접속부사 vs 접속사 (however 는 절을 못 잇는다) | 5·6 |
| T-14 | 상관접속사 짝 (either…or · not only…but also) | 5·6 |
| T-15 | 비교급·최상급 신호 (than · of all · the -est) | 5·6 |
| T-16 | 문장 삽입 — 주제만 맞고 흐름 안 맞음 | 6 |
| T-17 | 연결어 방향 (however/therefore/in addition) | 6 |
| T-18 | 시제 — 앞 문장 시점 무시 | 6 |
| T-19 | 지시어·대명사 지시 대상 (this · these · it) | 6 |
| T-20 | 지문 단어 그대로 재사용한 오답 (정답은 패러프레이즈) | 7 |
| T-21 | 부분 진실 — 선지 절반은 맞고 절반은 틀림 | 7 |
| T-22 | 다른 인물·날짜·금액에 붙은 정보 뒤섞기 | 7 |
| T-23 | 연계 근거가 다른 지문에 — 한 지문만 보고 답함 | 7 |
| T-24 | NOT/EXCEPT — 언급된 셋을 다 찾기 전에 고름 | 7 |
| T-25 | 동의어 — 사전 뜻 vs 문맥 뜻 | 7 |
| T-26 | 추론 과잉 — 지문에 없는 상식으로 답함 | 7 |
| T-27 | 문장 위치 — 대명사·연결어 단서 무시 | 7 |
| T-28 | 의도 문제 — 문자 그대로 해석 (반어 · 맥락) | 7 |
| T-29 | 목적 문제 — 첫 문장이 아니라 본문 중간에 목적 | 7 |
| T-30 | 시간 함정 — 긴 지문을 다 읽음 (문제 먼저 → 스캔) | 7 |

「어떻게 속이나」와 「빠져나오는 신호」는 각각 한 문장. 영어 예시 짝을 하나씩 괄호로 (T-20: `for free` → `complimentary`).
표 뒤에 「유형 코드」 절 — 위의 유형 코드 표를 그대로 싣고 "log.py 유형 열과 카탈로그 제목은 이 코드만 쓴다" 한 줄.

- [ ] **Step 4: 검증**

Run: `grep -c '^| T-' rc/traps.md` → `30`. `grep -o 'T-[0-9][0-9]' rc/traps.md | sort -u | wc -l` → `30`.

- [ ] **Step 5: 커밋**

```bash
git add rc/format.md rc/traps.md
git commit -m "catalog : seed : RC 형식 · 함정 카탈로그 T-01~T-30 · 유형 코드 정본"
```

---

### Task 5: rc/catalog/part5.md

**Files:**
- Create: `rc/catalog/part5.md`

**Interfaces:**
- Consumes: Task 4 의 유형 코드 7개 · T-01 ~ T-15.

- [ ] **Step 1: 웹 조사 (15분 한도)**

WebSearch: `"토익 파트5 품사 문제 풀이 신호 빈칸 앞뒤 관사 소유격 전치사"`, `"토익 part 5 어휘 문제 연어 collocation 빈출"`, `"토익 파트5 전치사 접속사 구별 문제 despite although during while"`. 얻을 것 — 유형별 **신호(빈칸 앞뒤에서 보는 것)** 와 **빈출 짝**. 문제를 베끼지 않는다. 신호와 짝 목록만 가져온다.

- [ ] **Step 2: 파일 구조**

머리말: "유형은 밝히지 않고 낸다. 사용자가 유형을 판별하는 것이 첫 채점 항목이다" · "각 유형의 「신호」가 △ 채점의 근거다".

유형 7개 각각 `## 품사` 처럼 코드를 제목으로. 절마다 **다섯 항목**을 이 소제목으로:

1. **무엇을 묻나** — 한 문장.
2. **신호 — 빈칸 앞뒤에서 보는 것** — 불릿 3~6개. 예: 품사 → "관사·소유격 뒤 + 명사 앞 = 형용사", "타동사 뒤 목적어 자리 = 명사", "완전한 문장 사이 = 부사", "be + ___ + p.p. = 부사".
3. **풀이 순서** — 번호 3단계 이내. 예: 동사 → "① 주어 찾기(수식어 걷어내기) ② 시간 단서 찾기(문장 끝까지) ③ 목적어 유무로 태".
4. **함정** — 이 유형에 심는 T-번호와 한 줄. (품사: T-01 T-02 T-03 · 동사: T-04 T-05 T-06 · 준동사: T-08 · 전접: T-07 T-13 T-14 · 대명: T-09 T-10 · 어휘: T-11 T-12 · 구문: T-15)
5. **예시 2개** — 조수가 새로 쓴 문제. 각각 `**101.**` 번호 · 문장(12~25단어) · (A)~(D) · 그 아래 접힌 해설 `<details><summary>정답·해설</summary> … 정답 · 신호 · 심은 함정 T-번호 · 오답 셋이 왜 틀렸나 </details>`. 예시 하나는 기본, 하나는 실전 난이도.

마지막 절 `## 빈출 짝` — 전접 (despite/although · during/while · because/because of · in spite of/even though) · 어휘 연어 20개 (`make/reach a decision` `meet a deadline` `place an order` …) · 시간 단서와 시제 (by the time → 과거완료/미래완료 · since → 현재완료 · next week → 미래 · recently → 현재완료/과거) 표.

- [ ] **Step 3: 검증**

Run: `grep -c '^## ' rc/catalog/part5.md` → 8 이상. `grep -c '<details>' rc/catalog/part5.md` → 14. `grep -o 'T-[0-9][0-9]' rc/catalog/part5.md | sort -u` 가 T-01~T-15 안에만 있다.

- [ ] **Step 4: 커밋**

```bash
git add rc/catalog/part5.md
git commit -m "catalog : seed : Part 5 유형 7개 — 신호 · 풀이 순서 · 함정 · 예시 14문제 · 빈출 짝"
```

---

### Task 6: rc/catalog/part6.md · rc/catalog/part7.md

**Files:**
- Create: `rc/catalog/part6.md`, `rc/catalog/part7.md`

**Interfaces:**
- Consumes: Task 4 유형 코드 (P6 4개 · P7 8개) · T-16 ~ T-30.

- [ ] **Step 1: 웹 조사 (15분 한도)**

WebSearch: `"토익 파트6 문장삽입 문제 풀이법 대명사 연결어 앞뒤 문장"`, `"토익 파트7 의도파악 문제 문자메시지 online chat what does she mean when she writes"`, `"토익 파트7 삼중지문 연계문제 풀이 어느 지문 근거"`. 얻을 것 — 문장 삽입 단서 목록, 의도 문제의 전형적 질문 문구, 연계 문제의 근거 배치 패턴.

- [ ] **Step 2: `rc/catalog/part6.md`**

머리말: 4지문 × 4문항 · 지문 80~130단어 · 빈칸 4 = 문법 1 + 어휘 1 + 연결어/시제 1 + 문장 삽입 1 · "빈칸 문장만 봐서는 못 푼다 — 앞뒤 한 문장이 단서".

유형 4개 (`## P6-문법` `## P6-어휘` `## P6-연결` `## P6-삽입`) 각각 Task 5 와 같은 다섯 항목. 삽입 유형의 신호는 반드시 — 삽입 문장 안의 대명사·지시어(this policy, these changes) · 연결어(however, for example, in addition) · 시제 · 관사(the 가 가리키는 앞 명사).

예시: 지문 **2개** (이메일 1 · 공지 1, 각 100단어 안팎) 에 빈칸 4개씩, 문항 번호 131~138. 각 지문 뒤 `<details>` 해설에 4문항 정답 · 유형 · T-번호.

- [ ] **Step 3: `rc/catalog/part7.md`**

머리말: 54문항 구성 (단일 29 · 이중 10 · 삼중 15) · 지문 종류 9가지 · "문제 먼저 읽고 스캔한다 (T-30)" · "정답은 패러프레이즈, 오답은 지문 단어 그대로 (T-20)".

절 1 `## 지문 종류와 어디를 먼저 보나` — 9종 표: 종류 | 먼저 보는 곳 | 자주 묻는 것. (이메일 → 제목·발신/수신·첫 문단 목적 · 마지막 문단 요청 / 문자 체인 → 시각과 발화자, 의도 문제 / 일정표·청구서 → 연계 문제의 근거 창고 …)

절 2 유형 8개 (`## 세부` `## 추론` `## NOT` `## 동의어` `## 삽입위치` `## 의도` `## 목적` `## 연계`) 각각: 무엇을 묻나 · **질문 문구의 전형** (영어: "What is indicated about …?" / "What is NOT mentioned …?" / "The word 'address' in paragraph 2, line 3 is closest in meaning to" / "In which of the positions marked [1]…[4] does the following sentence best belong?" / "At 10:15, what does Mr. Kim most likely mean when he writes, '…'?" / "What is the purpose of the e-mail?" / 연계는 "What is suggested about the order?" 같은 두 지문 결합형) · 풀이 순서 · 함정 T-번호 (세부: T-20 T-21 T-22 · 추론: T-26 · NOT: T-24 · 동의어: T-25 · 삽입위치: T-27 · 의도: T-28 · 목적: T-29 · 연계: T-23 T-22).

절 3 `## 예시` — **단일 지문 1개** (문자 체인, 120단어, 문항 3개: 의도 1 · 세부 1 · 추론 1) · **이중 지문 1세트** (이메일 + 일정표, 합 350단어, 문항 5개: 목적 · 세부 · 연계 · 동의어 · NOT). 각 세트 뒤 `<details>` 해설: 문항별 정답 · 유형 · 근거 문장(지문 몇, 문단 몇) · T-번호 · 패러프레이징 쌍.

절 4 `## 패러프레이징 방향` — 구체 → 일반 원칙 한 문단 + 쌍 20개 표 (`for free → complimentary` · `arrived after 12 → was late` · `every year → annually` · `purchase → buy` · `fix → repair` …).

- [ ] **Step 4: 검증**

Run: `grep -c '^## ' rc/catalog/part6.md` → 5 이상 · `grep -c '<details>' rc/catalog/part6.md` → 2. `grep -c '^## ' rc/catalog/part7.md` → 12 · `grep -c '<details>' rc/catalog/part7.md` → 2. 두 파일의 T-번호가 T-16~T-30 (part7 은 T-20~T-30) 안에만.

- [ ] **Step 5: 커밋**

```bash
git add rc/catalog/part6.md rc/catalog/part7.md
git commit -m "catalog : seed : Part 6 유형 4 · Part 7 유형 8 — 질문 문구 · 근거 위치 · 예시 세트 · 패러프레이징 20쌍"
```

---

### Task 7: rc/generation.md · rc/prescriptions.md

**Files:**
- Create: `rc/generation.md`, `rc/prescriptions.md`

**Interfaces:**
- Consumes: Task 4~6 의 코드 · 함정. 스펙 §7 · §8.
- Produces: CLAUDE.md(Task 11) 가 "문제를 만들 때 `rc/generation.md` 를 따른다" 로 가리킨다.

- [ ] **Step 1: `rc/generation.md`**

머리말: "이 파일이 조수를 묶는다. 없으면 쉬운 문제만 나온다." · "문제와 해설을 같이 주지 않는다" · "기출·교재를 옮기지 않는다".

절:
1. `## 공통` — 스펙 §7 RC 공통 7줄 (번호 체계 · Directions 원문 · 지문 표기(인용문/코드 블록) · 선지 (A)~(D) · 정답 분포(3연속 금지) · **문제마다 T-번호 하나 이상 내부 결정, 해설 때 공개** · 맥락 9종 순환 · 저작권). Directions 원문 세 개(Part 5·6·7)를 여기 그대로 싣는다.
2. `## 난이도 3단계` — 표: 단계 | Part 5 | Part 6 | Part 7. (기본: 신호가 빈칸 바로 옆 · 함정 0~1 · 단일 150단어 이하 / 실전: 수식어로 신호 가림 · 함정 1~2 · 이중 / 고난도: 함정 2 이상 · 어휘 문제에 유사 뜻 3개 · 삼중 500단어 이상 + 연계 2개). 올리는 조건 "최근 10문제 80% 이상", 내리는 조건 "60% 미만".
3. `## Part 5` — 스펙 §7 표 (유형 | 선지 구성 규칙 | 필수 함정) 그대로 + 문장 길이 12~25단어 + "한 세션 안에서 같은 유형 연속 3개 금지 (약점 반복 훈련일 때 예외)".
4. `## Part 6` — 스펙 §7 Part 6 네 줄 + 삽입 선지 4개 작성 규칙 (전부 주제 관련 · 정답만 앞 문장의 명사를 대명사/the 로 받음 · 오답 하나는 시제가 어긋남 · 오답 하나는 연결어 방향이 반대).
5. `## Part 7` — 스펙 §7 표(구성·단어 수) + 지문 9종 + 문제 유형 조합 규칙 + 함정 규칙 4줄 + **세트 작성 순서** (① 지문 종류와 인물·날짜·금액 표를 먼저 정한다 ② 연계 문제의 근거를 두 지문에 나눠 심는다 ③ 문항을 쓴다 ④ 오답에 지문 단어를 그대로 넣는다 ⑤ 정답이 3연속인지 확인). 문자 체인 형식 규격 (`[10:14] Min-jun Park: …` 줄 단위, 의도 문제 1개 필수).
6. `## 출력 형식` — 훈련 모드 문제 하나의 마크다운 골격을 코드 블록으로 (`**101.** The new … ___ … .` / `(A) …` 네 줄 / Part 7 은 `> ` 인용 지문 + 문항). 그리고 **판정 뒤 해설 골격** (정답 · 유형 · 신호 · 심은 함정 T-번호 · 오답 셋 이유 · 패러프레이징 쌍).
7. `## 진단 세트 · 미니 모의 구성` — init 22문제(Part 5 10: 품사 2 동사 2 준동사 1 전접 2 대명 1 어휘 2 · Part 6 1지문 4 · Part 7 단일 1지문 3 + 이중 1세트 5, 20분) · mock 26문제(Part 5 10 · Part 6 4 · Part 7 12 = 단일 1지문 2 + 이중 5 + 삼중 5, 22분) · 파트 세트(`mock rc p5` 30문제 10분 · `p6` 16문제 8분 · `p7` 단일 2 + 이중 1 + 삼중 1 = 약 17문제 20분).

- [ ] **Step 2: `rc/prescriptions.md`**

머리말: "init 과 debrief 뒤 조수가 여기서 처방을 골라 `my/profile.md` 에 적는다. 점수가 없으면 진단 정답률로 구간을 정한다."

표 (스펙 §8 RC 표 그대로, 열 추가 「진단 정답률」: ~50% / 50~70% / 70~85% / 85%+). 각 구간 아래 세 줄 — 이 구간이 무너지는 자리 · 세션 루틴(문제 수 · 순서) · 졸업 조건(다음 구간으로 가는 기준: 우선 유형 정답률 80% 를 최근 20문제에서).

마지막 절 `## 시간 부족이 약점일 때` — 훈련 모드에선 시간을 안 재니 mock 을 주 1회 · Part 7 "문제 먼저" 강제 · 마지막 15문제 찍는 패턴은 삼중 세트부터 푸는 순서 실험 (mock 에서 두 순서 비교).

- [ ] **Step 3: 검증**

Run: `grep -c 'Directions' rc/generation.md` → 3 이상. `grep -c '^## ' rc/generation.md` → 7. `grep -c '^|' rc/prescriptions.md` → 6 이상.

- [ ] **Step 4: 커밋**

```bash
git add rc/generation.md rc/prescriptions.md
git commit -m "gen : seed : RC 문제 생성 규격서 (난이도 3단계 · 파트별 선지·함정 규칙 · 세트 구성) · 점수대별 처방"
```

---

### Task 8: speaking/format.md · rubric.md · q1-2-read-aloud.md · prescriptions.md

**Files:**
- Create: `speaking/format.md`, `speaking/rubric.md`, `speaking/q1-2-read-aloud.md`, `speaking/prescriptions.md`

**Interfaces:**
- Produces: 문항 코드 `Q3` ~ `Q11` (log.py 문항 열) · 척도 → ○△✗ 환산표 (CLAUDE.md 가 인용).

- [ ] **Step 1: `speaking/format.md`**

스펙 부록 토스 표 (문항 · 유형 · 준비 · 답변 · 척도) + 등급표 (NM/NL 0~50 · NH 60~80 · IL 90~100 · IM 110~130 · IH 140~150 · AL 160~170 · AM 180~190 · AH 200) + "채점은 ETS 원어민 채점관이 녹음을 듣는다 — 이 레포는 타이핑이라 발음·억양을 못 본다" + 출처 링크 (토익스토리 2567 · 1113 · 링커리어 레벨표).

- [ ] **Step 2: `speaking/rubric.md`**

절 1 `## 볼 수 있는 것 / 없는 것` — 표: 잣대 | 타이핑으로 보나 | 어떻게 (발음·억양·강세: ✗ · 문법: ○ · 어휘: ○ · 내용 연관성: ○ · 일관성/구조: ○ · 지속성: ○ 단어 수로).

절 2 `## 분량 = 시간` — 15초 30~35단어 · 30초 60~75 · 60초 130~150. "이보다 20% 이상 짧으면 지속성 부족".

절 3 `## 문항별 채점 표` — Q3-4 · Q5-7 · Q8-10 · Q11 각각: 척도 만점 조건 / △ 조건 / ✗ 조건 (스펙 §6 잣대 표를 문항별로 구체화. Q9 는 "틀린 정보를 정정하지 않으면 ✗", Q10 은 "항목을 빠뜨리면 △", Q11 은 "입장 + 이유 2 + 예시 1 + 마무리 없으면 △").

절 4 `## 척도 → 판정` — Q3-10: 3 ○ · 2 △ · ≤1 ✗ / Q11: 4~5 ○ · 3 △ · ≤2 ✗. 등급 추정 공식 한 줄 (문항 척도 합의 비율로 IM/IH/AL 구간 추정, "발음 제외" 표기 필수).

절 5 `## 자주 걸리는 문법` — 표 10줄 (시제 일관 · 3인칭 단수 · 관사 · 가산/불가산 · 전치사 in/on/at · 비교급 · 같은 동사 반복 · 문장 안 끝남 · 접속사 없이 두 절 · because 뒤 절).

- [ ] **Step 3: `speaking/q1-2-read-aloud.md`**

"조수가 채점하지 않는다. 자습." 한 줄. 표시법 (강세 **굵게** · 끊어읽기 `/` · 연음 `‿` · 올림/내림 `↗ ↘`) · 지문 종류 셋 (광고 · 안내방송 · 뉴스/일기예보) 각각 40~60단어 예시 1개를 표시해서 · 자기 점검 목록 5개 (열거 억양 올림-올림-내림 · 고유명사 · 숫자 · 의문문 끝 · 45초 안에 끝났나).

- [ ] **Step 4: `speaking/prescriptions.md`**

스펙 §8 토스 표 + 각 단계 아래: 무너지는 자리 · 세션 루틴 (문항 순서와 수 — 경험 없음: Q5-7 2세트 + Q8-10 1세트 / IM→IH: Q11 1 + Q8-10 1 + Q7 1 / IH→AL: Q11 2 + Q9·Q10) · 졸업 조건 (해당 문항 두 세션 연속 ○).

- [ ] **Step 5: 검증**

Run: `grep -c '^|' speaking/format.md` → 12 이상. `grep -c '^## ' speaking/rubric.md` → 5. `grep -c '/' speaking/q1-2-read-aloud.md` → 20 이상.

- [ ] **Step 6: 커밋**

```bash
git add speaking/format.md speaking/rubric.md speaking/q1-2-read-aloud.md speaking/prescriptions.md
git commit -m "speaking : seed : 형식 · 채점 잣대(타이핑 한계 명시 · 분량=시간 · 척도→판정) · Q1-2 자습 · 단계별 처방"
```

---

### Task 9: speaking/templates/*.md (v0) · speaking/generation.md

**Files:**
- Create: `speaking/templates/q3-4-picture.md`, `speaking/templates/q5-7-questions.md`, `speaking/templates/q8-10-table.md`, `speaking/templates/q11-opinion.md`, `speaking/generation.md`

**Interfaces:**
- Produces: 문항별 뼈대 v0 (CLAUDE.md 가 "v0 는 남이 쓴 것, 내 말로 다시" 로 가리킨다) · 재료 생성 규격.

- [ ] **Step 1: 웹 조사 (20분 한도)**

WebSearch: `"토익스피킹 파트2 사진묘사 템플릿 순서 장소 중심인물 배경"`, `"토익스피킹 파트3 5-7번 답변 템플릿 15초 30초 이유"`, `"토익스피킹 파트4 8-10번 표 문제 템플릿 정정 나열 일정표"`, `"토익스피킹 파트5 11번 의견 템플릿 60초 구조 이유 예시"`. 얻을 것 — **뼈대의 순서와 상투 표현**. 특정 강사의 문장을 통째로 옮기지 않는다. 공통된 뼈대만 추리고 문장은 새로 쓴다.

- [ ] **Step 2: 템플릿 4파일 공통 구조**

각 파일: 머리말 ("v0 는 남이 쓴 뼈대다. 내 문장으로 다시 써서 `my/speaking/templates.md` 에 v1 을 쌓는다") → `## 뼈대` (순서 번호 + 각 단계 한 줄 역할) → `## v0 표현` (단계별 영어 문장 2~3개씩, 빈칸 `___` 로) → `## 예시 답 1개` (조수가 새로 쓴 장면/상황에 대한 완성 답, 단어 수 표기) → `## 흔한 ✗` (3~5개).

- q3-4: 뼈대 5단계 — 장소 → 중심 인물(동작·옷) → 주변 인물 → 배경·소품 → 느낌/추측. 30초 = 60~75단어. 예시 답은 Task 9 Step 4 의 장면 카드 하나로.
- q5-7: Q5·Q6 "직답 + 한 마디 덧붙임" (30단어), Q7 "입장 → 이유 1 → 이유 2 또는 예시 → 마무리" (65단어). 설문 상황 도입 표현 ("Imagine that a marketing firm is doing research…") 을 영어로 그대로.
- q8-10: Q8 "표 기본 정보 두 가지 (날짜·장소·시작 시각)" · Q9 "정정 — I'm afraid that's not correct. Actually, ___" · Q10 "나열 — There are two/three ___. First, ___. Second, ___" (65단어). 표 예시 1개(코드 블록) + 3문항 + 답.
- q11: "입장 → 이유 1 + 설명 → 이유 2 + 예시(내 소재) → 마무리" (140단어). 주제 유형 4가지 (찬반 · 선택 · 장단점 · 셋 중 하나) 각각 첫 문장 표현.

- [ ] **Step 3: `speaking/generation.md`**

절:
1. `## 공통` — 매번 새로 만든다 · 한 세션에 같은 주제 반복 금지 · 문항 코드 Q3~Q11 · 준비 시간 안내 문구 (Q5-7 "바로 쓰세요" · Q8-10 "표를 45초 보고 바로" · Q11 "45초 메모 후").
2. `## Q3-4 장면 카드` — 규격: 장소 1 · 중심 인물 1~2 (동작 · 옷 · 들고 있는 것) · 주변 인물 · 배경 2~3 · 소품 2~3. 실내/실외 · 인원 수 순환. 출력 골격 코드 블록 (`장소: … / 중심: … / 주변: … / 배경: … / 소품: …`). 예시 카드 2개.
3. `## Q5-7 설문 상황` — 주제 20종 목록 · 도입문 규격 · Q5·Q6 는 when/how often/where/what 형 짧은 질문, Q7 은 which/why/would you rather 형. 예시 세트 1개.
4. `## Q8-10 표` — 표 종류 4가지 (회의·행사 일정표 · 이력서 · 컨퍼런스 프로그램 · 청구서/주문서) 각각 필수 열. 코드 블록으로 실제 양식처럼. **Q9 의 틀린 정보를 조수가 질문에 심는 규칙** ("표에는 3 p.m., 질문은 2 p.m. 이라고 잘못 안다"). Q10 은 같은 종류 항목 2~3개를 묻는다. 예시 표 1개 + 3문항.
5. `## Q11 주제` — 30종 목록 (직장 6 · 교육 6 · 기술 6 · 생활 6 · 사회 6) · 형식 4가지 · 출력 골격 (영어 지시문 "Do you agree or disagree with the following statement? … Use specific reasons and examples").
6. `## 판정 뒤 출력 골격` — 척도 점수 · 잣대별 걸린 곳 · 고친 문장 (사용자 문장을 최소 수정) · "다시 쓰세요" 앞에 문항 원문 재게시.

- [ ] **Step 4: 검증**

Run: `ls speaking/templates | wc -l` → 4. 각 템플릿 `grep -c '^## '` → 4. `grep -c '^## ' speaking/generation.md` → 6. 예시 답 단어 수를 `wc -w` 로 재서 규격 안인지 (Q11 예시 130~150).

- [ ] **Step 5: 커밋**

```bash
git add speaking/templates speaking/generation.md
git commit -m "speaking : seed : 문항별 뼈대 v0 4종 · 재료 생성 규격 (장면 카드 · 설문 · 표 · 의견 주제 30종)"
```

---

### Task 10: tutor/playbook.md

**Files:**
- Create: `tutor/playbook.md` (원본 참고 `../interview-prep/tutor/playbook.md`)

- [ ] **Step 1: 작성**

머리말: "CLAUDE.md 가 뼈대, 여기는 사람에게 검증된 살. 사용자별 로그는 `my/tutor-log.md`. 거기서 두 번 ○ 인 것을 여기로 올리는 건 fork 한 사람이 PR 로."

`## 검증됨` — paper-study · interview-prep 에서 2회 이상 효과 본 셋을 이 레포 말로: 한 번에 문제 하나 + 힌트 한 줄 / 틀리면 직접 고쳐주고 다시 풀게 / 낱말 뜻만 풀어주고 답은 안 준다. 각각 원래 어디서 검증됐는지 한 줄.

`## 시도 중` — 이 레포에서 새로 넣은 것: 유형 안 밝히고 내기 · 정답 + 근거 + 함정 세 잣대 · 카드를 변형 문제로 · 약점 60/무작위 40 · 오답 이유를 사용자가 쓰기 · 토스 소재 뱅크 · 단어 수 = 시간.

`## 버린 것` — interview-prep 「버린 것」 이식: 답을 요구하면서 문제를 다시 안 적기 · 여러 문제 한 번에 · "다시 풀어 보세요" 만 · 위치를 뭉뚱그려 지목. 각각 왜 (사용자 말 한 마디 인용은 interview-prep 것 그대로 — "질문이 뭔데").

- [ ] **Step 2: 커밋**

```bash
git add tutor/playbook.md
git commit -m "docs : seed : 튜터 플레이북 — paper-study·interview-prep 검증됨/버린 것 이식, 이 레포의 시도 중 7개"
```

---

### Task 11: CLAUDE.md · .claude/commands/toeic.md

**Files:**
- Create: `CLAUDE.md`, `.claude/commands/toeic.md`

**Interfaces:**
- Consumes: 전 Task 의 파일 경로 · 코드 · T-번호 · 스크립트 CLI.

- [ ] **Step 1: `CLAUDE.md`**

interview-prep 의 CLAUDE.md 를 **골격 참고**하되 내용은 이 스펙 §3~§6, §10~§11 로. 절 번호와 필수 내용:

- 머리말 — "답을 대신 풀어주는 곳이 아니다 … 근거를 말하고, 함정을 짚히고, 다시 푸는 훈련" · 최종 목표 "새 문제·새 함정에도 근거로 답한다" · 두 트랙 · 못 하는 것(LC · 발음).
- `## 0. 사용자 부담은 0` — 스펙 §1.
- `## 1. 절대 규칙 일곱` — 스펙 §3 의 7개, 각각 소제목 + 2~4줄. **§1-5 「매 턴 문제를 다시 적는다」에 골격 코드 블록** (`> **101.** … (A)… (B)… / 고칠 곳 — (1)… (2)…`).
- `## 2. 무엇이 쌓이나` — 표: 자산 | 파일 | 누가 채우나 (프로필 · 풀이 기록 · 카드 · 오답 노트 · 패러프레이징 · 어휘 · 내 템플릿 · 내 소재 · 튜터 로그).
- `## 3. 세션 모드` — `init` · `rc` · `speaking` · `mock rc|speaking` · `debrief` 각각 루프를 코드 블록으로 (스펙 §4 · §5 · §6 · §10).
- `## 4. 세션 여는 법` — 읽는 순서 (`my/progress.md` → `review.py due` → `log.py stats` → `my/profile.md` → `my/sessions/` 최신 → 트랙별: `my/rc/wrong.md` 막힌 자리 / `my/speaking/templates.md` 상태) → 한 줄 알림 → **복습부터** → 문제 하나. `my/` 가 없으면 init 으로 보낸다.
- `## 5. 세션 닫는 법` — 스펙 §11 8단계.
- `## 6. 채점 — RC` — 잣대 셋 표 · 판정 표 · "판정 → 걸린 곳 → 근거(유형 코드 · T-번호 · 카탈로그 절) → 문제 다시 적고 다시" · ✗ 최대 2회 · **Part 7 세트는 문항별로 받고 문항별로 판정**.
- `## 7. 채점 — 토스` — 잣대 · 분량 표 · 척도→판정 · "발음 제외" 표기 · 고친 문장은 사용자 문장 최소 수정.
- `## 8. 힌트 사다리` — RC 4단계 (스펙 §5) · 토스 4단계 (뼈대 번호 → 그 단계 v0 표현 → 첫 문장 같이 → 뼈대 3줄 주고 살 붙이기).
- `## 9. 문제는 규격서대로` — "`rc/generation.md` · `speaking/generation.md` 를 따른다. 문제마다 T-번호를 심는다. 해설은 판정 뒤에만. 기출 금지" + 문제 고르기 (약점 60/무작위 40 · 난이도 승강 조건).
- `## 10. 카드와 복습` — review.py 명령 · 영역 값 · "카드는 변형 문제로 묻는다" · 카드 나오는 자리 셋 · 세션당 2~4장.
- `## 11. 튜터 구조 피드백은 즉시 규칙으로` — interview-prep §10-1 그대로 + "공통 결함이면 CLAUDE.md, 이 사용자 취향이면 `my/tutor-log.md`".
- `## 12. 공개 레포 규칙` — `my/` 는 커밋 안 함 · 커밋은 템플릿 변경 때만 · 형식 `{영역} : {타입} : {무엇}` · 영역·타입 목록 · 트레일러 없음 · 기출·교재 금지.

- [ ] **Step 2: `.claude/commands/toeic.md`**

```markdown
---
description: 토익 튜터 세션을 연다 — 인자 init(진단) / rc / speaking / mock rc|speaking / debrief. 없으면 progress 를 보고 rc·speaking 중 오늘 것을 고른다
---

CLAUDE.md 의 규칙(§1 · §3 · §4 · §6~§9)에 따라 세션을 연다. 사용자가 상황을 설명하게 하지 않는다.

**`my/` 가 없으면** `python3 scripts/init.py` 를 돌리고 `init` 모드로 들어간다. 인자가 무엇이든.

## 인자

- `init` — **진단.** CLAUDE.md §3 init 루프. 점수·목표·시험일·약점을 하나씩 묻고 → RC 진단 22문제(모의 방식, 20분) → 토스 Q7·Q11 → 소재 대여섯 개 → `my/profile.md` · `my/progress.md` 작성. 전부 `log.py add`
- `rc` — **RC 훈련.** §4 순서로 읽고 한 줄 알림 → 복습 카드(변형 문제) → 문제 하나 (`rc/generation.md` 규격, 유형 안 밝힘) → 정답+유형+근거 받기 → §6 채점 → 다시. 2~3문제마다 앞 오답 유형 되묻기
- `speaking` — **토스 훈련.** 복습 → 문항 하나 (`speaking/generation.md`) → 답 → §7 채점 → 다시. ○ 는 `my/speaking/templates.md` 새 버전
- `mock rc [p5|p6|p7]` — **미니 모의** 26문항 22분 (또는 파트 세트). 한 번에, 중간 교정 없음. 답과 걸린 시간을 받아 유형별 정오·문항당 시간·총평·카드
- `mock speaking` — Q3~Q11 풀세트 타이핑. 문항별 척도·추정 등급(발음 제외)·총평
- `debrief` — 실제 시험 점수 입력 → `my/profile.md` · 처방(`rc/prescriptions.md` · `speaking/prescriptions.md`) · `my/progress.md`
- 없으면 — `my/progress.md` 의 「지금 할 일」과 D-day 를 보고 rc / speaking 중 하나를 고르고 그 이유를 한 줄로 말한 뒤 시작

**절대** — 문제를 여러 개 한 번에 주지 않는다 (init · mock 제외). 답을 요구하는 턴에는 문제 원문을 다시 적는다. 해설은 판정 뒤에만.

세션을 닫을 때는 CLAUDE.md §5 — 기록 · 오답 노트 · 카드 · 템플릿 버전 · 로그 · 진도. 템플릿 파일이 바뀌었으면 커밋.
```

- [ ] **Step 3: 검증**

Run: `grep -c '^## ' CLAUDE.md` → 13. `grep -o 'rc/[a-z/0-9-]*\.md\|speaking/[a-z/0-9-]*\.md\|scripts/[a-z]*\.py' CLAUDE.md .claude/commands/toeic.md | sort -u | while read f; do [ -f "$f" ] || echo "MISSING $f"; done` → 출력 없음.

- [ ] **Step 4: 커밋**

```bash
git add CLAUDE.md .claude/commands/toeic.md
git commit -m "rules : seed : CLAUDE.md 튜터 규칙 12절 · /toeic 커맨드 (init·rc·speaking·mock·debrief)"
```

---

### Task 12: README 최종 · 통합 점검

**Files:**
- Modify: `README.md`

- [ ] **Step 1: README 보강**

Task 1 초안에 추가: `## 어떻게 도는가` (매 세션 루프 한 줄 + 인터뷰 레포 README 식 그림) · `## 세 가지 자산` 표 (카탈로그·함정 / 생성 규격서 / 내 기록 `my/`) · `## 레포 구조` (트리, 한 줄 설명) · `## 문제는 어디서 오나` ("조수가 `rc/generation.md` 규격대로 매번 새로 만든다. 기출·교재 없음. 그래서 외워지지 않는다") · `## 규칙은` (CLAUDE.md 링크 · 설계 스펙 링크) · `## 기여` (플레이북 「검증됨」은 자기 `my/tutor-log.md` 에서 두 번 ○ 난 것만 PR).

- [ ] **Step 2: 전체 점검**

Run:
```bash
python3 -m pytest -q
git status --short          # my/ 가 보이지 않아야 한다
grep -rn 'TBD\|TODO\|추후' --include='*.md' . | grep -v docs/superpowers   # 출력 없음
for f in $(grep -rho '`[a-z./0-9-]*\.md`\|`scripts/[a-z]*\.py`' README.md CLAUDE.md | tr -d '`' | sort -u); do [ -f "$f" ] || echo "MISSING $f"; done
```
Expected: 테스트 전부 통과 · status 에 my/ 없음 · TBD 없음 · MISSING 없음.

- [ ] **Step 3: 스펙 §14-4 — 본인 첫 진단은 이 계획 밖**

이 계획은 여기서 끝난다. `/toeic init` 은 사용자와의 세션이다.

- [ ] **Step 4: 커밋**

```bash
git add README.md
git commit -m "docs : seed : README 최종 — 흐름 · 자산 · 구조 · 문제 출처 · 기여 규칙"
```
