# Day - 23 협업 일지(고급)

#### 일자: 25-11-13 / 정유빈

---

### 팀원들과 논의한 일

- 발표자료 최종 개선 작업 진행
- 발표 대본 초안 작성 및 보고서 제출 준비

<br>

## \* 오늘 + 내가 한 일

### 발표자료 최종 개선 작업

- 텍스트가 많아서 눈에 잘 안들어오는 슬라이드 간추려서 제작
- 서식, 간격 등 조정

### 발표 대본 초안 작성

- 청취자가 최대한 발표자료를 보면서 이해하기 쉽게 대본 초안 작성
- 팀 대본 확인 후 발표 톤에 맟춰 수정
- 전체 발표 대본 초안 작성 완료

---

## \* 사용했던 코드

### 유저 결제 패턴 흐름 생키 데이터 생성

```python
# -------------------------------------------
# Branch 2 유저 수 계산 함수들
# -------------------------------------------

# 1) 보유 여부 기반 (result_3)
def count_has_events(events):
    return result_3[
        result_3['event_flow'].str.contains(events[0], na=False) &
        result_3['event_flow'].str.contains(events[1], na=False)
    ]['user_id'].nunique()


def count_has_all(events):
    cond = True
    for ev in events:
        cond &= result_3['event_flow'].str.contains(ev, na=False)
    return result_3[cond]['user_id'].nunique()


# 2) 순서 기반 (df_raw_2)
def count_ordered(events):
    cond = result_3['event_flow'].str.contains(events[0], na=False)
    prev_index = 0

    for e in events[1:]:
        cond &= result_3['event_flow'].str.contains(e, na=False)

    # 순서 비교
    order_users = []
    for _, row in result_3[cond].iterrows():
        seq = row['event_flow'].split(',')
        try:
            idx = [seq.index(ev) for ev in events]
            if idx == sorted(idx):
                order_users.append(row['user_id'])
        except:
            pass

    return len(set(order_users))


# -------------------------------------------
# Branch 2 숫자 계산
# -------------------------------------------

# b2_1 : launch_app & click_appbar_alarm_center 보유
b2_1 = count_has_events(['launch_app', 'click_appbar_alarm_center'])

# b2_1_1 : 순서 기반 (result_3)
b2_1_1 = count_ordered(['launch_app', 'click_appbar_alarm_center', 'view_questions_tap'])

# b2_2 : 보유 여부 기반 (result_3)
b2_2 = count_has_all(['launch_app', 'click_appbar_alarm_center', 'view_shop'])

# b2_3 : 보유 여부 + click_purchase
b2_3 = count_has_all(['launch_app', 'click_appbar_alarm_center', 'view_shop', 'click_purchase'])

# b2_5 : 보유 여부 + complete_purchase
b2_4 = count_has_all(['launch_app', 'click_appbar_alarm_center', 'view_shop', 'click_purchase', 'complete_purchase'])

print("▶ Branch 2 counts")
print("b2_1 :", b2_1)
print("b2_1_1 :", b2_1_1)
print("b2_2 :", b2_2)
print("b2_3 :", b2_3)
print("b2_4 :", b2_4)
```

<br>

---

## \*문제점

- 현재 다른 팀원들의 발표 대본 초안을 봤을 때, 어떤 점을 설명했으면 좋겠는데 안 한 부분이 눈에 많이 들어와서
- 내일 발표 리허설 할 때 수정논의 예정

<BR>

## \* 회고

- 발표 자료 마무리 작업을 진행했지만, 멘토님께서 강조하신 _“분량이 길면 핵심 메시지가 흐려질 수 있다”_ 는 부분을 충분히 반영했는지 걱정됨

- 주요 내용을 더 간결하게 전달하기 위해 슬라이드 구성을 다듬었지만, 실제 발표 흐름에서도 핵심만 명확하게 전달할 수 있도록 한 번 더 점검할 필요성을 느낌
