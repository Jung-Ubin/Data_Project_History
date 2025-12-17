# Day - 14 협업 일지(고급)

#### 일자: 25-10-30 / 정유빈

---

### 팀원들과 논의한 일

- 각자 정한 분석 방향으로 분석 진행하면서 공유할 내용 있으면 공유하기

<br>

## \* 오늘 + 내가 한 일

### 단발성 유저 재 정의

- 기존 : `session_count` 가 1인 유저들
- 문제점 발견 : 같은 `session` 내 `event_datetime` 을 확인했을 때, 가은 세션인데도 불구하고, **이전 → 다음 로그**의 시간 차이가 크게 나는것을 발견
- 변경
  - 1. `event_flow` 를 볼 때 필요 없는 `event_key` 를 지우고 다시 제작한 점을 고려
  - 2. shift 기법을 사용하여, 이전 로그와 다음 로그의 시간 차이가 **1시간 30분** 이상 나온다 가정했을 때 행을 분리하여 제작
  - 2-2. 같은 `session_id` 여도 `event_flow` 차이로 인해 행이 분리가 됨 (기존 한 줄 방식에서 변경)
  - 3. 다 만들어 졌다면, **같은 아이디끼리 시간 순으로 오름차순 정렬될 수 있게 다시 한번 정리**
  - 4. 정리 후 추가적인 컬럼인 `first_key`, `last_key` 를 각 행별로 추가하여, 앱을 실행 했을 때 마지막 키와 시작 키를 확인할 수 있게 제작
  - 5. 해당 테이블로 단발성 유저를 더 확실히 확인할 수 있고, 패턴을 조금 더 뚜렷하게 볼 수 있을 것 같다는 판단을 함.

---

### `session_count` = `1` 유저 세션 분리 작업

- 이전 이벤트와 시간 차이 계산
- **같은 user_id, 같은 session_id 내에서 이전 이벤트와 얼마나 시간이 벌어졌는지 측정**
- 이 값을 기준으로 **새로운 세션 시작 여부** 판단 가능
- 조건: 90분(= 90.0) 초과 시 NEW SESSION

<br>

- 다음과 같이 정리 완료  

![1761816297268](<image/Day14_협업일지_정유빈/1761816297268.png>)

<br>

### `session` 별 `evnet_flow` 생성

<br>

- 추후 활용할 수 있는 `first/last_evnet` 도 생성  
![1761816389264](<image/Day14_협업일지_정유빈/1761816389264.png>)

<br>

- 세션이 나눠질 때마다(`이전 ↔ 다음 로그 차이 90분이상`) 행을 분리하여 생성
- 사용자 패턴을 보다 쉽고 더 정확히 파악할 수 있게 설계

<br>

### 앱 사용량 분포 확인

- 기존 설정했던 가정 `session_count` 가 `1` 이면 단발성 유저
- 실제로도 단발성 유저가 많은지 확인

<br>

![1761816600227](<image/Day14_협업일지_정유빈/1761816600227.png>)

<br>

![1761816626556](<image/Day14_협업일지_정유빈/1761816626556.png>)

<br>

- 단발성 유저의 비율이 절반 이상을 차지하는 것을 확인

<br>

### `PrefixSpan` 활용하여, 패턴 확인

- `min_support` : 10만으로 설정 (그 이하로 할 시 너무 오래 걸림)
- 단일 이벤트가 아닌 **2개의 키가 연속적인 패턴만 찾게 설정**
- 동일 이벤트(A → A)패턴 제외
- TOP 20까지 볼 수 있는 결과로 출력

<BR>

| 컬럼               | 의미                                                   |
| ------------------ | ------------------------------------------------------ |
| `pattern_count`    | PrefixSpan 기준, **해당 패턴이 등장한 `전체 세션 수`** |
| `pattern_ratio(%)` | **전체 패턴에서 해당 패턴의 비율**                     |
| `pattern`          | A → B 형태의 최종 분석 패턴                            |
| `pattern_list`     | raw 리스트 형태                                        |
| `pattern_len`      | 이벤트 길이 (현재 2 또는 3)                            |

<BR>

![1761817042531](<image/Day14_협업일지_정유빈/1761817042531.png>)

<BR>

---

## \* 사용했던 코딩

### 자주 등장하는 패턴 순위별 정보 확인 (`event_pattern` 확인)

```python
# (1) 지지도 기준 내림차순 정렬
patterns_sorted = sorted(patterns, key=lambda x: x[0], reverse=True)

# (2) 길이 2 이상 + 모두 동일 이벤트(A→A) 패턴 제거
patterns_filtered = [
    (support, seq)
    for support, seq in patterns_sorted
    if len(seq) >= 2 and len(set(seq)) > 1
]

# (3) Top 20로 자르기
top_n = 20
patterns_top = patterns_filtered[:top_n]   # 여기서 선언됨!

# (4) Top20 총 패턴 발생 수
total_pattern_count = sum([support for support, _ in patterns_top])

# (5) 이벤트 패턴 테이블 생성
rows = []
for rank, (support, seq) in enumerate(patterns_top, start=1):
    rows.append({
        'rank': rank,
        'pattern_count': support,
        'pattern_ratio(%)': round((support / total_pattern_count) * 100, 4),
        'pattern': ' → '.join(seq),
        'pattern_list': seq,
        'pattern_len': len(seq),
    })

event_pattern = pd.DataFrame(rows)

event_pattern
```

<br>

---

## \*문제점

- 해당 테이블을 분석하면서, 원하는데로 결과가 출력되지 않아서, 해결하는 방법을 생각하는데 시간이 많이 걸림
- 단순하게 해결할 수 있는 문제를 너무 복잡하게 해결했음  
  (ex : 같은 이벤트 연속 등장 패턴 제외하는 법 → `if len(seq) >= 2 and len(set(seq)) > 1`)

<BR>

## \* 회고

- 패턴과 와이어프레임을 보면서 보완점과, 개선점을 발굴해보고,
- 새로운 분석 아이디어도 찾아봐야겠다.

