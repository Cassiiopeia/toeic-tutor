# RC 문제 생성 규격서

이 파일이 조수를 묶는다. 없으면 쉬운 문제만 나온다.
문제와 해설을 같이 주지 않는다 — 해설은 사용자가 판정을 받은 뒤에만 §6 골격으로 연다.
기출·교재를 옮기지 않는다 — 실제 기출 문제·교재 문제·그 변형을 쓰지 않고, 형식(번호 체계·선지 구성·함정 자리)만 따라 매번 새 문장·새 지문을 쓴다.

## 공통

1. 문제 번호는 실제 시험대로 매긴다 — Part 5 101~130 · Part 6 131~146 · Part 7 147~200. 세트 맨 앞에 그 파트의 Directions 원문을 붙인다.
2. 지문은 인용문(`>`)이나 코드 블록으로 원문 그대로 보여준다. 선지는 항상 (A) (B) (C) (D) 넷.
3. 정답 알파벳 분포를 고르게 섞는다 — 같은 글자가 3연속으로 정답이면 그 세트는 다시 만든다.
4. 문제마다 심을 함정을 `rc/traps.md` 의 T-번호로 조수가 먼저 정해 둔다(하나 이상). 문제를 낼 때는 밝히지 않고, 판정 뒤 해설(§6)에서 공개한다. 함정 없는 문제는 내지 않는다 — 기본 난이도(§2)만 예외로 0개를 허용한다.
5. 비즈니스 맥락 9종을 돌려 쓴다 — 사무 · 인사 · 마케팅 · 물류 · 재무 · 행사 · 부동산 · 여행 · 고객 서비스. (Part 7 지문 종류 9가지와는 다른 축이다 — 맥락은 "무슨 업무 이야기인가", 지문 종류는 "어떤 문서 형식인가".)
6. 실제 기출 · 교재 문제 · 그 변형을 쓰지 않는다. 형식만 재현한다.
7. 문제와 해설을 같이 주지 않는다 — 사용자가 답하고 판정을 받은 뒤에만 해설을 연다.

### Part 5 Directions (형식 재현용)

```
Directions: Each sentence below has one blank. Four choices follow the sentence.
Choose the option that best completes the sentence, then mark (A), (B), (C), or (D).
```

### Part 6 Directions (형식 재현용)

```
Directions: Read each passage below. Some words, phrases, or sentences are
missing from the passage. Four choices are given for every blank. Pick the
option that fits the passage as a whole, then mark (A), (B), (C), or (D).
```

### Part 7 Directions (형식 재현용)

```
Directions: You will read a set of passages — letters, notices, articles,
message chains, and similar texts. One or more passages are followed by
several questions about them. Choose the response that answers each
question most accurately, then mark (A), (B), (C), or (D).
```

## 난이도 3단계

| 단계 | Part 5 | Part 6 | Part 7 |
|---|---|---|---|
| 기본 | 신호가 빈칸 바로 옆에 있음 · 함정 0~1개 | 신호가 빈칸이 든 문장 안에서 끝남 · 함정 0~1개 | 단일 지문 150단어 이하 · 연계 없음 |
| 실전 | 수식어(구·절)로 신호를 가림 · 함정 1~2개 | 신호가 앞 문장으로 이동(시제·지시어) · 함정 1~2개 | 이중 지문 등장 · 연계 1개 |
| 고난도 | 함정 2개 이상 · 어휘 문제는 뜻이 비슷한 선지 3개 | 신호가 앞 문단 전체에 걸침 · 함정 2개 이상 | 삼중 지문 500단어 이상 · 연계 2개 |

단계는 세션 전체에 하나로 적용한다. 직전 10문제(파트 무관) 정답률이 80% 이상이면 한 단계 올리고, 60% 미만이면 한 단계 내린다. 기본 아래로는 내려가지 않고 고난도 위로는 올라가지 않는다.

## Part 5

문장 길이는 12~25단어. 한 세션 안에서 같은 유형을 연속 3개 내지 않는다 — 단, 약점 반복 훈련(특정 유형만 모아 푸는 세션)일 때는 예외로 연속을 허용한다.

| 유형 | 선지 구성 규칙 | 필수 함정 |
|---|---|---|
| 품사 자리 | 같은 어근 4형태(명사·동사·형용사·부사) | 형태만 비슷한 오답(T-01) · 명사 선지가 둘이면 사람/사물 구분(T-02) |
| 동사(수일치·시제·태) | 같은 동사의 4형태 | 주어·동사 사이에 긴 수식어(T-04) · 시간 단서를 문장 끝에(T-05) · 태를 물으면 목적어 유무로 가르기(T-06) |
| 준동사 | to부정사 · 동명사 · 분사 · 원형 | 앞 동사가 정하는 목적어 형태 — enjoy -ing vs decide to(T-08) |
| 전치사 vs 접속사 | 전치사 2 + 접속사 2 | 뜻은 같고 자리가 다른 짝 — despite/although · during/while(T-07) |
| 대명사 · 관계사 | 격 4형태 또는 관계사 4개 | 선행사가 사람/사물인지(T-10) · 재귀·소유대명사(T-09) |
| 어휘 | 같은 품사 4개, 그중 2개는 뜻이 비슷 | 뜻은 맞지만 연어(collocation)가 틀림(T-11) · 비슷한 뜻 어휘 쌍(T-12) |
| 비교 · 도치 · 병치 | 구문 4형태 | 필수 없음(기본 난이도 예외) — 비교급/최상급을 물을 때는 T-15 를 심는다 |

