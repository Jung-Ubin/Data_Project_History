# Day - 5 협업 일지(고급)

#### 일자: 25-10-17 / 정유빈

---

---

### 팀원들과 논의한 일

- 테이블을 팀원끼리 조금 더 살펴보고 비즈니스 플로우를 파악을 한 후, 데이터들을 어떤 이유로 제외할지 논리를 보강하여, `user_info`를 다시 정리(inner joun/left,right join 뭘 쓸건지 이런거)

<br>

## \* 오늘 + 내가 한 일

## 테이블 하나씩 뜯어 보기

- 총 테이블 25개를 하나씩 뜯어보며, 멘토님이 조언주신 비즈니스 플로우를 파악해보기

  <br>

---

## `accounts_group` (학급 테이블) 정보 정리

- **데이터 규모** : 84,515건
- **데이터 목적** : 각 유저의 소속 학년(grade), 반(class_num), 학교(school_id) 정보를 저장하는 테이블
- **NULL 존재 여부** : NULL 값 없음

<BR>

### **컬럼 정보**

| 컬럼명      | 데이터 타입         | 속성                               | 설명                                       | 주요 값 / 특징                      |
| ----------- | ------------------- | ---------------------------------- | ------------------------------------------ | ----------------------------------- |
| `id`        | BIGINT (PK, NN, AI) | 기본키 / Not Null / Auto Increment | 학급 레코드 고유 식별자                    | 중복 없음                           |
| `grade`     | INT (NN)            | Not Null                           | 학년 정보                                  | 1~3학년 중심, 4·20 등 비정상값 존재 |
| `class_num` | INT (NN)            | Not Null                           | 반 번호                                    | 1~10 내외의 정수값                  |
| `school_id` | BIGINT (NN)         | Not Null                           | 소속 학교 ID (`accounts_school.id`와 매칭) | FK 역할, 학교 테이블과 JOIN 가능    |

<BR>

### **테이블 데이터 현황 요약**

| 항목           | 결과                                                            |
| -------------- | --------------------------------------------------------------- |
| 전체 행 수     | **84,515건**                                                    |
| 고유 학년 수   | 5개 (1, 2, 3, 4, 20)                                            |
| NULL 존재 여부 | **없음** (`id`, `grade`, `class_num`, `school_id` 전부 값 존재) |

<BR>

---

### **학년별 회원 분포 (중·고등학교 구분 전)**

| 학년(grade) | 인원수     | 비율(%)    |
| ----------- | ---------- | ---------- |
| 1           | 19,659     | 23.26      |
| 2           | 35,581     | 42.10      |
| 3           | 29,273     | 34.64      |
| `4`         | `1`        | `0.00`     |
| `20`        | `1`        | `0.00`     |
| **합계**    | **84,515** | **100.00** |

- `grade=4`, `grade=20` 값은 오기입 혹은 테스트 데이터로 판단됨

- 위에서도 확인했지만, 4, 20으로 기입된 데이터 수 한번 더 체크하기  
  ![1760665973236](<image/Day5_협업일지_정유빈/1760665973236.png>)

---

### **비정상 학년 상세 확인**

- `accounts_school(학교 테이블)`의 정보를 끌고와서 `school_id`를 매칭하여 해당 유저 정보 확인  
  ![1760662815335](<image/Day5_협업일지_정유빈/1760662815335.png>)

- 두 사례 모두 중학교(M) 로 확인됨 → **학년 데이터 입력 오류 가능성 높음**
- **존재하지 않는 학년이기도 하며, 데이터 수가 극소수이기 때문에 제외 가능**

---

### **학교 유형별 회원 분포 (`accounts_school` JOIN 결과)**

- `accounts_group`의 `school_id`컬럼을 → `accounts_school`의 `id`컬럼과 매칭

| 구분(`school_type`) | grade | 인원수                       | 비율(%) |
| ------------------- | ----- | ---------------------------- | ------- |
| **고등학교(H)**     | 1     | 18,451                       | 37.92   |
|                     | 2     | 17,166                       | 35.27   |
|                     | 3     | 13,047                       | 26.81   |
| **중학교(M)**       | 1     | 1,198                        | 3.34    |
|                     | 2     | 18,408                       | 51.39   |
|                     | 3     | 16,217                       | 45.27   |
| **매칭 실패(NULL)** | 1     | 10                           | 38.46   |
|                     | 2     | 7                            | 26.92   |
|                     | 3     | 9                            | 34.62   |
| **유저수 총합**     |       | 84,513(**4, 20학년** 제외됨) |         |

- 전체 데이터 중 `school_type`이 NULL인 경우 26건 (0.03%) 존재

---

### **`accounts_group`의 `school_id`컬럼 과 `accounts_school`의 `id`컬럼 의 매칭 실패 원인 분석**

<br>

