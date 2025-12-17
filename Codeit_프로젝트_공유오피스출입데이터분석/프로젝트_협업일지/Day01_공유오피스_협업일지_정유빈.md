# Day - 1 협업 일지(중급2)

#### 일자: 2025-09-04 / 정유빈

---

### 팀원들과 논의한 일

- 데이터 전처리를 어떻게 진행할 것인지

## \* 오늘 + 내가 한 일

- trial_visit_info) 3일체험 신청자 일자별 방문기록 유저id, 날짜, 지점id, 최초입실시각, 최종퇴실시각, 체류시간
- 해당 테이블의 전처리를 진행
- 결측 / 중복 및 데이터 처리 기준을 팀원들과 의논하여 세우고 적용시켜 전처리 진행
- 유저별 trial 기간 산출

```python
groupby("user_uuid") + min(date) / max(date) 활용
```

- 72시간(3일) 이상 이용한 유저 = 134명 (전체의 약 2.2%) 이상 유저 제거
- isin과 ~를 이용해 해당 유저 삭제 → df_removed_cleaned 생성

- 유저별 마지막 trial_day 추출

```python
sort_values + groupby(...).tail(1) 활용
```

- 컬럼은 ['site_id', 'date', 'stay_time_second_total', 'trial_day']만 선택
- 유저별 속성으로 df를 새로 만든 후 파생변수 생성에 대해서 논의

---

## \* 사용했던 코딩

```python
# 각 유저별 trial_day 시작날 기준 72시간 오버된 유저 수(+ 비율)

# 유저별 첫 날짜와 마지막 날짜 구하기
user_date_range = df2_removed.groupby("user_uuid").agg(
    first_date=("date", "min"),
    last_date=("date", "max")
).reset_index()

# datetime 변환
user_date_range["first_date"] = pd.to_datetime(user_date_range["first_date"])
user_date_range["last_date"] = pd.to_datetime(user_date_range["last_date"])

# 기간 계산 (단위: 일)
user_date_range["duration_days"] = (user_date_range["last_date"] - user_date_range["first_date"]).dt.days

# 72시간(3일) 이상인 유저
over_72_users = user_date_range[user_date_range["duration_days"] >= 3]

# 전체 유저 수, 조건 만족 유저 수, 비율
total_users = user_date_range["user_uuid"].nunique()
over_72_count = over_72_users["user_uuid"].nunique()
over_72_ratio = over_72_count / total_users * 100

print(f"72시간(3일) 이상 이용한 유저 수: {over_72_count}")
print(f"전체 유저 수: {total_users}")
print(f"비율: {over_72_ratio:.2f}%")
```

---

## \*문제점

- 각 테이블 별 데이터가 많이 꼬여있어서 처리할 기준을 정하기 어려웠음
- 팀원들과 의논하며 기준을 계속 개선하며 진행하여 처음부터 계속 다시 시작하는 경우가 많았음

## \* 회고

- 프로젝트를 할 때마다 느끼지만 전처리 작업이 제일 어려울 뿐더러  
  가장 중요하다는것을 실감했다.
- FI(Feature Importance)를 확인하여 비즈니스 전략에 대해 가설을  
  설정하려 했는데 전처리 기준이 불명확하면 모델 결과 역시 왜곡될 수 있다는 점을 깨달았다.
- 팀원들과 전처리 기준 등을 의논하며, 내가 놓친 부분을 배울 수 있어서, 데이터를 바라보는 시각이 더 넓어졌다.
- 전 프로젝트에서도 느꼈듯 가설을 세우기 전 데이터의 구조, 생김새, 특성등을 이해하는 단계가 먼저 필요하다는 것을 오늘도 느꼈다.