log.py 유형 코드는 표 순서대로 `품사` · `동사` · `준동사` · `전접` · `대명` · `어휘` · `구문` 이다(`rc/traps.md` 유형 코드 표와 동일).

## Part 6

지문 종류는 이메일 · 공지 · 기사 · 광고 · 회람 · 편지 여섯 가지. 4지문에 종류가 겹치지 않게 고른다. 지문 하나는 80~130단어.

빈칸 4개 = 문법 1(`P6-문법`) + 어휘 1(`P6-어휘`) + 연결어/시제 1(`P6-연결`) + 문장 삽입 1(`P6-삽입`).

- 시제 문제는 빈칸이 든 문장만 봐서는 못 풀게 만든다 — 앞 문장이나 지문 상단 날짜에 시점을 심고, 빈칸 문장에는 시간 단서를 두지 않는다(T-18).
- 연결어 문제는 빈칸 문장만 읽으면 아무 연결어나 말이 되게 쓴다 — 앞뒤 문장의 관계(뒤집기/이어가기/덧붙이기)를 봐야만 방향이 정해지게 한다(T-17).

문장 삽입 선지 4개 작성 규칙:

- 4개 모두 지문 주제와 관련된 문장으로 만든다 — 화제만 보고는 못 고르게 한다(T-16).
- 정답 선지는 반드시 앞 문장에 나온 명사를 대명사나 `the + 명사`로 받는다.
- 오답 하나는 시제가 앞 문장과 어긋난다(T-18).
- 오답 하나는 연결어(however/therefore 류)의 방향이 반대다(T-17).
- 오답 하나는 지시어(this/these/it)가 가리킬 대상이 앞에 없거나 수가 안 맞는다(T-19).

## Part 7

| 구성 | 번호 | 문항 | 단어 수 |
|---|---|---|---|
| 단일 10지문 | 147~175 | 지문당 2~4 | 100~300 |
| 이중 2세트 | 176~185 | 세트당 5 | 합 300~450 |
| 삼중 3세트 | 186~200 | 세트당 5 | 합 400~600 |

지문 9종 — 이메일 · 문자 메시지 체인 · 공지 · 광고 · 기사 · 양식(신청서·설문) · 일정표 · 청구서/영수증 · 온라인 채팅. 이중·삼중 세트 안에서는 종류를 섞는다(예: 이메일 + 일정표 + 답장 이메일).

문제 유형 조합 규칙:

- 단일 지문(2~4문항)은 지문이 하나뿐이라 연계가 불가능하다 — 세부 · 추론 · NOT · 동의어 · 삽입위치 · 목적 중에서 채우고, NOT/EXCEPT 는 지문당 최대 1개.
- 이중·삼중 세트(5문항)는 연계 최소 1개(`연계`, 두 지문을 합쳐야만 풀림) + 동의어 1개(`동의어`) + 추론 1개(`추론`) + NOT/EXCEPT 최대 1개(`NOT`)를 넣고, 남는 자리는 세부(`세부`) · 목적(`목적`) · 삽입위치(`삽입위치`) 중에서 채운다.
- 세트 지문에 문자 메시지 체인이나 온라인 채팅이 섞이면 의도 문제(`의도`) 1개를 반드시 넣는다 — 남는 유형 자리 하나를 대신한다.

함정 규칙:

1. 오답 선지에는 지문 단어를 그대로 재사용하고, 정답은 패러프레이즈한다(T-20).
2. 비슷한 이름·날짜·금액을 지문 안에 둘 이상 등장시킨다(T-22).
3. 연계 문제의 근거는 반드시 서로 다른 지문에 나눠 심는다(T-23).
4. NOT 문제의 세 오답은 지문 여러 곳에 흩어 놓는다(T-24).

세트 작성 순서:

① 지문 종류와 등장인물 · 날짜 · 금액 표를 먼저 정한다 — 뒤섞을 값들을 미리 확정해야 함정 규칙 2번(T-22)을 심을 자리가 생긴다.
② 연계 문제의 근거를 두 지문에 나눠 심는다.
③ 문항을 쓴다.
④ 오답에 지문 단어를 그대로 넣는다.
⑤ 정답이 3연속인지 확인한다 — 3연속이면 선지 순서를 다시 섞는다.

문자 메시지 체인 형식 규격:

