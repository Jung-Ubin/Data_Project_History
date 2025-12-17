# Day - 8 협업 일지(고급)

#### 일자: 25-10-22 / 정유빈

---

### 팀원들과 논의한 일

- 각자 테이블들을 살펴본 후 고객들의 비즈니스 플로우 파악하기
- 결제율 상승을 위한 방향성을 가지고 분석 진행하기

<br>

## \* 오늘 + 내가 한 일

## 테이블 하나씩 뜯어 보기

- `hackle_events` 이벤트 테이블 정보 이어서 요약
- device 전용 view 생성

  <br>

---

## 이벤트 테이블 `hackle_events`(헥클 이벤트 발생 목록) 테이블 정리\_2

- 우리 팀의 주 목적인 "서비스 이용자의 결제율 상승"을 알아보기 위해서,
- 결제율을 높이려면, **결제까지 도달한 사람들의 행동 경로를 이해해야 한다고 판단함**

- `hackle_events` 내 고유 `session_id`들이 보유 중인, `event_key`들을 확인하고,
- 퍼널 단계를 정해서, 결제까지 도달하기 까지 구간 별 이탈률을 확인해 봐야겠다고 판단.

<br>

- 1번 이벤트 키를 보유한 고유 session_id 확보
- 1번과 2번 이벤트 키를 보유한 고유 session_id 확보,
- 1, 2, 3번 이벤트 키를 보유한 고유 session_id 확보
- 1, 2, 3, 4 이벤트 키를 보유한 고유 session_id 확보

<br>

1. 앱 실행 ($session_start, launch_app)
2. 서비스 이용 (click_question_start, complete_question)
3. 결제 화면 진입 (view_shop)
4. 결제 완료 (complete_purchase)

- 쿼리 결과
  ![1761123006058](<image/Day8_협업일지(고급)_DA_08_1팀_정유빈/1761123006058.png>)

<br>

확실히 이렇게 가볍게 몇 개의 이벤트만 확인해서 파악하기에는 인사이트로 활용하기 부족하다고 판단함

그래서, 기준을 정하여, 다시 퍼널 구조를 확인해보기로 함

### `session_id` 와 `user_id`, 그리고 `device_id`

- `session_id`는 `hackle_evnets`와 `hackle_properties`테이블에 컬럼이 존재함

- `user_id`와 `device_id`는 `hackle_properties`테이블에만 컬럼이 존재함 (`hackle_events` 테이블에 없음)

<br>

- 그리고 `device_id`와 `user_id`, `session_id`가 엉켜있는 상태

  - `device_id`에 여러 개의 `user_id` 존재 확인
  - `user_id`에 여러 개의 `session_id` 존재 확인
  - `user_id`에 여러 개의 `device_id` 존재 확인

유저들을 특정 방법을 어떻게 둘 것인지 팀원과 소통해본 결과 아래 2가지 방법 모두 확인해보자 결론남

<br>

1. `device_id` 기준 `session_id`의 모든 `event_flow`를 묶어서 분석
   - 1. 각 고유 `device_id` 행에서 `user_id`가 결측인 데이터는 삭제 (전체 데이터 대비 얼마 없음)
   - 2. 각 `user_id`에 `device_id`가 2건 이상 존재 시 해당 데이터는 삭제 (전체 데이터 대비 얼마 없음)
   - 3. 처리한 고유 `device_id` 목록에서 `user_id`확인 후 보유중인 `session_id` 확인
   - 4. 결제 완료 이벤트 키(`complete_purchase`)까지의 퍼널 구조를 설계

<br>

1. `user_id` 기준 `session_id`의 모든 `event_flow`를 묶어서 분석
   - 1. `session_id`와 `user_id`가 엮여있는 테이블(`hackle_properties`)에서 `user_id` 별로 보유중인 `session_id`를 확인
   - 2. 해당 `session_id`들이 보유중인 `event_key`들을 `event_datetime` 순으로 나열해서 각 `user_id`별 한 줄로 리스트화
   - 3. 해당 `user_id`들의 `event_flow`를 살펴본 후 `complete_purchase` 까지 퍼널 구조 설계

<br>

### `device_id_summary` view 생성 과정

#### 목적

`final.device_id_summary` 뷰는 **디바이스 단위로 유저·세션·이벤트 흐름을 한 줄로 요약**하기 위한 View
결제 퍼널 분석의 기반이 되는 데이터로,  
**한 디바이스에서 어떤 유저가, 어떤 세션을 통해, 어떤 이벤트 흐름을 보였는지를 확인 가능**

---

#### 사용 테이블

- **`final.hackle_properties`**  
  → `device_id`, `user_id`, `session_id`의 관계를 관리하는 테이블

- **`final.hackle_events`**  
  → 각 `session_id`별 `event_key`와 `event_datetime`(이벤트 발생 시각)을 기록한 테이블

---

#### 데이터 전처리 조건

1. **`user_id` 존재 데이터만 사용**

   - 비회원(비로그인) 사용자의 `device_id`는 제외 (`user_id IS NOT NULL AND user_id <> ''`)

2. **다중 기기 사용자 제거**

   - 하나의 `user_id`가 2개 이상의 `device_id`를 사용한 경우 → 해당 유저의 모든 행 제거
   - 결과적으로 `1 user_id ↔ 1 device_id` 관계만 남김

3. **정제된 데이터셋 확보**
   - 위 두 조건을 통과한 데이터는 **클린한 device-user 관계 테이블**로 사용

---

#### 뷰 구성 단계

1. **세션별 이벤트 흐름 생성 (`hackle_events` 테이블 활용)**

- 각 `session_id`별로 이벤트를 `event_datetime ASC` 순으로 정렬
- `GROUP_CONCAT(event_key SEPARATOR ',')`로 하나의 문자열로 연결

