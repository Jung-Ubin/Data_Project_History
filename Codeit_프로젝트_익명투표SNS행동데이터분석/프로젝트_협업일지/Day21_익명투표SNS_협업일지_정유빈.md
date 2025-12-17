# Day - 21 협업 일지(고급)

#### 일자: 25-11-11 / 정유빈

---

### 팀원들과 논의한 일

- 보고서 마무리하기
- 발표자료 구성 및 제작하기

<br>

## \* 오늘 + 내가 한 일

### 보고서 마무리 작업

- 개선안별 목표 지표를 구해서 적용
- 분석하면서 부족했던 데이터 및 분석 한계점들을 작성하며 보고서 마무리
- 멘토님께 피드백 부탁드린 후 내일 피드백 바탕으로 최종 마무리 작업 진행

### 발표자료 작성 준비

- 팀원들이 작성한 초안을 바탕으로 내용을 정리하고, 분석 내용 보강
- 최대한 보고 받는 대상 기준 필요한 인사이트만 얻을 수 있도록 톤과 내용 설계
- 내일 오후 쯤 마무리 될 예정

---

## \* 사용했던 코드

### SQL 작업 테이블 Python으로 가져오기

```python
## MySQL 연결 정보 입력

user = "xxxxxxxxx"
password = "xxxxxxxxxxx"
host = "xxxxxxxxxxxx"
port = xxxxxxx
database = "xxxxxxxxx"

engine = create_engine(
    f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}",
    pool_pre_ping=True,
    pool_recycle=xxxxxx,
)


# session_01 테이블 로드

query = """
SELECT
    num, device_id, user_id, osname, session_id,
    session_count
FROM xxxx.session_01
"""

df = pd.read_sql(query, engine)


# 3. 결과 확인

print(f"로드된 행 수: {len(df):,}")
```

<br>

---

## \*문제점

- 발표 자료를 만들 때 보고서와 다르게 핵심 내용을 컴팩트하게 정리하고 싶어서  
  덜어낼 내용들을 생각중에 있음(멘토님 피드백 받은 후 한번 더 확인해볼 예정)

<BR>

## \* 회고

- 보고서가 그래도 여유있게 마무리 단계에 접어들어 다행이라 생각하며,  
  발표자료 역시 팀원들이 초안을 잘 준비해준 덕분에 세부작업을 진행할 수 있었음.
- 초안을 검토하며 불필요한 내용은 덜어내고, 핵심 메시지를 중심으로 정리할 필요성을 느꼈음.
- 발표자료는 보고서와 달리 한 장당 전달 시간이 짧기 때문에, 핵심 분석 내용을 명확히 전달할 수 있도록  
  구성에 신경쓰며 마지막까지 완성도를 높여 유종의 미를 거둘 수 있도록 마무리에 최선을 다 해야겠다.