- 매칭 실패된 `school_id` 정보  
  ![1760668014985](<image/Day5_협업일지_정유빈/1760668014985.png>)

<br>

- `accounts_group`에서 `school_id` 컬럼 값이 1인 데이터 수  
  ![1760667934486](<image/Day5_협업일지_정유빈/1760667934486.png>)

<br>

- `school_type`이 NULL로 나온 데이터 수 : **26**  
  ![1760668181298](<image/Day5_협업일지_정유빈/1760668181298.png>)

<br>

| 구분                                          | 값                                                                 |
| --------------------------------------------- | ------------------------------------------------------------------ |
| 매칭 실패 `school_id`                         | **1**                                                              |
| `accounts_group`에서 `school_id==1` 데이터 수 | **26건** (**학교유형별 회원에서도 NULL 로 나온 수 26건**)          |
| 원인                                          | `accounts_school`에 `id=1`이 존재하지 않아 JOIN 불가               |
| 조치                                          | 데이터 정제 시 `school_id=1` 데이터 수가 적으니 제외 가능이라 판단 |

<br>

---

### **주요 인사이트 정리**

| 인사이트                                                | 해석                                                                    |
| ------------------------------------------------------- | ----------------------------------------------------------------------- |
| **학년 데이터는 1~3학년 중심으로 구조적 안정성이 높음** | → 실제 학제 기반 학년 분포와 일치                                       |
| **비정상 학년(4, 20) 2건 존재**                         | → 데이터 입력 오류 가능성, 정제 필요                                    |
| **학교 매칭률 99.97%로 데이터 결합 신뢰도 높음**        | → 대부분의 유저가 정상적으로 학교 정보와 연결됨                         |
| **중학교(M)와 고등학교(H) 비율 유사**                   | → 전체 데이터에서 중학생 약 48%, 고등학생 약 52% 수준 추정 가능         |
| **school_id=1 데이터는 제외 가능**                      | → 정확히 매칭되지 않은 정보 수가 26건으로 적기 때문에 분석 시 제외 가능 |

---

## `accounts_nearbyschool` (인근 학교 관계 테이블) 정보 요약

- **데이터 규모** : 59,500건
- **데이터 목적** : 각 학교별로 인근 학교 9개를 기록해두는 관계형 테이블 (거리순)
- **NULL 존재 여부** : NULL 값 없음

<BR>

### 컬럼 정보

| 컬럼명             | 데이터 타입         | 속성                               | 설명                          |
| ------------------ | ------------------- | ---------------------------------- | ----------------------------- |
| `id`               | BIGINT (PK, NN, AI) | 기본키 / Not Null / Auto Increment | 테이블 고유 식별자            |
| `distance`         | FLOAT (NN)          | Not Null                           | 기준 학교와 인근 학교 간 거리 |
| `nearby_school_id` | BIGINT (NN)         | Not Null                           | 인근 학교 ID                  |
| `school_id`        | BIGINT (NN)         | Not Null                           | 기준 학교 ID                  |

<BR>

### 테이블 데이터 현황 요약

| 컬럼명             | 데이터 타입         | 속성                               | 설명                          |
| ------------------ | ------------------- | ---------------------------------- | ----------------------------- |
| `id`               | BIGINT (PK, NN, AI) | 기본키 / Not Null / Auto Increment | 테이블 고유 식별자            |
| `distance`         | FLOAT (NN)          | Not Null                           | 기준 학교와 인근 학교 간 거리 |
| `nearby_school_id` | BIGINT (NN)         | Not Null                           | 인근 학교 ID                  |
| `school_id`        | BIGINT (NN)         | Not Null                           | 기준 학교 ID                  |

---

### 기준 학교당 인근 학교 데이터 수 분포

| 구분                     | 학교 수 |
| ------------------------ | ------- |
| 인근 학교 수 정확히 10개 | 5,950개 |
| 인근 학교 수 10개 미만   | 0개     |

<BR>
- 임의의 school_id 찍어서 정보 확인 시  

![1760682045852](<image/Day5_협업일지_정유빈/1760682045852.png>)

<BR>

- **각 학교가 10개의 인근 학교 데이터를 모두 보유하고 있음**  
  → (**본인 포함 10개**, 즉 “인근학교 9개 + 자기자신 1개” 구조)

<BR>

### 학교 간 평균 거리 분포 요약

| 거리 구간(`distance_range`) | 학교 수   | 비율(%)  |
| --------------------------- | --------- | -------- |
| `< 0.01`                    | 335       | 5.6%     |
| `0.01 - 0.02`               | 2,315     | 38.9%    |
| `0.02 - 0.03`               | 726       | 12.2%    |
| `0.03 - 0.05`               | 742       | 12.5%    |
| `0.05 - 0.08`               | 1,205     | 20.2%    |
| `>= 0.08`                   | 627       | 10.5%    |
| **합계**                    | **5,950** | **100%** |

