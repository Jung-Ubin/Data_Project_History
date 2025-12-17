import pandas as pd

# 데이터 불러오기
df = pd.read_csv(
    "C:/Users/nuwba/Desktop/과제/프로젝트미션/초급 프로젝트/사용할_데이터_정리/05_동작구_대중교통_좌표&정보.csv",
    encoding="utf-8-sig"
)

# 필요한 열 선택
df = df[['대중교통', '동 이름', '일평균총승객수']]

# 제외할 동 목록
제외_동 = ['신길동(영등포구)', '반포동(서초구)', '여의도동(영등포구)', '구로동(구로구)', '봉천동(관악구)']
df = df[~df['동 이름'].isin(제외_동)]

# 사용할 교통수단만 필터링
허용_교통 = ['버스', '지하철', '따릉이']
df = df[df['대중교통'].isin(허용_교통)]

# 동별 교통수단별 합계
pivot_df = df.pivot_table(
    index='동 이름',
    columns='대중교통',
    values='일평균총승객수',
    aggfunc='sum',
    fill_value=0
).reset_index()

# 교통수단별 합계 열 추가
pivot_df['동별일평균총승객수'] = pivot_df['버스'] + pivot_df['지하철'] + pivot_df['따릉이']

# 결과 저장
output_path = "C:/Users/nuwba/Desktop/과제/프로젝트미션/초급 프로젝트/통계적 분석/11_동작구_일일평균_버스,지하철,따릉이_이용률_합계.csv"
pivot_df.to_csv(output_path, index=False, encoding='utf-8-sig')