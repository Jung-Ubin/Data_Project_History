# Day - 15 협업 일지(고급)

#### 일자: 25-10-31 / 정유빈

---

### 팀원들과 논의한 일

- 각자 정한 분석 방향으로 분석 진행하면서 공유할 내용 있으면 공유하기

<br>

## \* 오늘 + 내가 한 일

### 3-Step / 2-Step 패턴 확인 후 분석

| 이벤트 키                   | 의미                   |
| --------------------------- | ---------------------- |
| `complete_purchase`         | 결제 완료              |
| `click_purchase`            | 결제 버튼 클릭         |
| `view_shop`                 | 상점/결제 화면 진입    |
| `complete_question`         | 질문 정상 제출         |
| `click_question_start`      | 질문 시작 버튼 클릭    |
| `click_question_ask`        | 질문 작성 화면 진입    |
| `click_question_open`       | 질문 상세 진입         |
| `click_timeline_chat_start` | 타임라인에서 채팅 시작 |
| `click_community_chat`      | 커뮤니티 채팅 진입     |
| `click_profile_ask`         | 프로필에서 질문하기    |

<BR>

- 위 정리한 키만 사용하여, 유저들의 패턴 분석

- `min_support` = 1000 설정

- `maxlen` = 3 설정

- 전처리 후 174,184명의 유저 대상으로 패턴 분석 진행

- 해당 유저들의 앱 사용률 분포 확인 시 아래와 같이 단발성 유저들이 대부분
  > 1회 사용 유저 비율: **59.75%**  
  > 2회 사용 유저 비율: 19.90%  
  > 5회 이상 사용 유저 비율: 8.40%  
  > 상위 1% 사용 횟수: 20.0회

<BR>

- 패턴을 추출한 후 의미 단위로 나눠서 해석 진행함

- 단발성 유저들의 대부분의 특징이 뭘까?
- 아래 인사이트 확인 시 질문 컨텐츠 자체의 **유저 흥미도가 한 번 사용 후 빠르게 떨어지는 것**으로 보여짐

---

### 3-Step / 2-Step 패턴 확인 후 분석

| 이벤트 키                   | 의미                   |
| --------------------------- | ---------------------- |
| `complete_purchase`         | 결제 완료              |
| `click_purchase`            | 결제 버튼 클릭         |
| `view_shop`                 | 상점/결제 화면 진입    |
| `complete_question`         | 질문 정상 제출         |
| `click_question_start`      | 질문 시작 버튼 클릭    |
| `click_question_ask`        | 질문 작성 화면 진입    |
| `click_question_open`       | 질문 상세 진입         |
| `click_timeline_chat_start` | 타임라인에서 채팅 시작 |
| `click_community_chat`      | 커뮤니티 채팅 진입     |
| `click_profile_ask`         | 프로필에서 질문하기    |

<BR>

- 위 정리한 키만 사용하여, 유저들의 패턴 분석

- `min_support` = 1000 설정

- `maxlen` = 3 설정

- 전처리 후 174,184명의 유저 대상으로 패턴 분석 진행

- 해당 유저들의 앱 사용률 분포 확인 시 아래와 같이 단발성 유저들이 대부분
  > 1회 사용 유저 비율: **59.75%**  
  > 2회 사용 유저 비율: 19.90%  
  > 5회 이상 사용 유저 비율: 8.40%  
  > 상위 1% 사용 횟수: 20.0회

<BR>

- 패턴을 추출한 후 의미 단위로 나눠서 해석 진행함

- 단발성 유저들의 대부분의 특징이 뭘까?
- 아래 인사이트 확인 시 질문 컨텐츠 자체의 **유저 흥미도가 한 번 사용 후 빠르게 떨어지는 것**으로 보여짐

---

### 3-Step 패턴 의미 단위 분류 및 분석

#### 1. 질문 생성/참여 패턴 (Core Usage)

- 이벤트 키 패턴 대부분이 여기에 포함됨

<br>

| 대표 패턴                                                        |  비율 |
| ---------------------------------------------------------------- | ----: |
| `click_question_open → click_question_start → complete_question` | 1.82% |
| `view_questions_tap → click_question_start → complete_question`  | 1.17% |

<br>

> `질문을 열어보고 → 질문 시작 → 질문 완성`  
> **올바른 질문 생성 흐름이 상위권**  
> 질문 중심의 탐색 및 반복 사용 행동 강함

---

#### 2. 질문 반복 탐색 패턴 (Wandering / Exploration)

- 완료 없이 계속 질문을 열어보고 이동하는 유형

<br>

| 대표 패턴                                                          |  비율 |
| ------------------------------------------------------------------ | ----: |
| `view_questions_tap → click_question_open → view_questions_tap`    | 0.96% |
| `click_question_open → click_question_start → click_question_open` | 0.81% |

<br>

