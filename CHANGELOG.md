# Changelog

**현재 버전:** 0.1.1  
**마지막 업데이트:** 2026-09-09T04:55:42Z  

---

## [0.1.1] - 2026-09-09

**🐛 수정**
- speaking — 상충 블록에서 척도 표 지시를 아래에서 위로 정정
- scripts — Windows cp949 콘솔에서 유니코드 기호 출력이 UnicodeEncodeError 로 죽던 문제
- chore — Windows 에서 경로 구분자 때문에 my.example 파일 검사 테스트가 깨지던 문제
- scripts — review.py 잔재 문구 정리 · 미사용 import 제거
- rules — 최종 리뷰 — 모든 문제 log.py add · t 간격 절반 · Q3-4 준비 45초 · 난이도 자리 · 용어 통일 · README mock 인자
- speaking — 최종 리뷰 — Q11 60초 · Q8 모범답 분량 · Q3-4 준비 45초 · Q7 소재 참조 · 문장 분리 · thank you 연음 제거
- gen — 단일 문자 체인·채팅에 의도 문항 필수
- catalog — 최종 리뷰 — 137 미래완료 강제 · 149 시간 산수 · 114 해설 · 109 중복 · 삽입 미니예시 수 일치 · 179 NOT 유일성
- docs — README 레포 구조 트리에 .gitignore 추가
- rules — 토스 등급 환산 200점 · 분량 부족 판정 문항별 · 난이도 단계 입력(log.md 마지막 10줄)과 저장(progress.md) · rc 루프에 §9 선택 규칙 연결
- catalog — Part 6 예시 133 연결어 근거를 인접 문장으로 · Part 7 예시 180 연계를 두 지문 필수로 재설계
- speaking — 등급 추정 200점 환산 · Q1-2 연음 표시를 자음+모음 규칙에 맞춤
- gen — mock rc Part 5 유형 수 명시(구문 제외 6) · Part 7 세트=문제 하나·문항별 판정 규칙 추가
- catalog — Part 5 예시 106 사역동사 선지 명확화 · 113 해설 최상급 오기 정정

**🔧 변경사항**
- chore : add : project-auto-wizard 로 릴리스 자동화 설치 (main trunk-based · basic · v0.1.0)
- speaking : add : 실전 팁(tips.md) · 시험 전날·당일(exam-day.md) · 채점 항목 누적 구조 · Q11 준비시간 출처 상충 기록
- scripts : add : init 이 .gitignore 개인 자료 줄을 직접 채운다 (my/ · private/ · 루트 pdf·이미지)
- rules : add : 성적표 ABILITIES MEASURED 로 약점 표적 지정 — 항목별 처방이 점수대 처방을 덮는다
- rules : add : init 에 성적표 ABILITIES MEASURED 절차(§3.1) · 조수가 읽어낸 값 사용자 확인 규칙(§3.2)
- docs : seed : README 최종 — 흐름 · 자산 · 구조 · 문제 출처 · 기여 규칙
- rules : seed : CLAUDE.md 튜터 규칙 12절 · /toeic 커맨드 (init·rc·speaking·mock·debrief)
- catalog : seed : Part 6 유형 4 · Part 7 유형 8 — 질문 문구 · 근거 위치 · 예시 세트 · 패러프레이징 20쌍
- speaking : seed : 문항별 뼈대 v0 4종 · 재료 생성 규격 (장면 카드 · 설문 · 표 · 의견 주제 30종)
- speaking : seed : 형식 · 채점 잣대(타이핑 한계 명시 · 분량=시간 · 척도→판정) · Q1-2 자습 · 단계별 처방
- gen : seed : RC 문제 생성 규격서 (난이도 3단계 · 파트별 선지·함정 규칙 · 세트 구성) · 점수대별 처방
- catalog : seed : Part 5 유형 7개 — 신호 · 풀이 순서 · 함정 · 예시 14문제 · 빈출 짝
- docs : seed : 튜터 플레이북 — paper-study·interview-prep 검증됨/버린 것 이식, 이 레포의 시도 중 7개
- scripts : add : log.py — 풀이 기록 add/stats, 유형·함정별 정답률, n≥4·70% 미만 약점
- scripts : seed : review.py 이식 — 저장 my/cards.md, 영역 P5·T-07·Q11
- catalog : seed : RC 형식 · 함정 카탈로그 T-01~T-30 · 유형 코드 정본
- chore : seed : 뼈대 — .gitignore(my/ 제외) · README 초안 · my.example 11파일 · init.py
- docs : seed : 구현 계획 12 Task — 뼈대·스크립트(TDD)·카탈로그·규격서·토스·규칙·README
- docs : seed : toeic-tutor 설계 스펙 — RC·토스 두 트랙, my/ 분리, 유형·함정 카탈로그 + 생성 규격서, log.py 약점 산출

---

