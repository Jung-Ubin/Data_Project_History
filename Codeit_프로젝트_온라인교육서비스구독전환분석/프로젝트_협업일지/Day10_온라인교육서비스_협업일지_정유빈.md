# Day - 10 협업 일지(중급1)

#### 일자: 2025-07-18 / 정유빈

---

### 팀원들과 논의한 일

- 중간 발표 리허설 진행
- 발표 대본 정리 후 중간 발표 및 발표 후 발표관련 피드백 진행
- 앞으로의 분석 방향 및 최종보고서 아이템 논의

---

## \* 오늘 + 내가 한 일

- 발표 후 각 팀원들의 발표관련 피드백 진행 (ex: 이런 부분에선 간단하게 발표 대본을 정리해도 좋을것 같다.)
- CPA 재 분석하여 LTV 재 집계 후 "무료 체험이 정말 회사 입장에서 손해인지" 파악

---

## \* 사용했던 코드

### user_df(구독자 정보(만듬))를 final_df로 변환한 후 LTV 계산, 추가하는 코드

```python
# NaN 처리
final_df['CPA_filled'] = final_df['CPA'].fillna(0)
final_df['LTR_filled'] = final_df['LTR'].fillna(0)

# 무료 체험 여부: trial_start_time 존재 여부로 판단
final_df['LTV'] = np.where(
    final_df['trial_start_time'].notna() & (final_df['LTR_filled'] > 0),
    final_df['LTR_filled'] - final_df['CPA_filled'],  # 무료 체험 + 구독
    np.where(
        final_df['LTR_filled'] > 0,
        final_df['LTR_filled'],                        # 비체험 구독
        -final_df['CPA_filled']                        # 무료 체험만 (구독 X → 손실)
    )
)

# 임시 컬럼 정리
final_df.drop(columns=['CPA_filled', 'LTR_filled'], inplace=True)

# 확인
print(final_df[['user_id', 'trial_start_time', 'LTR', 'CPA', 'LTV']].head())

```

<br>

---

<br>

## \* 문제점

- 위 분석으로 인해 "무료 체험이 정말 회사 입장에서 손해" 라는 안이 데이터 상으로 가능성이 있다고 판단
- 그래서 "무료 체험자의 전환률은 비 체험자보다 3배 이상 높지만 경제적인 이득으로는 손해"로 결론이 나서  
  이 상황에서 어떤 아이디어를 내야할 지 고민해봐야 함

---

## \* 회고

- 위 분석을 통해 새로운 아이디어를 생각하여 무료 체험을 다시 제안할 수 있는 인사이트를 확보를 새 분석 목적으로 삼음
- 분석 과정 중 머리가 복잡해져서 갑자기 진행이 안됐었음 → 계속 복잡하게 생각하지말고, 최대한 쉽게 할 수 있는 부분부터  
  차근차근 진행하여 해결하자
