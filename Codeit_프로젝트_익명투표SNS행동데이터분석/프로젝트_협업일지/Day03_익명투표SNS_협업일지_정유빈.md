# Day - 3 협업 일지(고급)

#### 일자: 25-10-15 / 정유빈

---

### 팀원들과 논의한 일

- 각자 테이블 살펴보기 및 ERD 진행
- 질문 관련 테이블 EDA를 진행할 인원과 유저 관련 테이블 EDA를 진행할 팀원 선정 및 분업 진행

<br>

## \* 오늘 + 내가 한 일

### 1. 유저 속성 1번 사용 불가 판단

- 유저 속성 1번에 사용하려 했던 테이블은 **특정 이벤트 기간 내 수집된 정보 (한 달)** 라 내용이 한정적임(매칭이 힘들다 판단)
- 사용 불가로 판단하여 **학교, 학년, 반 정보는 사용 불가**
- 다만 **유저 성별**은 `accounts_user` 테이블에서 정보를 가져올 수 있음

<br>

### 2. 계획한대로 df를 만들었을 때 NULL이 대부분을 차지함

- 유저수는 많지만, 실제로 활동한 유저 수는 **극히 적은 것으로 보여졌음**  
   (`accounts_user` 테이블 기준 유저 정보 대입 시 발생한 NULL현황)
  ![1760495251299](<image/Day3_협업일지(고급)_DA_08_1팀_정유빈/1760495251299.png>)

<BR>

- 임시 `user_info` 각 컬럼의 NULL 개수
  ![1760495379795](<image/Day3_협업일지(고급)_DA_08_1팀_정유빈/1760495379795.png>)

<br>

### 3. NULL을 해결하기위한 방법

- **임시 `user_info` 상황을 봤을 때, NULL값이 적은 컬럼은 전부 `accounts_user` 테이블에서 가져온 정보**
- **`accounts_user`는 회원 전체 데이터**여서 `user_id`를 가져왔을 때 NULL이 많이 생김
- 그래서 `accounts_user` 테이블을 제외한 **나머지 테이블에서 중복없이 `user_id` 정보를 가져온 후 `accounts_user`에서 필요한 데이터만 가져오기**
  (여전히 NULL 값은 많지만, 최대한 줄여본 결과)
  ![1760496149048](<image/Day3_협업일지(고급)_DA_08_1팀_정유빈/1760496149048.png>)

<br>

- **NULL 대체 값 다른 값들을 채울 수 있다고 판단되는 속성들**은 대체 값으로 채움
  - `blocked_count` : 해당 유저가 차단 당한 횟수 NULL 일 땐 → `0.0`으로 변환
  - `report_count` : 해당 유저가 신고한 횟수 NULL 일 땐 → `0.0`으로 변환
  - `reported_count` : 해당 유저가 신고당한 횟수 NULL 일 땐 → `0.0`으로 변환
  - `apperance_count` : 해당 유저가 질문에 등장한 횟수 NULL 일 땐 → `0.0`으로 변환
  - `attendance_count` : 해당 유저가 출석한 횟수 Null 일 땐 → `0.0`으로 변환
- 나머지 컬럼들은 NULL 유지

    <br>

### 4. `user_info` view 제작 내용 정리

1. `accounts_user`에 `id`컬럼으로 유저를 특정했을 때 NULL값이 너무 많이 존재함
2. 해서, `accounts_user` 외 **다른 테이블에서 `user_id`를 중복없이 추출하고, 각 `user_id`들에 데이터를 넣는 식**으로 진행 → 이 방법으로 대략 절반의 NULL값을 날림 (약 67만 → 약 35만)
3. View 내의 컬럼들 중 NULL을 대체 값으로 치환할 수 있는 컬럼들은 변경하여 제작함

<BR>

4. 현재 `user_info` View의 구성 정리

![1760514571478](<image/Day3_협업일지(고급)_DA_08_1팀_정유빈/1760514571478.png>)

<br>

| 구분            | 테이블명                      | 사용된 컬럼                                              | `user_info`에 생성된 컬럼                                                                                                                                                                                                         |
| --------------- | ----------------------------- | -------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **유저 속성 1** | `accounts_user`               | `gender`                                                 | `gender` (성별)                                                                                                                                                                                                                   |
| **유저 속성 2** | `accounts_user`               | `friend_id_list`                                         | `friend` (친구 수)                                                                                                                                                                                                                |
| **유저 속성 3** | `accounts_user`               | `is_push_on`                                             | `is_push_on` (알림 ON/OFF 여부)                                                                                                                                                                                                   |
| **유저 속성 4** | `accounts_userquestionrecord` | `chosen_user_id`, `user_id`, `has_read`, `answer_status` | `chosen_count` (선택받은 횟수), `selection_count` (선택한 횟수), `spellcheck_count` (투표 응답 후 초성 확인 수), `nonspellcheck_count` (투표 응답 후 초성 미확인 수), `noanswer_count` (질문 미응답 수), `read_count` (읽은 횟수) |
| **유저 속성 5** | `polls_usercandidate`         | `user_id`                                                | `appearance_count` (질문 등장 횟수) **※ NULL값은 0으로 치환**                                                                                                                                                                     |
| **유저 속성 6** | `accounts_attendance`         | `attendance_date_list`                                   | `attendance_count` (출석 횟수) **※ NULL값은 0으로 치환**                                                                                                                                                                          |
| **유저 속성 7** | `accounts_blockrecord`        | `block_user_id`                                          | `blocked_count` (차단당한 횟수) **※ NULL값은 0으로 치환**                                                                                                                                                                         |
| **유저 속성 8** | `accounts_timelinereport`     | `user_id`, `reported_user_id`                            | `report_count` (신고한 횟수), `reported_count` (신고받은 횟수) **※ NULL값은 0으로 치환**                                                                                                                                          |

