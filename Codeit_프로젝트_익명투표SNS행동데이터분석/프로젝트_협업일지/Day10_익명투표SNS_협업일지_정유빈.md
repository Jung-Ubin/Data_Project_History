# Day - 10 협업 일지(고급)

#### 일자: 25-10-24 / 정유빈

---

### 팀원들과 논의한 일

- 테이블 분석 및 분석 현황 정리 후 중간 발표 준비
- 분석 방향 다시한번 명확히 논의 후 각자 분석 시작

<br>

## \* 오늘 + 내가 한 일

### `device_id_summary` 개선 후 팀원들에게 공유

- "**각각의 앱 사용자들의 패턴을 파악하고, 인사이트를 확보**"하고자 해당 테이블 제작을 진행(결제율 포함)
- `device_id` / `user_id` 가 1:1 매핑되는 유저들만 남겨서 제작 (손실되는 데이터 크기가 크지 않아서 해당 조건으로 진행)
- `device_id` 와 `user_id` 1:1 매핑으로 만들었던 뷰를 테이블로 변경 후 팀원들에게 공유
- 테이블 생성 조건 및 쿼리 내 충족 조건 확인은 아래와 같음(현재 제작 중)

| 조건                                               | 포함 여부 | 작동 위치                                                   | 설명                       |
| -------------------------------------------------- | --------- | ----------------------------------------------------------- | -------------------------- |
| 1. `hackle_events`, `hackle_properties` 사용       | ✅        | SESSION_FLOW 단계                                           | 두 테이블 모두 명시적 사용 |
| 2. `session_id` 기준 연결                          | ✅        | `JOIN final.hackle_events e ON e.session_id = p.session_id` |                            |
| 3. `device_id` 기준 event_datetime 순 정렬         | ✅        | `ORDER BY e.event_datetime ASC`                             |                            |
| 4. 1:1 매핑만 유지                                 | ✅        | CLEAN_USERS JOIN 구조 (HAVING 조건)                         |                            |
| 5. 다중 user_id 가진 device 제거                   | ✅        | `HAVING COUNT(DISTINCT user_id) = 1`                        |                            |
| 6. 다중 device 가진 user 제거                      | ✅        | `HAVING COUNT(DISTINCT device_id) = 1`                      |                            |
| 7. 결과에서 device_id, user_id 중복 없음           | ✅        | `GROUP BY cu.device_id, cu.user_id, cu.osname`              |                            |
| 8. event_flow 시간순 세션/이벤트 정렬              | ✅        | `ORDER BY session_start_time`, `ORDER BY e.event_datetime`  |                            |
| 9. 여러 세션의 event_flow 구조 ("," + "/")         | ✅        | 두 단계 `GROUP_CONCAT` 구조                                 |                            |
| 10. `device_id`에 `NULL/공백 user_id` 포함 시 제거 | ✅        | CLEAN_USERS의 WHERE + HAVING 조건에서 자동 제거             |                            |

<br>

- 테이블 자체가 무거운 테이블(`hackle_evnets` 테이블 행 수만 약 1100만 건)이어서 제작에 오래걸림
- 인덱스를 만들어서 최소한 시간을 줄여보려는중

---

### 각 팀의 중간발표를 들은 후, 팀원들과 분석 방향성에 대해서 논의

1. 각 유저들의 `학교` / `학년` / `성별` 정보를 파악하여 각 학년들의 질문 선호도 조사
   - 각 학년별, 성별별 선호 질문과 비선호 질문을 확인한 후 개선아이템을 내는 분석 방향

  <br>

2. 각 유저들의 행동 패턴을 파악하여, 짧게 이용한 유저, 길게 이용하는 유저들의 이탈지점 확인
   - 이탈률이 높은 지점의 UX 개선 아이템을 내는 분석 방향

  <br>

- 일단 위 두가지를 확인해보고 추가적인 아이디어 발생 시 새로운 분석을 추가진행해볼 예정

<br>

---

## \* 사용했던 코딩

### 테이블 제작을 위한 인덱스 제작 쿼리

```sql
-- device_id_summary 테이블 생성을 위한 인덱스 준비
-- ---------------------------------------------------------
-- hackle_properties 인덱스 설계
-- 1. session_id는 JOIN 키 → 해시 인덱스 효과 큼
CREATE INDEX idx_hackle_properties_session_id
    ON final.hackle_properties (session_id);

-- 2. device_id는 중복 검출 및 후속 GROUP BY / DISTINCT 용
CREATE INDEX idx_hackle_properties_device_id
    ON final.hackle_properties (device_id);

-- 3. user_id는 null 제거 및 중복 판별에 필요
CREATE INDEX idx_hackle_properties_user_id
    ON final.hackle_properties (user_id);

-- 4. (device_id, user_id) 복합 인덱스 → “1:1 매핑 검증”시 속도 개선
CREATE INDEX idx_hackle_properties_device_user
    ON final.hackle_properties (device_id, user_id);

-- ---------------------------------------------------------

-- hackle_events 인덱스 설계
-- 1. JOIN 키 (session_id)
CREATE INDEX idx_hackle_events_session_id
    ON final.hackle_events (session_id);

-- 2. event_datetime 정렬용 (시간순 event_flow 생성 시)
CREATE INDEX idx_hackle_events_datetime
    ON final.hackle_events (event_datetime);

-- 3. (session_id, event_datetime) 복합 인덱스 → 시간순 정렬 + 세션별 이벤트 탐색 속도 개선
CREATE INDEX idx_hackle_events_session_datetime
    ON final.hackle_events (session_id, event_datetime);
```

---

## \*문제점

- 테이블 데이터 규모가 커서 원하는 구조로 device_id 와 user_id, session_id 들을 정리허는 과정에서 어려움이 있음

<BR>

## \* 회고

- 원하는 구조의 테이블을 만들기에는 출처 테이블의 데이터 규모가 너무 크니, 인덱스를 설정하고 테이블을 제작하여 시간을 줄여봐야겠다.
- 다른 팀의 분석 과정이 주제도 잘 설정하고, 분석 과정도 설득이될 정도로 잘 준비해서 분석 과정과, 아이디어를 얻는 방법을  
  참고하여 우리 팀도 분석을 잘 준비해야겠다.