> 유저가 **질문을 둘러보기만 하고 끝내지 않는 흐름**  
> 이는 `전환 개선 기회`가 될 수 있음  
> 어디서 이탈하는지 체크 → UI 개선

---

#### 3. 질문 → 상점(결제) 전환 패턴 (Low frequency)

| 대표 패턴                                           |  비율 |
| --------------------------------------------------- | ----: |
| `click_question_start → view_shop → click_purchase` | 0.17% |
| `view_questions_tap → view_shop → click_purchase`   | 0.16% |

<br>

> 질문 활용 → 상점 → 구매 클릭 연결은 있으나 빈도는 낮음  
> 결제를 유도할 아이템, 앱 흥미도가 부족하다 판단됨

---

#### 4. 질문 → 채팅 유도 패턴 (Small but interesting)

| 대표 패턴                                                              |  비율 |
| ---------------------------------------------------------------------- | ----: |
| `view_questions_tap → click_timeline_chat_start → view_questions_tap`  | 0.28% |
| `click_question_start → complete_question → click_timeline_chat_start` | 0.19% |

<br>

> 질문 → 커뮤니티 소통 가능성  
> 리텐션 강화 요인이지만 지표는 약함

---

#### 3-Step 인사이트 요약

| 카테고리            |          비중 | 해석                       |
| ------------------- | ------------: | -------------------------- |
| 질문 생산 플로우    | **매우 높음** | 앱의 핵심 경험             |
| 질문 탐색 반복      |      **높음** | 전환 지점 개선 여지        |
| 질문 완료 이후 유지 |          보통 | Retention 전략 중요 영역   |
| 상점/구매 흐름      |          낮음 | **구매 유도 UX 개선 필요** |
| 채팅/커뮤니티 전환  |          낮음 | Engagement 확장 가능성     |

<BR>

---

---

<BR>

## 2-Step 패턴 의미 별 분류 및 분석

| 카테고리                | 포함 이벤트 키                            | 의미 요약             |
| ----------------------- | ----------------------------------------- | --------------------- |
| **A. 질문 완성 퍼널**   | click_question_start / complete_question  | 질문 → 완성           |
| **B. 질문 탐색/반복**   | view_questions_tap / click_question_open  | 질문 열기/탐색        |
| **C. 질문 작성 흐름**   | click_question_ask / click_question_start | 질문 작성안 진입 흐름 |
| **D. 질문 후 후속행동** | complete_question → X                     | 리텐션 흐름           |
| **E. 상점/결제**        | view_shop / click_purchase                | Monetization          |
| **F. 채팅/소셜 전환**   | click_timeline_chat_start                 | 커뮤니티 소통         |

---

#### 1. 질문 완성 퍼널

| 패턴                                         |      비율 |
| -------------------------------------------- | --------: |
| `click_question_start` → `complete_question` | **5.93%** |

<BR>

> 가장 중요한 퍼널  
> 질문 작성 유도 UI 최적화 필요

---

#### 2. 질문 탐색/반복 패턴

| 패턴                                         |  비율 |
| -------------------------------------------- | ----: |
| `click_question_open` → `view_questions_tap` | 2.24% |
| `view_questions_tap` → `click_question_open` | 2.37% |

<BR>

> 질문을 열어보고 닫는 반복  
> 전환 저하 포인트(이탈 위험)

---

#### 3. 질문 작성 흐름 전개

| 패턴                                           |  비율 |
| ---------------------------------------------- | ----: |
| `click_question_open` → `click_question_start` | 2.37% |
| `click_question_start` → `click_question_open` | 2.10% |

<BR>

> 진입과 이탈이 뒤섞임  
> 입력 전 고민/회피 행동

---

#### 4. 상점/결제 전환 패턴

| 패턴                                  |  비율 |
| ------------------------------------- | ----: |
| view_shop → click_purchase            | 0.33% |
| click_question_start → click_purchase | 0.17% |

<BR>

> 구매 퍼널 매우 약함

---

#### 5. 채팅 흐름 패턴

| 패턴                                           |  비율 |
| ---------------------------------------------- | ----: |
| click_timeline_chat_start → view_questions_tap | 0.56% |
| view_questions_tap → click_timeline_chat_start | 0.43% |

<BR>

> 질문 → 채팅 연결

---

#### 2-Step 인사이트 요약

| 카테고리          |        비중 | 해석                 |
| ----------------- | ----------: | -------------------- |
| 1. 질문 완성 퍼널 | **매우 큼** | 앱 핵심 가치         |
| 2. 질문 탐색 반복 |      **큼** | 이탈 방지 필요       |
| 3. 작성 진입 흐름 |          큼 | 전환 유도 필요       |
| 4. 구매 퍼널      |        낮음 | 상점 노출 개선 필요  |
| 5. 소셜 전환      |        낮음 | Engagement 확장 가능 |

---

## 유저 행동 패턴 분석 인사이트 요약

