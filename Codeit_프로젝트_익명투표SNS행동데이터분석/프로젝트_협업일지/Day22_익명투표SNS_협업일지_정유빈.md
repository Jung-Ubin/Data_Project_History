# Day - 22 협업 일지(고급)

#### 일자: 25-11-12 / 정유빈

---

### 팀원들과 논의한 일

- 보고서 피드백 바탕 개선
- 발표자료 마무리 작업 진행

<br>

## \* 오늘 + 내가 한 일

### 보고서 개선 작업

- 멘토님께 받은 피드백 내용 바탕으로 보고서 구조 개선
  - 보고서 내용이 너무 긺 → 기간적으로 줄이거나, 구조변경이 힘드니 보고서 앞단에서 분석 스토리를 한 번 소개하는 요약 글 필요
  - '약'이란 어림잡은 수치들은 보고서에서 치명적 → 다른 분석 결과들에서도 수치가 딱 떨어지게 조정하여 보고서 내용 개선 필요
  - 발표 및 보고서의 분량이 긴 만큼 중요한 포인트들은 항상 되짚어가면서 강조하기
- 위 포인트들을 주로 개선하여 보고서 마무리 진행

### 발표자료 마무리 작업 진행

- 어제 작업 중이었던 부분 마무리 작업 및 서식 통일 진행
- 보고서에서도 수정했듯이 수치 수정 및 중요 내용 강조 포인트 추가

---

## \* 사용했던 코드

### PrefixSpan 사용하여 3Step 이하 패턴 추출

```python
from prefixspan import PrefixSpan

# 최소 지지도 설정
min_support = 1000

# 이벤트 흐름 데이터를 리스트 형태로 변환
sequences = flow_pattern_search_df['event_flow'].dropna().apply(lambda x: x.split(',')).tolist()

print("Data ready for PrefixSpan")
print(f"Total sessions: {len(sequences):,}")
print(f"Current min_support: {min_support:,}")

ps = PrefixSpan(sequences)
ps.maxlen = 3

# 지지도 기반 패턴 추출 (지지도 내림차순 정렬)
patterns = ps.frequent(min_support)

print("PrefixSpan complete!")
print(f"Found patterns: {len(patterns):,}")
```

<br>

---

## \*문제점

- 보고서와 발표자료를 피드백 바탕으로 개선하려 노력했지만, 놓친 부분이 있을 것 같음

<BR>

## \* 회고

- 보고서 전체의 흐름을 살펴본 뒤, 팀의 방향성과 맞지 않거나 불리하게 해석될 수 있는 내용은 팀원들과 논의 후 수정·삭제하였다.
- 또한 ‘약’ 등의 어림수나 반올림 수치가 보고서의 신뢰도를 떨어뜨릴 수 있음을 배웠고,
- 보고서를 받는 사람 입장에서 이해하기 쉽고 정확하게 작성하는 중요성을 다시 느꼈다.
