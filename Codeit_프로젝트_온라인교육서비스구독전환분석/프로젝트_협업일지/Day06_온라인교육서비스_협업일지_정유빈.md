# Day - 6 협업 일지(중급1)

#### 일자: 2025-07-14 / 정유빈

---

### 팀원들과 논의한 일

- 유저별 `complete.subscription` 로그 중복 발생 문제 공유
- `click.cancel_plan_button` 로그와의 시간 관계 검토 필요성 인식
- 분석 신뢰도 향상을 위해 **팀원 각자의 분석 방식 피드백 및 수정 방향 제안**

---

## \* 오늘 + 내가 한 일

- `user_df` 최종 정제 및 사용자별 결제-취소 흐름 기반 `plan_type`, `plan_price`, `subscription_months` 설정 완료

  - 당일 취소자/취소 이력 없는 유저/중간 해지 유저 등 세부 조건에 따라 분기 처리
  - `plan_type` 및 `plan_price`를 `.apply()` 기반 함수로 자동 채움 (강사님이 도와주심(python 또 까먹어서 공부 필요))

- **LTR 계산 방식 고도화**

  - 1개월 플랜: 개월 수 × 15,920원
  - 12개월 플랜:
    - 12개월 이하 사용 시 → 사용 개월 수 × 월평균가 (131,600 ÷ 12)
    - 12개월 초과 사용 시 → 131,600원 + 초과 개월 수 × 12개월 구독 타입의 월평균가
  - 이 방식은 실제 구독 기간을 반영하여 과도한 매출 추정을 방지하며, 보수적으로 수익 추정 가능

- 위 개선된 LTR 계산 함수를 `.apply()` 형태로 적용하고 `user_df['LTR']` 컬럼 생성 완료

---

## \* 사용했던 코드

### LTR 계산 방식 정리

```python
def calculate_ltr(row):
    # 1개월 플랜: 고정 단가
    if row['plan_type'] == '1개월 플랜':
        return row['subscription_months'] * 15920.0

    # 12개월 플랜: 조건 분기
    elif row['plan_type'] == '12개월 플랜':
        base_price = 131600.0
        monthly_price = base_price / 12
        months = row['subscription_months']

        if months <= 12:
            return months * monthly_price
        else:
            extra_months = months - 12
            return base_price + (extra_months * monthly_price)

    # 나머지 (plan_type 없는 유저): NaN 반환
    else:
        return np.nan

user_df['LTR'] = user_df.apply(calculate_ltr, axis=1)
```

<br>

---

<br>

## \* 문제점

- 오늘 분석이 개인적으로 시간이 너무 오래걸린것 같아서 아쉬움

- 분석 중 `.apply()`나 `.loc[]`, `np.maximum()` 등 Pandas/Python 문법을 사용하는 데 어려움을 겪음  
  → **기본 문법에 대한 학습 부족을 체감했으며, 반복 학습과 실습의 필요성**을 절감함

---

## \* 회고

- 오늘 `.apply()` 함수 작성이나 조건 분기 처리에서 오류를 자주 내며,  
  **파이썬 기초 문법을 많이 까먹고 있다는 점을 뼈저리게 느낌**  
  → Pandas와 Python 기초 문법을 다시 복습하고, 함수/조건문/값 대입 로직을 연습해야겠다는 다짐을 함