<br>

2. **디바이스별 세션 통합 (`hackle_properties` 테이블 활용)**

- `device_id`를 기준으로 같은 유저(`user_id`)를 묶고,
- 해당 유저가 가진 모든 세션(`session_id`)을 리스트로 연결
- `user_id_count`, `session_count` 로 `device_id` 당 보유 데이터 계산

<br>

3. **세션 이벤트 병합 (`event_flow`)**

- 각 세션의 이벤트 흐름(`session_event_flow`)을 시간 순으로 이어붙임
- 세션 간 구분은 `' / '` 기호로 표시
- 한 세션의 모든 이벤트가 끝나면 `' / '` 뒤에 다음 세션 이벤트가 이어짐

<br>

#### 최종 뷰 컬럼 구성

| 컬럼명          | 설명                                       |
| --------------- | ------------------------------------------ |
| `num`           | 행 번호 (ROW_NUMBER)                       |
| `device_id`     | 고유 디바이스 ID                           |
| `user_id`       | 해당 디바이스에 연결된 유저 ID (콤마 구분) |
| `user_id_count` | 해당 디바이스가 보유한 고유 유저 수        |
| `session_id`    | 해당 유저가 가진 세션 목록 (콤마 구분)     |
| `event_flow`    | 세션별 이벤트 흐름 (`/` 구분)              |

<br>

#### 구조 설계 이유

- **데이터 신뢰성 확보**  
  → 다중 기기를 사용하는 유저를 제외하여, 디바이스별 행동 패턴을 명확히 분석 가능 (`device_id`에 여러 user_id가 있어도 한 사람이라 가정했기 때문)

- **퍼널 분석용 구조 단순화**  
  → 각 device_id가 하나의 분석 단위가 되므로, 세션 기반 전환 흐름(앱 실행 → 결제) 분석이 쉬움

- **이벤트 흐름의 직관성**  
  → `event_flow` 컬럼 하나로 전체 행동 경로를 한눈에 파악 가능  
  → `/` 구분으로 세션 간 구분이 명확하여 시각화·전환 퍼널 설계에 유리

<br>

#### `device_id_summary` 확인

<BR>

![1761126823725](<image/Day8_협업일지(고급)_DA_08_1팀_정유빈/1761126823725.png>)

<BR>

- View 생성 시 CONCAT 실수를 해서 그림과 같은 결과가 나옴
- 그런데, 보면 숫자\_ID 와 문자\_ID가 연관성이 있어보여서 확인이 필요해보임

<br>

---

---

## \* 사용했던 코딩

### `device_id_summary` View 생성 쿼리 (CONCAT 실수를 해서 다시 만들어볼 예정)

```sql
CREATE OR REPLACE VIEW final.device_id_summary AS
WITH valid_properties AS (
    -- user_id가 존재하는 데이터만 사용
    SELECT device_id, user_id, session_id
    FROM final.hackle_properties
    WHERE user_id IS NOT NULL AND user_id <> ''
),
multi_device_user AS (
    -- 여러 device_id를 사용한 user_id 제거 대상 식별
    SELECT user_id
    FROM valid_properties
    GROUP BY user_id
    HAVING COUNT(DISTINCT device_id) > 1
),
clean_properties AS (
    -- 다중 기기 user 제거 후 남은 device-user-session 데이터
    SELECT *
    FROM valid_properties
    WHERE user_id NOT IN (SELECT user_id FROM multi_device_user)
),
session_event_flow AS (
    -- 세션 단위 이벤트 흐름 생성 (이벤트 시간순 정렬)
    SELECT
        session_id,
        GROUP_CONCAT(event_key ORDER BY event_datetime ASC SEPARATOR ',') AS session_flow,
        MIN(event_datetime) AS session_start_time
    FROM final.hackle_events
    GROUP BY session_id
),
device_event_flow AS (
    -- device_id 단위로 모든 세션을 시간 순으로 병합 (' / '로 구분)
    SELECT
        cp.device_id,
        cp.user_id,
        GROUP_CONCAT(DISTINCT cp.session_id ORDER BY sf.session_start_time ASC SEPARATOR ',') AS session_list,
        COUNT(DISTINCT cp.user_id) AS user_id_count,
        COUNT(DISTINCT cp.session_id) AS session_count,
        GROUP_CONCAT(sf.session_flow ORDER BY sf.session_start_time ASC SEPARATOR ' / ') AS event_flow
    FROM clean_properties cp
    JOIN session_event_flow sf ON cp.session_id = sf.session_id
    GROUP BY cp.device_id, cp.user_id
)
-- 최종 결과 출력 (행번호 포함)
SELECT
    ROW_NUMBER() OVER (ORDER BY device_id) AS num,
    device_id,
    user_id,
    user_id_count,
    session_count AS user_session_count,
    session_list,
    event_flow
FROM device_event_flow;
```

---

---

## \*문제점

- 행동 데이터를 결제 하는 사람들의 패턴 확인을 위해 분석해보다 보니, 순서가 꼬이거나 복잡해서 실수하는 경우가 발생함

<BR>

## \* 회고

- 팀원들과 의논했을 때, 어느정도 테이블은 살펴봤다는 의견이 나오고 이제 결제율에 관련된 분석을 진행해보자란 의견도 나왔음.
- 각각 테이블들을 살펴보면서, 활용할 인사이트를 정리해서 결제율 관련 분석과 아이템 아이디어를 내봐야겠다.
- 퍼널 분석을 할 때 로그들을 살펴보고 어떤식으로 확인해야 할지 아이디어가 떠오르지 않았음. 아직도, 퍼널 구조가 미완성이라 내일 강사님과 멘토님에게도 관련 질문을 해서 마무리 지을 예정..
