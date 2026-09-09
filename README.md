# toeic-tutor

토익 RC 와 토익스피킹을 **문제 풀이 → 근거 말하기 → 직접 교정 → 다시 → 카드 → 복습** 으로 훈련하는 Claude Code 튜터.
clone 해서 `/toeic init` 한 번이면 자기 수준에 맞게 시작한다.

## 하는 것 / 못 하는 것

- **RC(Reading)** — Part 5·6·7. 조수가 매번 새 문제를 만들고, 답이 아니라 **근거**를 채점한다.
- **토익스피킹** — Q3~Q11 을 **타이핑**으로. 내용·구조·문법·어휘·분량을 본다.
- 못 하는 것 — **리스닝 없음. 발음·억양 없음.** 조수가 소리를 못 낸다.

## 약점은 어떻게 찾나

**"어느 파트에서 틀리는지" 는 느낌으로 못 짚는다.** 측정값이 있으면 측정값이 이긴다. `/toeic init` 이
셋 중 쓸 수 있는 것을 위에서부터 찾는다.

| 순위 | 자료 | 무엇을 주나 | 한계 |
|---|---|---|---|
| **1** | **공식 성적표 ABILITIES MEASURED** | RC·LC 다섯 항목의 정답률 + **같은 회차 응시자 평균** | 최근 2년 안에 응시한 사람만. PDF 를 조수에게 줘야 한다 |
| **2** | 무료 온라인 레벨테스트 | 실제 형식 50문항(LC 25 + RC 25)의 파트별 분석 | 사설이라 ETS 환산·항목 분류와 다르다. 정답률만 주고 근거는 안 본다 |
| **3** | 조수가 내는 진단 22문제 | **근거를 말하게 해서 왜 틀리는지** 본다 | 표본이 작아 정답률 신뢰도는 낮다 |

1·2 는 *무엇이* 약한지를, 3 은 *왜* 틀리는지를 잰다. **서로 대체재가 아니라 보완재다** — 성적표로 표적을
정하고, 그 표적 유형으로 조수가 문제를 내서 근거 대는 방식을 본다.

성적표가 있으면 조수가 파싱해 표로 보여주고 **확인을 받은 뒤** `rc/prescriptions.md` 의 **항목별 처방**으로
표적을 정한다. 이게 점수대 처방을 덮는다 — 점수대 표는 "그 점수대 사람이 *대체로* 어디서 무너지나" 의
평균값이라, 개인 항목값과 어긋나면 개인값이 이긴다.

## 어떻게 도는가

매 세션 루프 한 줄 — **복습 카드 → 문제 하나 → 정답+유형+근거 → 판정(정답·근거·함정) → 틀리면 다시 → 카드.**

```
   성적표 있음 ──→ ABILITIES MEASURED 로 표적 지정 (빠르고 정확)
                          │
   성적표 없음 ──→ 진단 22문제
                          │
                          ▼
   init ──→ rc · speaking (매일 하나씩) ──→ mock (시험 직전) ──→ debrief (시험 뒤)
                          ▲                                            │
                          └────────── 처방(prescriptions) 갱신 ─────────┘

   매 세션: 복습 카드 → 문제 하나 → 정답+유형+근거 → 판정(정답·근거·함정) → 다시 → 카드
   시험 직전: mock (세트 한 번에, 중간 교정 없음, 끝에 총평)
```

## 세 가지 자산

| 자산 | 어디 | 무엇 |
|---|---|---|
| **카탈로그 · 함정** | `rc/catalog/` · `rc/traps.md` | 유형별 신호·풀이 순서·함정(T-번호). 채점의 근거 |
| **생성 규격서** | `rc/generation.md` · `speaking/generation.md` | 조수가 매번 새 문제를 만드는 기준. 이게 없으면 쉬운 문제만 나온다 |
| **내 기록** | `my/` | 프로필·진도·풀이 기록·오답 노트·내 템플릿·카드. gitignore, 로컬에만 |

## 문제는 어디서 오나

조수가 `rc/generation.md`(RC) · `speaking/generation.md`(토스) 규격대로 매번 새로 만든다. 기출·교재 없음. 그래서 외워지지 않는다.

## 시작

```bash
git clone <this repo> && cd toeic-tutor
claude
```

파이썬 3 이 필요하다 (표준 라이브러리만 쓴다). **Windows 에서는 `python3` 가 Microsoft Store 스텁이라
아무 출력 없이 끝난다** — 그 환경에서는 `python` 으로 부른다. 조수가 세션 첫 스크립트 전에 확인한다.

```
/toeic init            점수 · 목표 · 성적표(있으면) · 진단 22문제 · 토스 2문항 · 소재 캐기
/toeic rc              RC 훈련 — 복습 카드 먼저, 문제 하나씩
/toeic speaking        토스 훈련
/toeic mock rc [p5|p6|p7]   미니 모의 (26문항 22분 · 또는 파트 세트)  ·  /toeic mock speaking
/toeic debrief         실제 시험 뒤 점수 입력
/toeic                 인자 없으면 progress 를 보고 rc·speaking 중 오늘 것을 고른다
```

