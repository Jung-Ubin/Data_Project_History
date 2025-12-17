# Day - 2 협업 일지(중급1)

#### 일자: 2025-07-08 / 정유빈

---

### 팀원들과 논의한 일

- 각 맡은 소 주제에 대해서 관련 분석을 진행했음

---

## \* 오늘 + 내가 한 일

- 무료 체험을 시작한 사용자 중 유료 결제 전환 여부 분석 진행

- 전환률 분석을 위해 `user_id` 기준으로 무료 체험자, 유료 결제자 집합 생성  
  → Set 연산을 사용하여 전환된 사용자 계산

- 무료 체험자 수 대비 전환 비율이 **약 22.87%** 임을 확인

- 이후 심화 분석(예: 체험 사용자 vs 비체험 사용자 비교, 카이제곱 검정, 로지스틱 회귀 등)을 위해 전체 유저 기준의 테이블 구성 구상 시작

---

## \* 사용했던 코드

### 무료 체험 → 구독 전환률 계산 코드

```python
# 무료 체험 → 구독 전환률 계산 코드

# 파일 불러오기
free_trial_df = pd.read_csv('/content/drive/MyDrive/Codeit_1팀_중급1/주제2_원본데이터들/start.free_trial.csv', encoding="utf-8-sig")
sub_df = pd.read_csv('/content/drive/MyDrive/Codeit_1팀_주제2_원본데이터들/complete.subscription.csv', encoding="utf-8-sig")
renew_df = pd.read_csv('/content/drive/MyDrive/Codeit_1팀_중급1/주제2_원본데이터들/renew.subscription.csv', encoding="utf-8-sig")

# 유저 ID만 뽑기
free_users = set(free_trial_df['user_id'].unique())
paid_users = set(sub_df['user_id'].unique()) | set(renew_df['user_id'].unique())

# 전환된 유저: 무료 유저 중 결제까지 간 유저
converted_users = free_users & paid_users

# 전환률 계산
total_free = len(free_users)
converted = len(converted_users)
conversion_rate = converted / total_free if total_free > 0 else 0

# 출력
print("무료 체험 → 유료 전환 분석")
print(f"무료 유저 수       : {total_free}")
print(f"전환된 유저 수     : {converted}")
print(f"전환률             : {conversion_rate:.2%}")
```

---

## \* 문제점

- 카이제곱 검정/로지스틱 회귀분석을 통해 사용자의 행동 분석 우선순위를 잡았지만,  
  어떻게 진행하는지에 대해선 고민하지 못했음

---

## \* 회고

- 테이블별 컬럼 구조를 다시 정리해보면서 분석 가능한 변수들 목록화한 것이 도움이 되었음  
  다음 심화 분석(무료 트라이얼 사용자들이 왜 구독전환률이 높은지?) 에 대해서도 같은 방식으로 하면 되겠다고 느낌

---