<br>

**★ 5**. `accounts_userquestionrecord` 테이블에서 제작된 View 변수들은, 결측 값을 0으로 대체하였으나,  
 **해당 컬럼들을 0 으로 한다면 서비스의 핵심 가치를 경험하지 못했다고 판단,**  
 **삭제하는 것과 다를게 없어서 NULL을 유지하고, 분석할 때 제외할 예정**

## <br>

## \* 사용했던 코딩

### `user_info`에서의 사용 가능한 데이터 수 확인(중요 데이터 컬럼 NULL 제외 살아있는 데이터 수와 비율)

```sql
-- user_info에서 null이 많이 존재하는 컬럼에서의 살아있는 데이터 개수와 그 데이터들의 비율
SELECT
  COUNT(*) AS total_rows,

  SUM(spellcheck_count IS NOT NULL) AS spellcheck_nonnulls,
  ROUND(SUM(spellcheck_count IS NOT NULL) / COUNT(*) * 100, 2) AS spellcheck_nonnull_pct,

  SUM(nonspellcheck_count IS NOT NULL) AS nonspellcheck_nonnulls,
  ROUND(SUM(nonspellcheck_count IS NOT NULL) / COUNT(*) * 100, 2) AS nonspellcheck_nonnull_pct,

  SUM(noanswer_count IS NOT NULL) AS noanswer_nonnulls,
  ROUND(SUM(noanswer_count IS NOT NULL) / COUNT(*) * 100, 2) AS noanswer_nonnull_pct,

  SUM(read_count IS NOT NULL) AS read_nonnulls,
  ROUND(SUM(read_count IS NOT NULL) / COUNT(*) * 100, 2) AS read_nonnull_pct
FROM final.user_info;

```

---

## \*문제점

- 현재 `user_info` 뷰 기준으로 **활성 데이터(결측이 없는 유효 행)는 총 15,426건 존재함** (`accounts_user` 테이블 기준 유저 수는 약 67만)

  - 이 데이터를 활용해 클러스터링 모델에 대입했을 때,  
     **클러스터를 구성하는 유저들이 `user_info`에 포함된 유저들과 얼마나 매칭되는지가 걱정됨..**
    <BR>
  - 다만, 만약 클러스터의 주요 구성원이 모두 user_info의 유저들과 일치한다해도,  
     **이는 활동이 활발한 유저일수록 하트 소모가 많고**  
     → 결제 가능성이 높다는 **예상 가능한 결과(활동량 ↔ 결제활동 연관성)** 로 해석될 가능성이 높음 (단순한 결과로 나올 것이다.. 라는 예상)
    <BR>

  - 따라서 단순히 활동 유저 중심의 클러스터 해석에 그치지 않고,  
     앱에서 **무작위로 제공되는 질문들의 유형별 반응(선호도, 참여율, 하트 소모율 등)** 을 함께 분석하면,  
     유저의 궁금증과 참여를 유도하는 질문 패턴을 더 구체적으로 파악할 수 있음
    <BR>

  - 다만, 어떻게해야 지금 정리해놓은 유저 특성과, 해당 질문들을 연결할지에 대해서는 조금 더 생각이 필요함  
     (ex: 질문들을 정리해서, 카테고리(장르:연애, 패션, 성격 등..)를 만들어서  
     각 유저의 `A(spellcheck_count)`가 많은 질문을 `user_info`에 컬럼을 추가해서 넣어야하나? → 그렇게 했을 때 데이터에선 과연 매칭이 잘 될까 힘들 것 같은데... 등 생각 중)
    <BR>

  - 이를 통해 향후 분석의 방향성을  
    **“결제 유도형 질문 디자인” 혹은 “참여 활성화 전략”** 으로 보다 명확하게 설정할 수 있을 것이라고 판단 됨.. 팀원들과 의논할 예정

<BR>

## \* 회고

- 이번 분석에서는 **예상대로 활동량이 높은 유저일수록 결제 확률이 높게 나타나는 당연한 결과가 도출될 가능성이 높다고 생각됨**

<BR>

- 단순히 유저의 결제 패턴만 분석하는 것은 새로운 인사이트를 얻기 어렵다는 한계를 느낌

<BR>

- 따라서 질문과 유저 간의 연관성, **즉 어떤 질문이 유저의 참여·하트 소모·결제 행동을 유발하는지**를 파악하기 위한 데이터 전처리 및 구조 설계 방안을 고민할 필요가 있음

<BR>

- 이를 통해 향후에는 **“결제를 유도하는 콘텐츠(질문) 특성”을 중심**으로 보다 실질적인 비즈니스 인사이트를 도출하는 방향으로 발전시킬 수 있을 것으로 기대됨
