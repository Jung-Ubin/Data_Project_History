# Day - 13 협업 일지(고급)

#### 일자: 25-10-29 / 정유빈

---

### 팀원들과 논의한 일

- 각자 정한 분석 방향으로 분석 진행하면서 공유할 내용 있으면 공유하기

<br>

## \* 오늘 + 내가 한 일

### `session_count` == `1`(앱을 한 번만 사용한 단발성 유저) 의 `event_flow` 만들기

- `devcie_user_id_summary` 테이블에서 `session_count` = `1` 인 유저의 테이블을 따로 제작 후,
- 해당 테이블에 `event_flow` 와 `event_count` 를 생성하여 패턴 분석하고자 함
- **단발성 유저들이 많이 사용한 경로 확인** 후 해당 부분에 대한 개선, 보완점을 찾아보자 생각함

<br>

### `PrefixSpan`(min_support=1000) 확인 시, 분석 방법 내 단점 발견

- 패턴으로써 가치가 없는(`$session_start`, `launch app` 등) 키들이 존재
- 분석할 때 노이즈가 껴서, 내가 보고싶은 키들의 패턴을 확인하지 못함

<br>

### 필요없는 `event_key` 를 삭제하고 진행

- 앱을 사용할 때, 핵심 가치를 느낄 수 있는 키들 외 일부 서브 키들은 배제를 하고,
- 테이블을 다시 생성하여, `PrefixSpan` 을 사용하여, 패턴 분석 예

---

## \* 사용했던 코딩

### 만들었던 `event_flow`가 시간 순서대로 잘 정렬이 되어있는지 확인

- 테이블 내 `session_id` 랜덤하게 5개씩 뽑고, `hackle_events` 테이블의 `event_datetime` 과 비교해서 확인
- `df3_sorted` = `hackle_events` 내 필요한 컬럼 빼온 후 정렬한 테이블

```python
import random

sample_count = 5
device_ids = outlier_session_1_log_df['device_id'].unique().tolist()
random_sample = random.sample(device_ids, min(sample_count, len(device_ids)))

check_results = []

for dev_id in random_sample:
    row = outlier_session_1_log_df[outlier_session_1_log_df['device_id'] == dev_id].iloc[0]
    session_id = row['session_id']
    flow_str = row['event_flow']
    flow_list = flow_str.split(',') if isinstance(flow_str, str) else []

    # ✅ 정답 flow (df3_sorted에서 이벤트 순서 추출)
    df3_tmp = df3_sorted[df3_sorted['session_id_01'] == session_id]
    true_flow_list = df3_tmp['event_key_01'].tolist()

    check_results.append({
        'device_id': dev_id,
        'session_id': session_id,
        'flow_len': len(flow_list),
        'true_len': len(true_flow_list),
        'check_result': "✅ O" if flow_list == true_flow_list else "❌ X"
    })

result_df = pd.DataFrame(check_results)
print(result_df)
```

<br>

```python

# 예시
         device_id                            session_id

0  E4D919EB-B4AE-445A-9DA3-862143CF9685          WEzQN2EcriQ7q8fHLgRvvrBd9Lf1
1  114AB4DB-8D0F-4077-ADAA-661FA677484D          9tJT9LgW25aR1UyQqqU5mBsmSmx1
2  690DA893-8B14-4580-BB4D-B7FB4D4448E0          KBU2jlUOH0RSbe3zWBiPVLauRhE2
3  71eb42fd-8d88-4087-acf4-b84ef18cfb24          pTUx2y8pwHexfFdfYiYDXYJ5QsM2
...



   flow_len   true_len   check_result
0    10          10          ✅ O
1    37          37          ✅ O
2    49          49          ✅ O
3    13          13          ✅ O
4    15          15          ✅ O
```

---

## \*문제점

- SQL에서 작업할 때, 워낙 테이블이 크기 때문에 분석 진행 속도가 많이 느려졌었음.
- 일단 사용자들의 패턴을 분석해서 아이템을 만드는 생각을 하고있지만, 패턴 역시도 뻔한 결과로 나오면 아이템을 어떻게 만들어야될지 고민중
- 어떤 분석과 패턴을 또 연결 시켜보면 좋을지도 고민 중

<BR>

## \* 회고

- 테이블 자체가 너무 커서 python에서는 활용을 못할 줄 알았는데 오히려 저런 작업들은 SQL보다 빨라서 신기했다.
- 테이블이 크지만, 복잡한 계산이 들어가야하는 부분은 파이썬으로 해결해야겠다.
- 패턴을 보고나서 어떤 분석으로 또 연결 시킬지, 개선, 보완점을 어떻게 만들어볼지 생각해봐야겠다.
