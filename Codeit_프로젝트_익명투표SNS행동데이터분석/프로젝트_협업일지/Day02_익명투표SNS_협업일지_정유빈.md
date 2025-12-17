# Day - 2 협업 일지(고급)

#### 일자: 25-10-14 / 정유빈

---

### 팀원들과 논의한 일

- 각자 테이블 살펴보기 및 ERD 진행
- 모 sns사의 결제율 상승을 큰 틀로 잡고 테이블을 바라보자는 방향으로 논의

<br>

## \* 오늘 + 내가 한 일

### 1. sql에서 View로 만들었던 `user_payment_summary` 가져와서 클러스터링 진행

- View에서 분석용 데이터 선정 : X = df[['total_heart', 'total_paycount']].copy()
- 최적의 k 수 : 4 (Elvbow Method로 확인)

![1760405436406](<image/Day2_협업일지(고급)_DA_08_1팀_정유빈/1760405436406.png>)

| 클러스터 | 평균 총 하트 구매량 (`total_heart`) | 평균 총 결제 횟수 (`total_paycount`) |
| :------: | :---------------------------------: | :----------------------------------: |
|  **0**   |            **약 5,854**             |               **6.65**               |
|  **1**   |             **약 794**              |               **1.08**               |
|  **2**   |            **약 19,632**            |              **14.30**               |
|  **3**   |            **약 2,209**             |               **2.73**               |

<br>

### 2. 각 군집별 결재 패턴 분석

![1760405652619](<image/Day2_협업일지(고급)_DA_08_1팀_정유빈/1760405652619.png>)

<br>

### 3. KMeans 클러스터링 분석 간단 해석

| 클러스터 | 주요 결제 패턴                                                |
| :------- | :------------------------------------------------------------ |
| **0**    | 200·1000 하트 상품 위주로 고르게 결제하는 중간 활동 그룹      |
| **1**    | 777 하트 위주로 결제하지만 전반적으로 결제 빈도 낮은 저활동군 |
| **2**    | 모든 하트 상품을 많이 결제하는 **고액 결제군(핵심 매출층)**   |
| **3**    | 777·1000 하트 상품 중심의 소액 다회형 그룹                    |

<BR>

![1760404584247](<image/Day2_협업일지(고급)_DA_08_1팀_정유빈/1760404584247.png>)

| 분석                   | 질문                                                                     | 답변                                                                      |
| ---------------------- | ------------------------------------------------------------------------ | ------------------------------------------------------------------------- |
| **SQL 총합 분석**      | “전체적으로 어떤 하트 상품이 가장 많이 팔렸나?”                          | → **777 하트가 60.8%로 압도적**                                           |
| **K-Means 클러스터링** | “유저를 결제 패턴으로 묶으면, 각 그룹은 어떤 하트 상품을 주로 결제하나?” | → 예를 들어, 2번 클러스터는 1000·4000 하트 중심, 0번은 200·1000 하트 중심 |

- 전체적으로는 **777 하트가 가장 잘 팔림 → 매출 구조의 중심 상품**

- 그러나 `고액 유저층(cluster 2) 은 heart1000 및 heart4000 위주로 구매`  
  → VIP 상품

- `저활동 유저(cluster 1) 는 대부분 heart777 위주의 소액 단건 결제`로 보여짐  
   → 프로모션/재활성화 타깃 가능

### 4. 유저 속성 view (`user_info`)를 제작하기 위해 각 테이블에서 속성 찾아보기 (내가 찾은 속성)

- `user_payment_summary` View에 존재하는 `user_id`들에게 속성을 붙여줘서, `user_info` View를 제작할 예정

<BR>

- 유저 속성 1 : `user_properties` → 각 유저의 성별, 학교, 학년, 반 유저 속성 생성
  - `gender` : 성별 (`F`, `M`)
  - `school` : 학교
  - `grade` : 학년
  - `class` : 반

<br>

- 유저 속성 2 : `accounts_user` → `friend_id_list` 를 명 수로 변환해서 → 각 유저들의 친구가 몇 명 있는지

  - `friend` : 해당 유저의 친구 수

<br>

- 유저 속성 3 : `accounts_user` → `is_push_on`을 활용하여 → 알람을 켠 유저 / 알람을 꺼놓은 유저 속성 생성

  - `is_push_on` : 해당 유저의 앱 알람 ON/OFF 여부