- 전체적으로 0.02~0.05 사이의 중간 거리 구간이 다수이며, 지역적으로 밀집된 학교 분포를 가짐

---

## school_density_info (학교 밀집도 정보 뷰) 생성

- **데이터 규모** : 5,950행
- **데이터 목적** : 각 학교 주변의 학교 밀집도(density) 계산 "density값이 크면 주변 학교가 가깝다"
- 해당 데이터를 school_id 정보가 있는 user들에게 매칭 시켜보기 위해 생성
- **NULL 존재 여부** : 없음
- **생성 기반 테이블** : `accounts_nearbyschool`

<br>

```sql
-- 뷰 생성 쿼리
CREATE OR REPLACE VIEW final.school_density_info AS
SELECT
    school_id,                           -- 기준 학교 ID
    SUM(1.0 / distance) AS density       -- 거리의 역수를 합산한 밀집도
FROM final.accounts_nearbyschool
WHERE distance IS NOT NULL
  AND distance <> 0                      -- 자기 자신(거리 0) 제외
GROUP BY school_id;
```

<br>

- 뷰 모습  

![1760682255118](<image/Day5_협업일지_정유빈/1760682255118.png>)

<br>

### 뷰 검증 및 density(밀집도) 사용방법

- `density(밀집도)` 값이 높을수록 주변 학교가 가까이 많이 존재한다는 의미
- 지역적으로 학교가 밀집된 구역을 나타냄

<br>

- 학교 별로 뷰에 정보가 잘 들어갔는지 확인 시 5,950건 확인  
  ![1760683678789](<image/Day5_협업일지_정유빈/1760683678789.png>)

<br>

- `accounts_nearbyschool` 테이블의 고유 학교 수 5,950건과 일치  
  ![1760683769840](<image/Day5_협업일지_정유빈/1760683769840.png>)

<br>

---

## event_user_nearbyschooldensity_info (유저별 학교 밀집도 뷰)

- 데이터 규모 : 230,784건
- 데이터 목적 : 이벤트 기간 유저(user_properties)에 학교 밀집도(density) 정보를 연결하여 지역적 특성 반영
- NULL 존재 여부 : 없음
- 생성 기반 뷰/테이블 :`user_properties`, `school_density_info`

<br>

```sql
-- 뷰 생성 쿼리
CREATE OR REPLACE VIEW final.event_user_nearbyschooldensity_info AS
SELECT
    up.*,                 -- user_properties의 모든 유저 정보
    sdi.density           -- school_density_info에서 가져온 밀집도
FROM final.user_properties AS up
LEFT JOIN final.school_density_info AS sdi
    ON up.school_id = sdi.school_id
WHERE sdi.density IS NOT NULL;           -- 밀집도 정보가 있는 경우만 남김
```

<br>

### `event_user_nearbyschooldensity_info` 뷰 제작 과정

#### 1. `school_density_info`뷰를 `user_properties(이벤트 기간 유저 정보)` 테이블에 `schoo_id` 와 매칭시켜서 user 추적

```sql
-- `user_properties`의 유저 정보에 `school_density_info` 밀집도 정보를 LEFT JOIN으로 가져와서 달아주기

SELECT
    up.*,               -- user_properties 테이블의 모든 유저 정보
    sdi.density         -- school_density_info 뷰에서 가져온 밀집도 값
FROM final.user_properties AS up
LEFT JOIN final.school_density_info AS sdi
    ON up.school_id = sdi.school_id;  -- school_id 기준으로 두 테이블 매칭
```

- `dnesity(밀집도)` 매칭 결과  
  ![1760684719560](<image/Day5_협업일지_정유빈/1760684719560.png>)

<br>

#### 2. LEFT JOIN 과정 중 소실되는 행 있는지 / 매칭 안된 density값 있는지 확인

```sql
-- LEFT JOIN 과정 중 혹시라도 소실된 데이터 행 없는지 확인
-- 기존 `user_properties`의 데이터 행 수 : 230,819
-- 학교 밀집도 정보 뷰 와 LEFT JOIN 후 행 수 : 230,819
-- school_density_info에 매칭되지 않아 density가 NULL인 행 수 : 35

SELECT
  COUNT(*)                              AS joined_rows,          -- 조인 결과 총 행 수
  COUNT(DISTINCT up.user_id)            AS distinct_users,       -- 유저 고유 수(참고)
  SUM(sdi.school_id IS NULL)            AS no_match_density_rows -- density 못 붙은 유저 수(참고)
FROM final.user_properties AS up
LEFT JOIN final.school_density_info AS sdi
  ON up.school_id = sdi.school_id;
```

- 쿼리 결과  
  ![1760684865593](<image/Day5_협업일지_정유빈/1760684865593.png>)

<br>

