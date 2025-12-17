# Day - 15 협업 일지(중급1)

#### 일자: 2025-07-25 / 정유빈

---

### 팀원들과 논의한 일

- 최종 보고서 / 발표 자료 보완 및 발표 대본 작성 준비

## \* 오늘 + 내가 한 일

- 최종 보고서 마무리 작업 및 멘토링 시간 피드백 내용 적용
- 서식 재 수정 및 발표 자료 제작

---

## \* 사용했던 코드

### 타임 로그 datetime 형식으로 변형

```python
# 시간 컬럼(datetime)으로 변환
complete_df['client_event_time'] = pd.to_datetime(complete_df['client_event_time'])
trial_df['client_event_time'] = pd.to_datetime(trial_df['client_event_time'])
cancel_df['client_event_time'] = pd.to_datetime(cancel_df['client_event_time'])
```

<br>

---

<br>

## \* 문제점

- 최종 보고서의 절반 부분이 노션버그로 날아가는 이슈 발생  
  → 백업 자료로 해결 후 다시 서식 맟춰서 작성

- 아직 최종 보고서 및 발표 자료를 완료하지 못한 팀원발생  
  → 마무리 작업과 작성 과정에서 지원하여 해결

---

## \* 회고

- 팀으로 같은 방향성으로 분석을 진행했지만, 작성 방향은 각기 다 달라서  
  서식을 맟추는데 시간이 꽤 걸렸다.  
  아직 그 부분(보고서 서식)에 대해선 미완인 부분이기 때문에 다음주 마무리를 잘 맺어야 될거같다.