- 한 줄에 발화 하나. `[HH:MM] 이름: 내용` 형식을 지킨다 — 예: `[10:14] Min-jun Park: Are you still at the printer?`
- 발화자는 2~4명, 시각은 위에서 아래로 순서대로 올라간다.
- 의도 문제 1개는 반드시 넣는다. 질문 형식은 `At [HH:MM], what does [이름] most likely mean when she/he writes "..."?` 로 하고, 정답 근거는 그 발화 바로 앞뒤 줄에서만 찾을 수 있게 만든다(T-28).
- 온라인 채팅도 같은 줄 단위 형식을 쓴다. 참여자가 3명 이상이면 그룹 채팅으로 표기한다.

## 출력 형식

### 문제 골격

Part 5 (문제 하나):

```
**101.** The new logistics manager will ___ all delivery schedules for the regional warehouse starting next month.

(A) oversee
(B) oversight
(C) overseen
(D) overseeing
```

Part 6 (한 세트 4문항, 마지막이 문장 삽입):

```
**Questions 131-134 refer to the following notice.**

> All staff members are asked to submit expense reports by the last day of
> each month. The finance team ___(131)___ every report within five
> business days of receiving it. ___(132)___, any report that is missing a
> receipt will be sent back for revision. Employees who file a ___(133)___
> report on time avoid delays in reimbursement. ___(134)___

**131.**
(A) review
(B) reviews
(C) reviewing
(D) to review

**132.**
(A) However
(B) Therefore
(C) For example
(D) In addition

**133.**
(A) completely
(B) completed
(C) completion
(D) complete

**134.**
(A) The finance team meets every Monday morning to plan new projects.
(B) This process keeps year-end records accurate.
(C) New employees receive a separate onboarding packet.
(D) The office will be closed for the national holiday.
```

Part 7 (단일 지문 한 세트):

```
**Questions 147-149 refer to the following e-mail.**

> From: Dana Reyes
> To: All Staff
> Subject: Monthly Supply Order
>
> Hello team,
>
> Our monthly supply order will be placed this Friday. Please send any
> requests for printer paper, pens, or folders to the front desk by
> Thursday at noon. Requests received after the deadline will be added to
> next month's order instead.
>
> Thank you,
> Dana

**147.** What is the purpose of the e-mail?
(A) To announce a new supplier
(B) To request supply orders before a deadline
(C) To cancel a scheduled delivery
(D) To introduce a new staff member

**148.** By when should requests be sent?
(A) Monday
(B) Wednesday
(C) Thursday
(D) Friday

**149.** What will happen to a late request?
(A) It will be rejected.
(B) It will be placed the same week.
(C) It will be moved to the following month.
(D) It will be sent to a different office.
```

### 해설 골격 (판정 뒤에만 연다)

```
정답: (A) oversee
유형: 품사
신호: 조동사 will 뒤 + 빈칸 뒤에 목적어(all delivery schedules)가 있어 능동 동사 원형 자리
심은 함정: T-01
오답 셋 이유:
(B) oversight 는 명사라서 will 뒤 동사 자리에 올 수 없다
(C) overseen 은 과거분사로 수동형에나 쓰이는데 목적어가 남아 있어 능동이 필요하다
(D) overseeing 은 동명사/분사라 will 뒤에 단독으로 오지 못한다
패러프레이징 쌍: — (Part 7 문제에서만 채운다. 예: for free → complimentary)
```

`유형` 필드는 `rc/traps.md` 유형 코드 표의 코드만 쓴다 — Part 5: `품사` `동사` `준동사` `전접` `대명` `어휘` `구문` / Part 6: `P6-문법` `P6-어휘` `P6-연결` `P6-삽입` / Part 7: `세부` `추론` `NOT` `동의어` `삽입위치` `의도` `목적` `연계`.

## 진단 세트 · 미니 모의 구성

### init 진단 — 22문제, 20분

- Part 5 10문제 — 품사 2 · 동사 2 · 준동사 1 · 전접 2 · 대명 1 · 어휘 2 (구문 유형은 넣지 않는다)
- Part 6 1지문 4문항
- Part 7 8문항 — 단일 1지문 3문항 + 이중 1세트 5문항

합계 10 + 4 + 8 = 22문항, 20분.

### mock rc — 26문제, 22분

- Part 5 10문제 (Part 5 표의 6개 유형을 고르게 순환, 같은 유형 3연속 금지)
- Part 6 4문항 (1지문)
- Part 7 12문항 — 단일 1지문 2문항 + 이중 1세트 5문항 + 삼중 1세트 5문항

합계 10 + 4 + 12 = 26문항, 22분.

### 파트 세트 (`mock rc p5` · `p6` · `p7`)

- `mock rc p5` — 30문제, 10분 (실제 시험 Part 5 전체 분량)
- `mock rc p6` — 16문제, 8분 (4지문 × 4문항, 실제 시험 Part 6 전체 분량)
- `mock rc p7` — 단일 2지문(지문당 2~4문항) + 이중 1세트(5문항) + 삼중 1세트(5문항), 총 약 17문항, 20분
