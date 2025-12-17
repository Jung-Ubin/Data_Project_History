# Day - 4 협업 일지(중급1)

#### 일자: 2025-07-10 / 정유빈

---

### 팀원들과 논의한 일

- 팀 협업일지를 통한 업무 공유 및 팀 내 피드백 진행

---

## \* 오늘 + 내가 한 일

- 구독자 1명이 실제 수강한 레슨 수 대비, 레슨 1회당 '가상의 비용'이 얼마인지 파악하는 분석 진행

  - 분석 대상자 정의
  - 수강 완료 레슨 수 집계
  - 레슨당 가정비용 계산
  - 시각화![1752141258306](<image/Day4_협업일지(중급1)_DA_08_1팀_정유빈/1752141258306.png>)
  - 이상치 제거 및 분포 재분석

- 주제 2 a회사의 LTV 분석 진행 중
- 분석 대상 정리: 유저별 LTR 계산

---

## \* 사용했던 코드

### cost_per_lesson(사용자측 레슨 1회당 소비비용) 컬럼 내 이상치 제거

```python
# 이상치 기준 계산
Q1 = user_summary_df['cost_per_lesson'].quantile(0.25)
Q3 = user_summary_df['cost_per_lesson'].quantile(0.75)
IQR = Q3 - Q1

lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

# 이상치 제거
filtered_df = user_summary_df[(user_summary_df['cost_per_lesson'] >= lower_bound) &
                              (user_summary_df['cost_per_lesson'] <= upper_bound)]

filtered_df['cost_per_lesson'].describe().round(2)
```

|       | cost_per_lesson |
| ----- | --------------- |
| count | 12498.00        |
| mean  | 914.43          |
| std   | 1005.20         |
| min   | 7.47            |
| 25%   | 211.70          |
| 50%   | 505.40          |
| 75%   | 1224.62         |
| max   | 4700.00         |

<br>

## \* 문제점

- renew.subscription 로그가 일부 유저에게 누락되는 현상이 있어,
  기존 LTR 계산 방식이 실제 구독 기간을 과대 추정할 가능성 존재

> EX)
>
> > 1개월 타입
> > 1월 결제 (첫 구독 시작 > 첫 결제 완료 로그)  
> > 2월 결제 (정기 결제 갱신 로그 + 만료 후 재구독)  
> > →이런식이면 값이 부풀려졌을 수가 있음

- plan.type에 따라 결제 구조가 다르므로 로그 흐름 분석 필요
- click.cancel_subscription_button 등 구독 종료 시점 파악 가능한 로그가 있는지 검토 필요

---

## \* 회고

- 단순히 이벤트 로그 개수를 세는 기존 방식은 실제 구독 기간과 차이가 있을 수 있음을 인지

- 분석 정확도를 위해 로그 흐름을 실제 유저 단위로 면밀히 확인하는 과정의 필요성을 느낌

- 이상치 제거로 분석 신뢰도가 높아질 수 있었고, LTR/LTV 계산의 신뢰 기반이 마련된 하루
