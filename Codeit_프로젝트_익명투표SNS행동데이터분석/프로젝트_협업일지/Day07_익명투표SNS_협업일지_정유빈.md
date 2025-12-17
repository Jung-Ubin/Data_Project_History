# Day - 7 협업 일지(고급)

#### 일자: 25-10-21 / 정유빈

---

### 팀원들과 논의한 일

- 각자 테이블들을 살펴본 후 고객들의 비즈니스 플로우 파악하기

<br>

## \* 오늘 + 내가 한 일

## 테이블 하나씩 뜯어 보기

- 총 테이블 25개를 하나씩 뜯어보며, 비즈니스 플로우를 파악해보기

  <br>

---

## 이벤트 테이블 `hackle_events`(헥클 이벤트 발생 목록) 테이블 정리

- **데이터 규모** : 11,441,319건
- **데이터 목적** : 각 유저의 2023-07-18 ~ 2023-08-10 (약 4주) 해당 기간의 행동 로그 수집

### 컬럼 정보

| 컬럼명           |  NULL 건수 | NULL 비율(%) | 주요 설명                                 |
| ---------------- | ---------: | -----------: | ----------------------------------------- |
| `event_id`       |          0 |         0.0% | 이벤트 고유 식별자 (PK)                   |
| `event_datetime` |          0 |         0.0% | 이벤트 발생 시각                          |
| `event_key`      |          0 |         0.0% | 이벤트 종류                               |
| `session_id`     |          0 |         0.0% | 세션 식별자 (앱 실행 단위)                |
| `id`             |          0 |         0.0% | 유저 ID (문자열)                          |
| `item_name`      |          0 |         0.0% | 관련 아이템 이름                          |
| `page_name`      |          0 |         0.0% | 발생 페이지 이름                          |
| `friend_count`   |  7,525,560 |     약 65.7% | 친구 수 정보 (일부 이벤트만 수집됨)       |
| `votes_count`    |  7,545,540 |     약 65.9% | 투표 수 정보 (일부 이벤트만 수집됨)       |
| `heart_balance`  |  7,286,430 |     약 63.7% | 보유 하트 수 (일부 이벤트만 기록됨)       |
| `question_id`    | 10,991,835 |     약 96.1% | 관련 질문 ID (스킵 이벤트 등 대부분 NULL) |

---

### 1. 고유 `session_id` 수 확인

- `session_id` 고유 데이터 수 : **253,616**

<br>

### 2. `event_key` 이벤트별 발생된 횟수 및 와이어프레임 참고하여 행동 추측