## 레포 구조

```
toeic-tutor/
├── CLAUDE.md                     튜터 규칙 — 절대 규칙 일곱 · 채점 잣대 · 세션 모드
├── README.md                     이 파일
├── .gitignore                    my/ 전체 제외 (+ 파이썬·OS·IDE)
├── .claude/commands/toeic.md     /toeic init · rc · speaking · mock rc|speaking · debrief
├── rc/
│   ├── format.md                 75분 100문항 형식 · 파트별 문항 번호 · 시간 배분
│   ├── catalog/part5.md          Part 5 유형별 신호 · 풀이 순서 · 함정(T-번호) · 예시
│   ├── catalog/part6.md          Part 6 지문 종류 × 빈칸 유형
│   ├── catalog/part7.md          Part 7 지문 종류 × 문제 유형 · 연계 규칙
│   ├── traps.md                  함정 카탈로그 T-01… (채점 근거 번호)
│   ├── generation.md             문제 생성 규격서 · 해설 골격
│   └── prescriptions.md          RC 처방 — 성적표 항목별(우선) · 점수대별(대체)
├── speaking/
│   ├── format.md                 11문항 · 준비/답변 시간 · 척도 · 등급표
│   ├── onboarding.md             ★ 토스가 처음이면 여기부터 — 무슨 시험인지 · 11문항 흐름 · 어디서 갈리나
│   ├── rubric.md                 채점 잣대 — 타이핑으로 볼 수 있는 것 / 없는 것
│   ├── tips.md                   실전 팁 — 직답 우선 · 이유 은행 · 문항별 공략 · 연습법
│   ├── exam-day.md               시험 전날 · 당일 절차 · 최종 체크리스트
│   ├── templates/                문항별 뼈대 v0 (남이 쓴 것 — 공개 자료 종합)
│   ├── q1-2-read-aloud.md        Q1-2 자습용 — 강세·끊어읽기 표시. 조수가 채점하지 않는다
│   ├── generation.md             장면·설문·표·의견 생성 규격서 · 판정 뒤 출력 골격
│   └── prescriptions.md          경험 없음 → IM → IH → AL 처방
├── tutor/playbook.md             검증된 튜터 방식 (공통 — 검증된 것만 PR 로 보탠다)
├── scripts/
│   ├── init.py                   my/ 뼈대 생성 (my.example/ 복사)
│   ├── review.py                 복습 카드 — due · add · grade · list · stats
│   └── log.py                    풀이 기록 — add · stats (유형·함정별 약점 판정)
├── tests/                        test_init.py · test_log.py · test_review.py
├── version.yml                   현재 버전 (릴리스 워크플로우가 갱신 — 손대지 않는다)
├── .github/workflows/            릴리스 발행 · README 버전 갱신 · PR 요약 · 이슈 도우미
├── .github/scripts/              위 워크플로우가 쓰는 스크립트
├── my.example/                   init 결과의 모양 (커밋됨) — my/ 와 같은 파일 구성
├── docs/superpowers/             specs/ 설계 스펙 · plans/ 구현 계획
└── my/                           ★ 내 기록 (gitignore) — init 이 만든다
```

## 내 기록은 어디에

`my/` 에만 쌓이고 git 에 올라가지 않는다. 성적표 PDF·점수 캡처처럼 조수에게 주는 개인 파일은 `private/`
에 둔다. 둘 다 `.gitignore` 가 막고, 루트에 떨어진 `*.pdf` · `*.png` 도 함께 막는다.

**`scripts/init.py` 가 이 줄들을 직접 채운다.** 이 레포는 공개라 개인 파일이 한 번 커밋되면 그대로
공개된다 — 사용자가 `.gitignore` 를 손볼 일이 없게 init 이 매번 확인하고, 빠진 줄만 넣는다.

## 규칙은

전체 규칙은 [`CLAUDE.md`](CLAUDE.md), 설계 배경은
[`docs/superpowers/specs/2026-09-08-toeic-tutor-design.md`](docs/superpowers/specs/2026-09-08-toeic-tutor-design.md).

## 기여

`tutor/playbook.md`(공통 플레이북)에 새 방식을 올리려면 먼저 자기 `my/tutor-log.md` 에서 **같은 시도가
두 번 ○** 인지 확인한다. 검증된 것만 PR 로 올린다. 카탈로그·함정·규격서·스크립트를 고치는 PR 도 실제
기출 문제를 옮기지 않는다 — 형식만 재현한다.

---

<!-- AUTO-VERSION-SECTION: DO NOT EDIT MANUALLY -->
## 최신 버전 : v0.1.0 (2026-09-09)

[전체 버전 기록 보기](CHANGELOG.md)
