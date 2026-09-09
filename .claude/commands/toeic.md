---
description: 토익 튜터 세션을 연다 — 인자 init(진단) / rc / speaking / mock rc|speaking / debrief. 없으면 progress 를 보고 rc·speaking 중 오늘 것을 고른다
---

CLAUDE.md 의 규칙(§1 · §3 · §4 · §6~§9)에 따라 세션을 연다. 사용자가 상황을 설명하게 하지 않는다.

**`my/` 가 없으면** `python3 scripts/init.py` 를 돌리고 `init` 모드로 들어간다. 인자가 무엇이든.
(Windows 는 `python scripts/init.py` — `python3` 는 스텁이라 조용히 실패한다. CLAUDE.md §0)

## 인자

- `init` — **진단.** CLAUDE.md §3 init 루프. 점수·목표·시험일·약점을 하나씩 묻고 → **성적표가 있으면 PDF 를 받아 ABILITIES MEASURED 를 읽고(§3.1) 값을 확인받는다(§3.2) — 이러면 진단 22문제를 건너뛴다** → 없으면 RC 진단 22문제(모의 방식, 20분) → 토스 Q7·Q11 → 소재 대여섯 개 → `my/profile.md` · `my/progress.md` 작성. 전부 `log.py add`
- `rc` — **RC 훈련.** §4 순서로 읽고 한 줄 알림 → 복습 카드(변형 문제) → 문제 하나 (`rc/generation.md` 규격, 유형 안 밝힘) → 정답+유형+근거 받기 → §6 채점 → 다시. 2~3문제마다 앞 오답 유형 되묻기
- `speaking` — **토스 훈련.** 복습 → 문항 하나 (`speaking/generation.md`) → 답 → §7 채점 → 다시. ○ 는 `my/speaking/templates.md` 새 버전
- `mock rc [p5|p6|p7]` — **미니 모의** 26문항 22분 (또는 파트 세트). 한 번에, 중간 교정 없음. 답과 걸린 시간을 받아 유형별 정오·문항당 시간·총평·카드
- `mock speaking` — Q3~Q11 풀세트 타이핑. 문항별 척도·추정 등급(발음 제외)·총평
- `debrief` — 실제 시험 점수 입력 (+ 성적표가 있으면 §3.1 로 항목별 정답률 갱신) → `my/profile.md` · 처방(`rc/prescriptions.md` 항목별 우선 · `speaking/prescriptions.md`) · `my/progress.md`
- 없으면 — `my/progress.md` 의 「지금 할 일」과 D-day 를 보고 rc / speaking 중 하나를 고르고 그 이유를 한 줄로 말한 뒤 시작

**절대** — 문제를 여러 개 한 번에 주지 않는다 (init · mock 제외). 답을 요구하는 턴에는 문제 원문을 다시 적는다. 해설은 판정 뒤에만.

세션을 닫을 때는 CLAUDE.md §5 — 기록 · 오답 노트 · 카드 · 템플릿 버전 · 로그 · 진도. 템플릿 파일이 바뀌었으면 커밋.