#### 3. `density(밀집도)` 값이 매칭 안된 유저의 `school_id`확인

```sql
-- 매칭 안된 유저의 `school_id` 확인
-- 이전에 봤던 `account_group` 테이블에서의 school_type이 NULL이었던
-- `school_id == 1`과, `school_id == 5929` 두 학교가 오류가 나옴
-- 데이터 수도 적고, 다른 테이블에서 오류가 보였던 id이기도 하기에 해당 id들은 제외하고 진행해도 될 것 같음

SELECT
    up.user_id,
    up.school_id
FROM final.user_properties AS up
LEFT JOIN final.school_density_info AS sdi
    ON up.school_id = sdi.school_id
WHERE sdi.school_id IS NULL;
```

- 쿼리 결과  
  ![1760684995668](<image/Day5_협업일지_정유빈/1760684995668.png>)

<br>

#### 4. NULL값 제외 후 `event_user_nearbyschooldensity_info` 생성

- NULL값 `school_id`가 다른 테이블(`accounts_group`)에서도 오류가 났던 정보
- 해당 뷰 관련 테이블의 데이터 수 대비 NULL 데이터 수도 적어서 제외하기로 결정

```sql
-- density가 NULL이 아닌 유저만 남겨서 새로운 뷰 생성
CREATE OR REPLACE VIEW final.event_user_nearbyschooldensity_info AS
SELECT
    up.*,                 -- user_properties의 모든 유저 정보
    sdi.density           -- school_density_info에서 가져온 밀집도
FROM final.user_properties AS up
LEFT JOIN final.school_density_info AS sdi
    ON up.school_id = sdi.school_id   -- 학교 ID 기준으로 조인
WHERE sdi.density IS NOT NULL;        -- 밀집도 정보가 있는 경우만 남김
```

#### 5. 생성된 `event_user_nearbyschooldensity_info` 뷰 데이터 행 수 확인

```sql
-- `user_properties` 테이블 행 수 확인 (230,819)
-- 뷰 생성으로 LEFT JOIN했을 때 density(밀집도) NULL 값 수 : 35
-- 뷰 데이터 행 개수 (230,784 ( == 230,819 - 35)

SELECT COUNT(*) AS total_rows
FROM final.event_user_nearbyschooldensity_info;
```

- 쿼리 결과  
  ![1760685394767](<image/Day5_협업일지_정유빈/1760685394767.png>)

#### 6. `event_user_nearbyschooldensity_info` 뷰 내 `school_id` 고유 개수 확인

```sql
-- `user_properties`의 `school_id` 고유 값 수 확인 (5023)
-- `density`값이 매칭 안된 NULL값으로 나온 `school_id` 1, 5929 제외됨 (2개 제외)
-- 뷰 내 `school_id(기준 학교)`컬럼 고유 데이터 수 (5,021 (== 5023 - 2)

SELECT COUNT(DISTINCT school_id) AS school_id_count
FROM final.event_user_nearbyschooldensity_info;
```

- 쿼리 결과  
  ![1760685640395](<image/Day5_협업일지_정유빈/1760685640395.png>)

---

---

## \* 사용했던 코딩

### 생성한 `school_density`뷰를 사용하여, `event_user_nearbyschooldensity_info` 생성하기

```sql
-- NULL 이유를 파악했으니 해당 NULL값은 제외하고
-- 이벤트 기간에 유저들의 학교 / 학년 / 반 / user_id / 주변학교밀집도 가 들어간 뷰를 만들자

-- density가 NULL이 아닌 유저만 남겨서 새로운 뷰 생성
CREATE OR REPLACE VIEW final.event_user_nearbyschooldensity_info AS
SELECT
    up.*,                 -- user_properties의 모든 유저 정보
    sdi.density           -- school_density_info에서 가져온 밀집도
FROM final.user_properties AS up
LEFT JOIN final.school_density_info AS sdi
    ON up.school_id = sdi.school_id   -- 학교 ID 기준으로 조인
WHERE sdi.density IS NOT NULL;        -- 밀집도 정보가 있는 경우만 남김
```

---

---

## \*문제점

- 테이블을 분석할 때마다 느끼지만, 테이블마다 유저 수가 달라서 해당 유저들을 어떻게 추출할지에 대해서는
  각 테이블의 유저들을 빼올 때 우리가 생각했을 때 필수 데이터가 존재하는 유저들은 나머지가 NULL이어도 살리고, 이런식으로 진행해야할지 고민됨

<BR>

## \* 회고

- 테이블을 분석하며, 유저들의 모집단을 어떻게 구성을 해야할지에 대한 아이디어를 팀원들과 회의를하며, 발굴해야할 것 같다.
- 오늘 역시 진행된 테이블 수가 몇 개 존재하지 않아서, 분석 속도가 붙지 않음.. 테이블 분석 요령을 좀 더 필요할 것 같다.


