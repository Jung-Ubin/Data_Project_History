# Day - 1 협업 일지(고급)

#### 일자: 2025-10-13 / 정유빈

---

### 팀원들과 논의한 일

- 리스토어링 다시 진행(기존 데이터 날아감)
- 리스토어링 후 각자 테이블 살펴보기 및 ERD 진행

## \* 오늘 + 내가 한 일

- user 목록에서의 **성비 확인**
  - **F: 396665(cnt), 58.58**
  - **M: 280418(cnt), 41.42**

<BR>

- `is_push_on` 비율 확인

  - **0: 106236(cnt), 15.69**
  - **1: 570849(cnt), 84.31**

- 각 유저들의 구매 정보 View 생성 `user_payment_summary`

<BR>

- **`user_payment_summary`로 확인한 각 아이템별 판매율 확인**
  | 상품 | 총 판매 횟수 | 전체 대비 비율(%) |
  | -------------- | ------------ | ----------------- |
  | heart.200 | 15,822 | 16.63% |
  | **heart.777** | **57,873** | **60.83% 🥇** |
  | heart.1000 | 19,309 | 20.30% |
  | **heart.4000** | **2,136** | **2.25%** |
  | **총합** | 95,140 | 100% |

<BR>

---

## \* 사용했던 코딩

### `user_payment_summary` View 만들기

```sql
CREATE VIEW final.user_payment_summary AS
SELECT
    user_id,
    SUM(CASE WHEN productId = 'heart.200' THEN 1 ELSE 0 END) AS paycount_heart200,
    SUM(CASE WHEN productId = 'heart.777' THEN 1 ELSE 0 END) AS paycount_heart777,
    SUM(CASE WHEN productId = 'heart.1000' THEN 1 ELSE 0 END) AS paycount_heart1000,
    SUM(CASE WHEN productId = 'heart.4000' THEN 1 ELSE 0 END) AS paycount_heart4000,
    SUM(
        CASE
            WHEN productId = 'heart.200' THEN 200
            WHEN productId = 'heart.777' THEN 777
            WHEN productId = 'heart.1000' THEN 1000
            WHEN productId = 'heart.4000' THEN 4000
            ELSE 0
        END
    ) AS total_heart,
    COUNT(*) AS total_paycount
FROM final.accounts_paymenthistory
GROUP BY user_id;

```

---

## \*문제점

- 보안설정을 제대로 하지 않아서, 리스토어링을 다시하여 시간이 다소 많이 소모됨  
  → **ip를 0.0.0.0에서 내 pc ip로 변경 & 컨테이너 비밀번호 12356에서 특정으로 변경**
- 테이블을 조금 더 다양하게 봤으면 좋았을 것 같지만, 현재로썬 user 정보가 있는 테이블과, 결제히스토리 테이블 정도만 확인했음

## \* 회고

- 오늘 나온 인사이트를 바탕으로 내일 `View`를 활용한 클러스터링을 통해 각 군집 별 구매 스타일을 파악할 것이다.
- 보안 강화를 통해 앞으로 정리해논 테이블들이 없어지지 않게 관리를 잘 해야할 것 같다.
