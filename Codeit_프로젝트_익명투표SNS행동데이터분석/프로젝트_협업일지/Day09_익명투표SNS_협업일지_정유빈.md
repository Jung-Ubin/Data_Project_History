# Day - 9 협업 일지(고급)

#### 일자: 25-10-23 / 정유빈

---

### 팀원들과 논의한 일

- 각자 테이블들을 살펴본 후 고객들의 비즈니스 플로우 파악하기
- 결제율 상승을 위한 방향성을 가지고 분석 진행하기

<br>

## \* 오늘 + 내가 한 일

- 우리 팀의 주 목적인 "서비스 이용자의 결제율 상승"을 알아보기 위해서,
- 결제율을 높이려면, **결제까지 도달한 사람들의 행동 경로를 이해해야 한다고 판단함**

### `device_id_summary` 뷰 생성하기

<br>

#### 문제 인식 배경

> `hackle_events`와 `hackle_properties` 두 테이블을 분석하는 과정에서,  
> `user_id`, `session_id`, `device_id`의 관계가 일관되지 않고 뒤섞여 있는 문제가 발견되었다.

<br>

#### 발견된 문제점

- 같은 `device_id`에 여러 `user_id`가 연결되어 있음
- `user_id`가 숫자형(가입 유저)과 문자형(비회원 또는 익명)으로 혼재되어 있음
- 동일 `device_id` 내에서도 `session_id`가 여러 개 존재하며, 일부는 중복 또는 불명확하게 매핑됨

<br>

이러한 이유로 **행동 데이터(event flow)** 를 추적하거나  
**사용자 단위(user-level)** 분석을 직접 수행하기 어렵다고 판단하였다

<br>
<br>

#### event_flow를 확인하기 위한 정렬

- 이 뷰는 **하나의 고유 디바이스(`device_id`)가 단 하나의 유저(`user_id`)만 가지는 완전한 1:1 매핑 데이터**를 만들기 위한 것

<br>

- 이를 통해 **비정상 매핑(여러 유저가 같은 기기를 쓰거나, 한 유저가 여러 기기를 사용하는 경우)** 을 모두 제거하고, 정제된 “고유 유저–기기 단위”의 **세션 흐름(Event Flow)** 을 분석할 수 있게 됨

<br>

- 정제 과정에서의 데이터 손실을 확인 했을 때, 전체 대비 소수의 데이터가 오류이기 때문에,
- 오류 데이터들(`user_id`가 공란인 `device_id`는 삭제, `user_id` 여러 개의 `device_id`를 거쳐갔을 때도 해당되는 데이터 삭제)

<br>
<br>

### `device_id_summary` 주요 데이터 출처

| 테이블              | 역할                               | 주요 컬럼                                      |
| ------------------- | ---------------------------------- | ---------------------------------------------- |
| `hackle_properties` | 디바이스, 유저, OS, 세션 연결 정보 | `device_id`, `user_id`, `osname`, `session_id` |
| `hackle_events`     | 세션별 이벤트 로그                 | `session_id`, `event_datetime`, `event_key`    |

> 두 테이블은 `session_id` 기준으로 조인된다

<br>
<br>

### 단계별 처리 로직

#### 1. 비정상 유저 제거 (`valid_user_device`)

`hackle_properties`에서 아래 조건을 만족하는 행만 남김:

- `user_id`가 `NULL` 아님
- `user_id`가 빈 문자열(`''`) 아님
- `user_id`가 숫자로만 구성 (`^[0-9]+$`)

→ 문자 난수나 비회원 세션 제거

---

#### 2. 디바이스 중복 확인 (`device_unique`)

- 각 `device_id`가 몇 개의 `user_id`를 가지고 있는지 계산
- `user_per_device = 1` → “한 디바이스–한 유저” 관계 가능

---

#### 3. 유저 중복 확인 (`user_unique`)

- 각 `user_id`가 몇 개의 `device_id`를 사용했는지 계산
- `device_per_user = 1` → “한 유저–한 디바이스” 관계 가능

---

#### 4. 1:1 매핑만 필터링 (`filtered_mapping`)

- 위 두 조건을 동시에 만족하는 행만 남김  
  (`user_per_device=1 AND device_per_user=1`)
- 즉, **하나의 유저가 단 하나의 기기만 사용했고, 그 기기 역시 다른 유저와 공유되지 않은 경우만 유지**

---

#### 5. 세션별 이벤트 흐름 생성 (`user_session_flow`)

- 각 `(user_id, device_id, session_id)` 조합별로
  - `event_datetime` 기준 오름차순 정렬
  - 세션 내 이벤트(`event_key`)를 순서대로 연결 → `'a,b,c'` 형태의 `session_flow` 생성
  - `MIN(event_datetime)`을 `session_start_time`으로 저장 → 이후 정렬 기준으로 활용

---

#### 6. 유저 단위 세션 흐름 병합 (`merged_flow`)

- 같은 유저(=같은 디바이스)가 가진 세션들을 시간순으로 정렬하여
  - `session_id` 리스트를 콤마(`,`)로 연결  
    → `"sessionA,sessionB,sessionC"`
  - `session_flow`들을 `' / '` 구분자로 연결  
    → `"launch_app→view_shop / launch_app→click_question_start→complete_signup"`
  - 세션 개수(`session_count`) 계산

---

#### 7. 최종 출력 (`SELECT`)

