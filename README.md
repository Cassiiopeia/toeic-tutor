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