<br>

- 유저 속성 4 : `accounts_userquestionrecord` → **chosen_user_id**, **user_id**, **has_read**, **answer_status**을 활용하여 아래와 같은 속성 생성
  - `chosen_count` : 해당 유저가 선택받은 횟수 (**chosen_user_id**에서 아이디 등장 횟수 카운트)
  - `selection_count` : 해당 유저가 선택한 횟수 (**user_id**에서 아이디 등장 횟수 카운트)
  - `answer_count` : 해당 유저가 질문에 답변한 횟수 (**chosen_user_id** 유저의 **answer_status**가 `A`인 횟수 카운트)
  - `pending_answer_count` : 해당 유저가 답변보류중인 질문 횟수 (**chosen_user_id** 유저의 **answer_status** `P`인 횟수 카운트)
  - `no_answer_count` : 해당 유저가 답변 거절한 질문 횟수 (**chosen_user_id** 유저의 **answer_status** `N`인 횟수 카운트)
  - `read_count` : 해당 유저가 받은 질문을 읽은 횟수 (**chosen_user_id** 유저의 **answer_status**가 1인 횟수 카운트)

<br>

- 유저 속성 5 : `polls_usercandidate` → `user_id` 컬럼을 사용
  - `apperance_count` : 해당 유저의 질문 등장 횟수 카운트

<br>

- 유저 속성 6 : `accounts_attendance` → `attendance_date_list` 활용
  - `attendance_count` : 해당 유저의 출석 횟수 카운트

<br>

- 유저 속성 7 : `accounts_blockrecord` → `block_user_id` 활용

  - `blocked_count` : 해당 유저가 차단당한 횟수 카운트

<br>

- 유저 속성 8 : `accounts_timelinereport` → `user_id`, `reported_user_id` 활용

  - `report_count` : 해당 유저가 신고한 횟수 카운트
  - `reported_count` : 해당 유저가 신고당한 횟수 카운트

<br>
<br>

---

## \* 사용했던 코딩

### `accounts_timelinereport` → `user_id`, `reported_user_id` 활용하여 유저별 `report_count` / `reported_count` 확인

```sql
WITH reported AS (
    SELECT
        reported_user_id AS user_id,
        COUNT(*) AS reported_count
    FROM final.accounts_timelinereport
    GROUP BY reported_user_id
),
reporter AS (
    SELECT
        user_id,
        COUNT(*) AS report_count
    FROM final.accounts_timelinereport
    GROUP BY user_id
)
-- FULL JOIN 대체
SELECT
    COALESCE(r.user_id, p.user_id) AS user_id,
    COALESCE(p.report_count, 0) AS report_count,
    COALESCE(r.reported_count, 0) AS reported_count
FROM reported r
LEFT JOIN reporter p ON r.user_id = p.user_id

UNION

SELECT
    COALESCE(r.user_id, p.user_id) AS user_id,
    COALESCE(p.report_count, 0) AS report_count,
    COALESCE(r.reported_count, 0) AS reported_count
FROM reporter p
LEFT JOIN reported r ON r.user_id = p.user_id;
```

---

## \*문제점

- 아직 살펴보지 못한 테이블이 많음 유저 속성이 더 추가될 예정
- 팀원 중 데이터 세팅이 아직 안된 팀원들이 있어서 아직 활발하게 분석이 이뤄지지 못한 점이 아쉬움
- `user_info` View를 생성하기 전 SQL로 데이터를 겉햝기 식으로 살펴보고있는데 앞으로 찾아볼 유저 속성까지도 다 넣어서 Veiw를 만들 때  
  유저 속성에 Null값이 존재한다던지 그런 점이 걱정되긴 함

## \* 회고

- 아직 살펴보지 못한 테이블들을 확인하어, `user_info` View를 생성하고 클러스터 군집에 대입하여 각 군집 별 유저 특징을 확인해봐야겠다.
- SQL 쿼리를 짜는 능력이 아직 많이 부족해서 불안하다. 쿼리를 읽을 줄 알고 어떻게 분석을 해야할진 생각이 나는데  
  막상 쿼리를 짤 때는 문법이 잘 생각이 안나서 힘들다.. SQL을 열심히 공부해야 할 것 같다.