| 순위 | 이벤트명 (`event_key`)            | 발생 횟수 | 주요 의미 / 발생 맥락          | 피그마 상 동작 / 설명                                                                                                                                                                          |
| ---- | --------------------------------- | --------: | ------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1    | view_lab_tap                      | 1,266,665 | 실험실(Lab) 탭 진입            | → (2)홈→질문 피그마 탭의 "시작 가능" 하단 화면의 `질문 추천` 클릭 시 진입되는 화면 진입 시 & "질문 대기" 화면의 `재밌는 질문 아이디어가 있어?` 버튼 클릭 시 진입되는 화면 진입 시              |
| 2    | view_timeline_tap                 | 1,194,508 | 타임라인 탭 진입               | → 타임라임 화면 진입                                                                                                                                                                           |
| 3    | $session_start                    | 1,036,852 | 앱 세션 시작 (앱 실행/복귀)    | → 단순 앱 시작                                                                                                                                                                                 |
| 4    | launch_app                        |   986,388 | 앱 실행 시점                   | → 단순 앱 실행 시 동시에 출력                                                                                                                                                                  |
| 5    | click_question_open               |   816,801 | 질문 상세 화면 열기            | → (3)Ping 피그마 탭의 "PING" 화면의 임의의 질문 클릭 (클릭 시 (3)PING 피그마탭의 "상세" 화면으로 이동하는 것으로 추정)                                                                         |
| 6    | click_bottom_navigation_questions |   769,163 | 하단 “질문” 탭 클릭            | → ???                                                                                                                                                                                          |
| 7    | click_bottom_navigation_profile   |   653,507 | 하단 “프로필” 탭 클릭          | → ???                                                                                                                                                                                          |
| 8    | $session_end                      |   649,658 | 앱 세션 종료 (백그라운드 등)   | → 단순 앱 종료                                                                                                                                                                                 |
| 9    | click_bottom_navigation_timeline  |   536,051 | 하단 “타임라인” 탭 클릭        | → ???                                                                                                                                                                                          |
| 10   | skip_question                     |   454,981 | 질문 스킵(넘기기) 클릭         | → (2)홈→질문 피그마 탭의 "질문" 창의 `건너뛰기` 버튼 클릭                                                                                                                                      |
| 11   | click_bottom_navigation_lab       |   453,683 | 하단 “랩” 탭 클릭              | → ???                                                                                                                                                                                          |
| 12   | view_profile_tap                  |   413,294 | 프로필 탭 진입                 | → (6) 프로필 피그마 탭의 "내 프로필" 화면 진입                                                                                                                                                 |
| 13   | view_questions_tap                |   353,400 | 질문 탭 진입                   | → (2)홈→질문 피그마 탭의 "질문" 화면 진입 (`click_question_start` 이후에 나오는 로그일 가능성)                                                                                                 |
| 14   | click_appbar_alarm_center         |   253,541 | 상단 알림 센터 진입            | → (2)홈→질문 피그마 탭의 "시작 가능" 화면의 좌측 상단 `PING` 버튼 클릭 (클릭 후 (3)PING 피그마 탭의 "PING" 화면으로 이동하는 것으로 추정)                                                      |
| 15   | click_notice_detail               |   229,358 | 공지사항 상세 보기             | → (2)홈→질문 피그마 탭의 "시작 가능" 화면의 상단 `확성기 배너` 클릭                                                                                                                            |
| 16   | click_question_start              |   220,385 | 질문 시작 버튼 클릭            | → (2)홈→질문 피그마 탭의 "시작 가능" 화면의 `START` 버튼 클릭                                                                                                                                  |
| 17   | click_random_ask_shuffle          |   184,217 | 랜덤 질문 섞기 클릭            | → ??? (2)홈→질문 피그마 탭의 "질문" 화면에 `이름 셔플` 버튼 외 셔플 버튼이 보이지 않음                                                                                                         |
| 18   | click_attendance                  |   157,737 | 출석 이벤트 클릭               | → (2)홈→질문 피그마 탭의 "시작 가능" 화면에 우측 하단 `출석체크` 버튼 클릭                                                                                                                     |
| 19   | complete_question                 |   154,105 | 질문 완료(제출)                | → (2)홈→질문 피그마 탭의 "완료" 화면 출력과 동시에 생성되는 것으로 추정                                                                                                                        |
| 20   | click_appbar_chat_rooms           |   148,422 | 채팅방 보기                    | → (3)PING 피그마 탭의 "1.6.0 업데이트 <채팅 추가>" 화면에서 3 번째 화면 하단 `채팅방 열기 ♥200` 버튼 클릭                                                                                      |
| 21   | click_question_ask                |   136,766 | 질문 물어보기 클릭             | → (3)PING 피그마 탭의 "상세" 화면의 `핑에게 답장하기` 버튼 클릭? ▲                                                                                                                             |
| 22   | click_question_share              |    69,241 | 질문 공유 클릭                 | → (3)PING 피그마 탭의 "답장 완료" 화면의 `공유하기` 버튼 클릭? ▲                                                                                                                               |
| 23   | click_timeline_chat_start         |    50,186 | 타임라인 채팅 시작 클릭        | → ???                                                                                                                                                                                          |
| 24   | click_appbar_friend_plus          |    49,545 | 친구 추가 버튼 클릭            | → (8)친구+ 피그마 탭의 "친구+" 화면의 `친구추가` 버튼 클릭                                                                                                                                     |
| 25   | view_login                        |    49,275 | 로그인 화면 진입               | → (1)온보딩 피그마 탭의 "기존 계정 로그인 인증" 좌측 화면 진입                                                                                                                                 |
| 26   | click_appbar_setting              |    26,685 | 설정 버튼 클릭                 | → (6)프로필 피그마 탭의 "내 프로필" 화면의 우측 상단 `톱니바퀴` 버튼 클릭? ▲                                                                                                                   |
| 27   | view_shop                         |    26,607 | 상점(하트샵) 화면 진입         | → (7)하트 충전소 피그마 탭의 "하트 충전소" 좌측 화면 진입                                                                                                                                      |
| 28   | view_signup                       |    25,630 | 회원가입 화면 진입             | → (1)온보딩 피그마 탭의 "학교 선택" 좌측 화면 진입                                                                                                                                             |
| 29   | click_random_ask_normal           |    18,653 | 랜덤 질문(일반모드) 요청       | → ???                                                                                                                                                                                          |
| 30   | click_profile_ask                 |    14,627 | 프로필에서 질문하기 클릭       | → 프로필 하단에 자주 걸리는 질문 top3 그 질문인가???? 아직 애매함                                                                                                                              |
| 31   | click_purchase                    |    13,039 | 구매 버튼 클릭                 | → (7)하트 충전소 피그마 탭의 "하트 충전소" 좌측 화면 아이템들 중 하나 클릭 후 아마도 구매하기 버튼 나오면 그거 눌렀을때??? ▲                                                                   |
| 32   | click_random_ask_other            |    11,075 | 다른 유저에게 랜덤 질문 보내기 | → ???                                                                                                                                                                                          |
| 33   | view_home_tap                     |     5,392 | 홈 탭 진입                     | → (2)홈→질문 피그마 탭의 "시작 가능" 화면 진입                                                                                                                                                 |
| 34   | click_friend_invite               |     3,221 | 친구 초대 버튼 클릭            | → (8)친구+ 피그마 탭의 "친구+" 화면의 초대 가능한 친구 목록에서 `초대하기` 버튼 클릭                                                                                                           |
| 35   | complete_purchase                 |     2,201 | 결제 완료                      | → 피그마에서 결제 완료 화면이 나오지 않지만, click_purchase 해당 로그 등장 후 완료 시 해당 로그 발생으로 추정 ▲                                                                                |
| 36   | click_copy_profile_link_profile   |     1,703 | 프로필 링크 복사 클릭          | → (6)프로필 피그마 탭의 "내 프로필" 화면에서 `프로필 링크` 버튼 클릭                                                                                                                           |
| 37   | click_community_chat              |     1,335 | 커뮤니티 채팅방 진입           | → (4)(메시지 (1.6.0 업데이트 추가) 피그마 탭의 "상대가 누군지 모르는 경우" 화면 진입 시 ▲                                                                                                      |
| 38   | click_invite_friend               |     1,054 | 친구 초대 팝업/링크 공유       | → (2)홈→질문 피그마 탭의 "실행 불가 - 친구 수가 적음" & "실행 불가 - 같은 학교 유저가 40명 미만" / (3)PING "받은 PING이 없는 경우" 화면의 `초대 링크 복사` 버튼 클릭                           |
| 39   | complete_signup                   |       974 | 회원가입 완료                  | → (1)온보딩 피그마 탭의 "알림 권한 등록" 화면 진입 시                                                                                                                                          |
| 40   | click_autoadd_contact             |       918 | 연락처 자동 추가 버튼 클릭     | → (1)온보딩 피그마 탭의 "자동 친구 추가" 화면의 `자동으로 친구추가` 버튼 클릭                                                                                                                  |
| 41   | button                            |       428 | 일반 버튼 클릭(비분류)         | → ????                                                                                                                                                                                         |
| 42   | click_copy_profile_link_ask       |        40 | 프로필 링크 복사???? 클릭?     | → ????                                                                                                                                                                                         |
| 43   | view_friendplus_tap               |         7 | 친구추가 탭 진입               | → (8)친구+ 피그마 탭의 "친구+" 화면 진입                                                                                                                                                       |
| 44   | click_notice                      |         1 | 공지사항 리스트 진입 클릭      | → ??? (2)홈→질문 피그마 탭의 "시작 가능" 화면의 상단 `확성기 배너` 클릭 했을 때 리스트가 나오는건지? 그렇다고 보기엔 횟수가 너무 적어서 상단 다른 이벤트에 같은 뜻으로 해석한 이벤트 값이 있음 |

<br>

### 3. 세션별 이벤트 수 및 일평균 세션 규모

| 순위 | 이벤트명 (`event_key`)              | 고유 세션 수 | 일평균 세션 수 | 주요 의미 / 특징 요약                                                     |
| ---- | ----------------------------------- | -----------: | -------------: | ------------------------------------------------------------------------- |
| 1    | `$session_start`                    |      252,877 |       10,536.5 | 앱 실행 시 자동 발생하는 세션 시작 이벤트. 전체 세션 중 거의 대부분 존재. |
| 2    | `launch_app`                        |      251,179 |       10,465.8 | 앱 런칭 시점에 함께 발생. `$session_start`와 짝지어 나타나는 경향.        |
| 3    | `$session_end`                      |      201,549 |        8,397.9 | 앱 종료 이벤트. 세션의 종료를 의미.                                       |
| 4    | `view_lab_tap`                      |      177,248 |        7,385.3 | 실험실(Lab) 탭 진입. 가장 많이 진입되는 메뉴 중 하나.                     |
| 5    | `click_bottom_navigation_questions` |      171,524 |        7,146.8 | 질문 탭 클릭. 주요 활동 유입 경로 중 하나.                                |
| …    | …                                   |            … |              … | …                                                                         |

- **인사이트**
  - 앱 실행/종료(`launch_app`, `$session_start`, `$session_end`) 관련 이벤트가 전체 세션의 중심을 차지  
     → 유저의 이용 주기(앱 접속 빈도) 확인 가능.
  - `view_lab_tap`, `view_timeline_tap` 등 **탭 이동 이벤트** 비중이 높음  
     → 앱 내 탐색 중심의 사용 패턴을 보여줌
  - 뭔가 흐름을 파악할 수 있는 인사이트가 나오지 않아 각 이벤트들의 규모 측정 정도로만 확인(5위까지 작성된 이유)

<br>

### 4. 이벤트 간 전이(Transition) 분석

> **각 세션 내 이벤트 발생 순서를 시간순으로 정렬**하여,  
> **“각 이벤트 이후 가장 자주 등장하는 다음 이벤트(Top3)”** 를 집계한 결과
> 이를 통해 **유저의 실제 앱 내 이동 흐름** 을 파악해보고,
> 행동 전환 지점 중심으로 패턴을 확인 해 보고자 해당 분석 진행

| 순위 | 기준 이벤트 (`event_key`)         | 1위 후속 이벤트                   | count_1 | 2위 후속 이벤트                   | count_2 | 3위 후속 이벤트                   | count_3 |
| ---- | --------------------------------- | --------------------------------- | ------: | --------------------------------- | ------: | --------------------------------- | ------: |
| 1    | click_question_open               | click_question_open               | 479,386 | click_question_share              |  59,539 | view_timeline_tap                 |  38,053 |
| 2    | $session_start                    | launch_app                        | 448,181 | $session_end                      | 116,002 | $session_start                    |  56,607 |
| 3    | launch_app                        | $session_start                    | 423,833 | $session_end                      | 123,861 | launch_app                        |  53,731 |
| 4    | $session_end                      | $session_start                    | 377,535 | launch_app                        | 247,087 | view_login                        |   7,434 |
| 5    | skip_question                     | skip_question                     | 326,333 | complete_question                 |  99,290 | $session_end                      |   8,349 |
| 6    | view_timeline_tap                 | view_lab_tap                      | 296,761 | click_bottom_navigation_timeline  | 190,089 | click_bottom_navigation_questions | 130,486 |
| 7    | view_lab_tap                      | view_timeline_tap                 | 270,209 | click_bottom_navigation_profile   | 199,042 | click_bottom_navigation_lab       | 186,208 |
| 8    | click_bottom_navigation_profile   | view_lab_tap                      | 201,144 | view_profile_tap                  | 129,439 | view_timeline_tap                 |  94,503 |
| 9    | click_bottom_navigation_timeline  | view_timeline_tap                 | 199,485 | view_lab_tap                      |  78,108 | click_bottom_navigation_questions |  73,255 |
| 10   | click_bottom_navigation_lab       | view_lab_tap                      | 194,969 | click_bottom_navigation_profile   |  73,530 | view_timeline_tap                 |  69,897 |
| 11   | click_random_ask_shuffle          | click_random_ask_shuffle          | 170,966 | click_random_ask_normal           |   3,566 | click_random_ask_other            |   2,252 |
| 12   | click_appbar_alarm_center         | click_notice_detail               | 155,083 | click_bottom_navigation_questions |  10,942 | click_appbar_alarm_center         |  10,504 |
| 13   | click_bottom_navigation_questions | view_timeline_tap                 | 132,751 | click_bottom_navigation_questions | 123,417 | view_questions_tap                | 105,602 |
| 14   | view_profile_tap                  | click_bottom_navigation_profile   | 116,776 | view_lab_tap                      | 115,579 | view_timeline_tap                 |  56,869 |
| 15   | click_question_start              | skip_question                     | 112,135 | complete_question                 |  53,861 | $session_end                      |   9,963 |
| 16   | view_questions_tap                | click_bottom_navigation_questions |  98,767 | view_timeline_tap                 |  87,088 | view_lab_tap                      |  38,801 |
| 17   | click_notice_detail               | click_notice_detail               |  69,841 | $session_end                      |  16,473 | click_bottom_navigation_questions |  15,844 |
| 18   | click_question_share              | click_question_open               |  40,894 | view_timeline_tap                 |   4,735 | $session_end                      |   4,137 |
| 19   | click_attendance                  | $session_end                      |  35,248 | click_question_start              |  19,785 | click_question_open               |  19,374 |
| 20   | complete_question                 | $session_end                      |  27,810 | click_question_open               |  20,219 | view_timeline_tap                 |  17,867 |
| 21   | click_appbar_chat_rooms           | click_appbar_alarm_center         |  24,787 | $session_end                      |  14,864 | click_appbar_chat_rooms           |  12,234 |
| 22   | click_question_ask                | view_lab_tap                      |  21,281 | click_bottom_navigation_timeline  |  19,930 | click_bottom_navigation_lab       |  18,344 |
| 23   | view_signup                       | view_signup                       |  17,115 | view_login                        |   4,040 | $session_end                      |   2,156 |
| 24   | click_timeline_chat_start         | click_timeline_chat_start         |  12,794 | view_lab_tap                      |   8,598 | $session_end                      |   4,186 |
| 25   | view_login                        | $session_end                      |  11,965 | click_question_open               |  10,919 | $session_start                    |   7,679 |
| 26   | view_shop                         | click_purchase                    |   9,309 | launch_app                        |   4,831 | $session_end                      |   1,950 |
| 27   | click_appbar_friend_plus          | $session_end                      |   5,724 | view_lab_tap                      |   5,330 | view_timeline_tap                 |   4,246 |
| 28   | click_appbar_setting              | view_lab_tap                      |   5,500 | $session_end                      |   3,880 | click_bottom_navigation_questions |   2,609 |
| 29   | click_random_ask_normal           | click_random_ask_shuffle          |   3,793 | view_lab_tap                      |   1,945 | click_random_ask_normal           |   1,843 |
| 30   | click_purchase                    | click_purchase                    |   3,445 | complete_purchase                 |   2,127 | view_timeline_tap                 |     871 |
| 31   | click_profile_ask                 | view_lab_tap                      |   2,889 | click_profile_ask                 |   1,976 | $session_end                      |   1,201 |
| 32   | click_random_ask_other            | click_random_ask_shuffle          |   1,977 | click_random_ask_normal           |   1,621 | view_lab_tap                      |   1,064 |
| 33   | view_home_tap                     | launch_app                        |   1,660 | $session_end                      |   1,562 | $session_start                    |     964 |
| 34   | click_friend_invite               | click_invite_friend               |     571 | view_timeline_tap                 |     265 | $session_end                      |     255 |
| 35   | complete_signup                   | $session_start                    |     415 | view_timeline_tap                 |     118 | click_question_start              |      91 |
| 36   | complete_purchase                 | view_timeline_tap                 |     364 | view_lab_tap                      |     283 | click_question_open               |     256 |
| 37   | click_copy_profile_link_profile   | view_lab_tap                      |     346 | click_appbar_setting              |     323 | $session_end                      |     148 |
| 38   | click_community_chat              | view_timeline_tap                 |     316 | click_community_chat              |     215 | view_profile_tap                  |     171 |
| 39   | click_invite_friend               | click_invite_friend               |     224 | click_friend_invite               |     133 | launch_app                        |     124 |
| 40   | click_autoadd_contact             | view_lab_tap                      |     139 | click_bottom_navigation_profile   |      97 | click_autoadd_contact             |      78 |
| 41   | button                            | button                            |     118 | launch_app                        |     114 | $session_end                      |      83 |
| 42   | click_copy_profile_link_ask       | click_bottom_navigation_questions |       6 | view_lab_tap                      |       5 | click_bottom_navigation_profile   |       4 |
| 43   | view_friendplus_tap               | view_questions_tap                |       3 | launch_app                        |       1 | $session_end                      |       1 |
| 44   | click_notice                      | click_notice_detail               |       1 | –                                 |       – | –                                 |       – |

<br>

- **앱 기동 흐름**

  - `$session_start`, `launch_app`, `$session_end` 세 이벤트가 **세션 구조의 뼈대**를 이룸.
  - 반복적으로 상호 전이되어 “앱 실행 → 앱 종료” 패턴이 명확히 드러남.
  - 동일 시점에 중복 로깅되는 구조적 특성도 존재 (`launch_app` ↔ `$session_start`).

- **탭 간 순환 행동 패턴**

  - `view_lab_tap`, `view_timeline_tap`, `click_bottom_navigation_*` 계열 간의 전이가 빈번함.
  - 이는 유저가 **여러 탭을 오가며 탐색하는 행동 습관**을 보여줌.
  - 특히 `view_lab_tap ↔ view_timeline_tap` 간 이동이 가장 많아 **핵심 네비게이션 루프**로 해석 가능.

- **질문 관련 이벤트 흐름**

  - `click_question_start → skip_question → complete_question` 경로가 빈번함.
  - 일부 세션에서는 `click_question_open → click_question_open` 반복 패턴 → 유저가 **여러 질문을 연속 조회**함을 의미.
  - `click_question_share`나 `view_timeline_tap`으로 이어지는 흐름은 **질문 공유/확산 행동**으로 이어짐.

- **결제 관련 행동 경로**

  - `view_shop → click_purchase → complete_purchase` 구조가 명확히 확인됨.
  - 다만 전체 전이 비중은 낮음 → 결제 유저는 전체 중 소수임을 시사.

- **탐색 외 기능(설정/알림/친구초대 등)**

  - `click_appbar_alarm_center → click_notice_detail` 비율이 높음 → 알림 클릭 후 상세 공지로 이동하는 일반적 경로.
  - `click_appbar_setting`, `click_appbar_friend_plus` 등은 주로 세션 종료 전 후속 이벤트(`$session_end`)로 마무리됨.

- **전이의 구조적 특징**
  - 상위 10여 개 이벤트가 대부분 자기 자신 혹은 상호 반복되는 전이로 구성됨.
  - 이는 유저가 **특정 화면 내 반복 행동을 자주 수행**하거나,  
    **앱 네비게이션이 한정된 루프 구조로 설계**되어 있음을 반영함.

<br>

#### 아직 해당 테이블을 마무리 하지 못했기에 이어서 분석 예정

---

## \* 사용했던 코딩

### 각 세션별 이벤트 순서를 고려해서, 모든 세션을 합산한 후 각 이벤트의 후속 이벤트 빈도를 집계하고, 그 중 Top3를 구하는 것

```sql
WITH ordered_events AS (
    SELECT
        session_id,
        event_datetime,
        event_key,
        LEAD(event_key) OVER (PARTITION BY session_id ORDER BY event_datetime) AS next_event_key
    FROM final.hackle_events
),
transition_counts AS (
    SELECT
        event_key,
        next_event_key,
        COUNT(*) AS transition_count
    FROM ordered_events
    WHERE next_event_key IS NOT NULL
    GROUP BY event_key, next_event_key
),
ranked AS (
    SELECT
        event_key,
        next_event_key,
        transition_count,
        ROW_NUMBER() OVER (PARTITION BY event_key ORDER BY transition_count DESC) AS rnk
    FROM transition_counts
)
SELECT
    event_key,
    MAX(CASE WHEN rnk = 1 THEN next_event_key END) AS next_event_1,
    MAX(CASE WHEN rnk = 1 THEN transition_count END) AS count_1,
    MAX(CASE WHEN rnk = 2 THEN next_event_key END) AS next_event_2,
    MAX(CASE WHEN rnk = 2 THEN transition_count END) AS count_2,
    MAX(CASE WHEN rnk = 3 THEN next_event_key END) AS next_event_3,
    MAX(CASE WHEN rnk = 3 THEN transition_count END) AS count_3
FROM ranked
WHERE rnk <= 3
GROUP BY event_key
ORDER BY count_1 DESC;
```

---

---

## \*문제점

- 행동 로그 데이터 테이블의 분석 과정을 진행할 때 전달받은 피그마 와이어프레임에서 어떤 행동이 각 `event_key`에 해당되는지 파악하는 것이 오래 걸렸음 (아직 파악(추측)하지 못한 이벤트 키도 존재)

- 어떤 분석을 진행해야지 로그 데이터를 활용하여 유용한 인사이틀 얻을지 생각 중이지만, 뭔가 시원하게 이어나가지 못하고 있음

<BR>

## \* 회고

- 위 테이블을 분석할 때 다른 테이블 보다 훨씬 진도가 느려졌음 이벤트 로그들이 정확히 어떤 행동인지 파악하고 정리하느라 시간을 소비함
- 이어서 분석할 땐, 분석 순서를 팀원과 의논해서 정리를 해본 후 진행 해야 할 것 같음