- 순번(`num`)을 부여하고 핵심 컬럼만 정리

```bash
num / device_id / osname / user_id / session_id / session_count / event_flow
```

<br>

- 모든 결과는 `user_id` 기준으로 정렬됨

---

### `device_id_summary` 뷰 검증 결과

| 항목                      | 값      |
| ------------------------- | ------- |
| 전체 행 수 (`total_rows`) | 228,192 |
| 고유 device_id 수         | 228,192 |
| 고유 user_id 수           | 228,192 |

> `total_rows = unique_device_id_count = unique_user_id_count`  
> → **모든 device_id ↔ user_id가 1:1 매핑된 상태로 완벽히 정제됨**

---

## 추가 정보

- `hackle_properties`에 존재하는 고유 `device_id` 수: **251,720건**
- `device_id_summary_2`의 최종 행 수: **228,192건**
- 즉, 1:1 매핑 필터링 및 `user_id` == NULL 값 제거로 인해 약 **23,500여 개의 NULL & 다중 매핑 케이스 제거됨**

---

## 활용 포인트

- **퍼널 분석**  
  `event_flow`를 이용해 `launch_app → view_shop → click_purchase`와 같은 행동 경로 분석 가능

  <BR>

- **유저 활동 분류**  
  `session_count`를 기반으로 고활성/저활성 유저 그룹화 가능

  <BR>

- **OS별 비교 분석**  
  `osname`을 활용해 iOS/Android 유저 행동 차이 분석 가능

---

## \* 사용했던 코딩

### `device_id_summary` 개선 뷰 쿼리

```sql
CREATE OR REPLACE VIEW final.device_id_summary_2 AS
WITH valid_user_device AS (
    -- 1) 공란/문자난수 user_id 제거 (숫자만 허용)
    SELECT
        device_id,
        user_id,
        osname,
        session_id
    FROM final.hackle_properties
    WHERE user_id IS NOT NULL
      AND user_id <> ''
      AND user_id REGEXP '^[0-9]+$'
),
device_unique AS (
    -- 2) device_id가 가리키는 user_id 수
    SELECT device_id, COUNT(DISTINCT user_id) AS user_per_device
    FROM valid_user_device
    GROUP BY device_id
),
user_unique AS (
    -- 3) user_id가 거친 device_id 수
    SELECT user_id, COUNT(DISTINCT device_id) AS device_per_user
    FROM valid_user_device
    GROUP BY user_id
),
filtered_mapping AS (
    -- 4) 완전 1:1(device_id ↔ user_id)만 유지
    SELECT v.device_id, v.user_id, v.osname, v.session_id
    FROM valid_user_device v
    JOIN device_unique d  ON v.device_id = d.device_id AND d.user_per_device = 1
    JOIN user_unique  u  ON v.user_id   = u.user_id   AND u.device_per_user = 1
),
user_session_flow AS (
    -- 5) (user_id, device_id, session_id) 단위 세션 플로우 생성
    SELECT
        f.device_id,
        f.user_id,
        f.osname,
        f.session_id,
        MIN(e.event_datetime) AS session_start_time,
        GROUP_CONCAT(e.event_key ORDER BY e.event_datetime ASC SEPARATOR ',') AS session_flow
    FROM filtered_mapping f
    JOIN final.hackle_events e
      ON e.session_id = f.session_id
    GROUP BY f.device_id, f.user_id, f.osname, f.session_id
),
merged_flow AS (
    -- 6) 한 유저(=한 디바이스)에 대해 세션을 시간순으로 합치기
    SELECT
        uf.device_id,
        uf.user_id,
        uf.osname,
        -- ⚠️ 요구사항: session_id를 시간순 리스트로 제공(콤마 구분)
        GROUP_CONCAT(uf.session_id ORDER BY uf.session_start_time ASC SEPARATOR ',') AS session_id,
        COUNT(*) AS session_count,
        GROUP_CONCAT(uf.session_flow ORDER BY uf.session_start_time ASC SEPARATOR ' / ') AS event_flow
    FROM user_session_flow uf
    GROUP BY uf.device_id, uf.user_id, uf.osname
)
SELECT
    ROW_NUMBER() OVER (ORDER BY user_id) AS num,
    device_id,
    osname,
    user_id,
    session_id,      --  여기 추가됨 (시간순 리스트)
    session_count,
    event_flow
FROM merged_flow
ORDER BY user_id;
```

---

---

## \*문제점

- 이벤트 플로우를 확인하기위해 `device_id` 별로 정리를 해놨지만, 뷰 제작 출처 테이블의 `event_key` 보유 상황을 살펴봤을 때 `complte_purchase`(결제 완료) **이벤트 키의 등장 횟수가 굉장히 적었던 것으로 파악**되서, 앞으로 "**결제까지 도달한 사람들의 행동 경로**"를 파악할 때 어떻게 진행해야 할지 감이 잘 잡히지 않음

<BR>

## \* 회고

- 만든 뷰에서의 각 유저들의 `event_flow`를 파악하고, depth를 나눠서 depth별 가장 자주 나오는 이벤트 순서를 모아서 내일 진행해보자.
- 각 테이블들의 데이터들이 복잡하게 엉켜있어서, 데이터들을 정리하고, 정렬하는데 시간을 오래 쏟았음.
- 내일 다시한번 검토해보고, 위에 설명한 내용을 진행해봐야겠따.