```SCSS
|앱 실행 (`launch_app`)
브랜치_1
|  |→ 질문 화면 진입 (`view_questions_tap`, `click_bottom_navigation_questions`)
|  | |→ 질문 탐색(질문 고르기) (리스트/상세 반복) (`click_question_open`)
|  | | |→ 질문 문답 진행 (`click_question_start`)
|  | | | |→ 질문 완료 (`complete_question`)
|  | | | | |→ (채팅 소통) (`click_timeline_chat_start`)
|  | | |↘ 문답 중 이탈 (`view_questions_tap`)
|  | | | |→ 탐색으로 회귀 (`click_question_open`)
|  | | | | |→ 종료 가능성 ↑ (`$session_end`)
브랜치_2
|  |→ 질문 수신 확인 (`click_appbar_alarm_center`)
|  | |↘ 결제 시도 (극 소수 유저) (`view_shop`)
|  | | |→ 상점 진입 → 구매 클릭 (`click_purchase`)
|  | | | |→ 구매 완료는 매우 낮음 (`complete_purchase`)
|  | |→ 결제 시도 없으면, 질문 돌아가서 브랜치 1 순서 진행 (`view_questions_tap`, `click_bottom_navigation_questions`)
|  | | | | | |→ 종료 (`$session_end`)
```

<br>

- **유저의 핵심 행동은 질문을 받고 제출하는 흐름**에 집중된다.

- **질문을 보기만 하고 이탈하는 탐색 반복형 행동이 매우 많다** → 전환 저하 핵심 지점.

- **질문 문답 단계에서 입력 직전 이탈 비율이 높아짐**

- **질문 → 결제로 이어지는 퍼널은 매우 약하다**

- **질문 → 채팅 전환은 잠재적 리텐션 포인트지만 현재는 낮은 수준**

- **단발성(1회 사용) 유저가 60% 이상으로 재방문 구조가 취약**

- **질문 콘텐츠에 흥미 유지 실패 → 반복 이용자 확대 전략 필요**

- **상위 사용자라도 사용 횟수 상한이 낮아 장기 체류 기능이 부족**

- **질문 완료 이후 후속 행동 유도 기획 부족 → 소셜/커뮤니티 강화 (ex:업데이트내용에 들어간 채팅방 개설)**

- 콘텐츠 흐름이 **재미 유발보단 단순 Q&A 중심으로 제한되어 있어서, 흥미도 유지가 힘듦**

---

## \* 사용했던 코딩

### 만든 구조를 확인하기 위한 Sankey 다이어그램 그려보기

```python
# Jupyter Desktop / Google Colab 렌더러 설정
pio.renderers.default = "notebook"

# 한글 라벨 매핑
LABEL_KR = {
    'launch_app': '앱 실행',
    'question_view': '질문 화면',
    'question_open': '질문 탐색',
    'question_start': '질문 시작',
    'question_complete': '질문 완료',
    'alarm_center': '질문 수신',
    'view_shop': '결제 시도',
    'click_purchase': '구매 클릭',
    'complete_purchase': '구매 완료',
    'session_end': '앱 종료'
}

# 라벨 치환
sankey_data['source_kr'] = sankey_data['source'].map(LABEL_KR)
sankey_data['target_kr'] = sankey_data['target'].map(LABEL_KR)

# Sankey에서 사용할 노드 ID 생성
nodes = list(dict.fromkeys(list(sankey_data['source_kr']) + list(sankey_data['target_kr'])))
node_idx = {label: i for i, label in enumerate(nodes)}

# ID 매핑
sankey_data['s_id'] = sankey_data['source_kr'].map(node_idx)
sankey_data['t_id'] = sankey_data['target_kr'].map(node_idx)

# Sankey 그래프 생성
fig = go.Figure(data=[go.Sankey(
    arrangement="snap",
    node=dict(
        pad=25,
        thickness=22,
        label=nodes,
        line=dict(color="black", width=1),
        color="lightgray"
    ),
    link=dict(
        source=sankey_data['s_id'],
        target=sankey_data['t_id'],
        value=sankey_data['value'],
        color="rgba(90,90,255,0.4)"
    )
)])

fig.update_layout(
    title="유저 행동 흐름 Sankey Diagram\n(Branch1 질문 흐름 + Branch2 결제 흐름)",
    font_size=14,
    height=600,
    margin=dict(l=10, r=10, t=60, b=10)
)

 fig.show(renderer="notebook")
```

<br>

---

## \*문제점

- 오늘 유저의 핵심 행동 패턴의 기준을 잡을 수 있었다, 하지만 다이어그램 구조와 퍼널 구조를 아직 그려보질 못해서 확인이 더 필요한 상태다

<BR>

## \* 회고

- 오늘 팀원들과 이야기하며, 각자의 분석 인사이트를 이제 어떻게 녹여낼 것인지 논의해봤다. 아직 정리가 더 필요해보인다.
- 정리한 인사이트를 바탕으로 액션 아이템이나, 추가 분석 방향성을 생각해볼 예정이다.
