# Day - 6 협업 일지(중급2)

#### 일자: 2025-09-11 / 정유빈

---

### 팀원들과 논의한 일

- 보고서 작성 방법 논의
- 남은 분석 진행

## \* 오늘 + 내가 한 일

- 보고서 작성 방향 제시
- 차례 작성 및 분석 내용 정리
- 전체적인 톤 정리
- 클러스터링 분석 마무리 및 클러스터 해석

## \* 사용했던 코딩

- K-Means 그래프 확인(3D)

```python
from sklearn.cluster import KMeans
import numpy as np

# 실행 시 기존 kmeans_label 컬럼 제거
if 'kmeans_label' in pca_df.columns:
    pca_df = pca_df.drop(columns=['kmeans_label'])

# K-means 모델 학습
model = KMeans(n_clusters=4, random_state=123)
model.fit(pca_df[['PC1','PC2','PC3']])  # 주성분만 사용

# 라벨 추가
pca_df['kmeans_label'] = model.labels_

# 클러스터 개수 확인
print("고정된 클러스터 수 (모델 설정):", model.n_clusters)
print("실제로 생성된 클러스터 라벨:", np.unique(model.labels_))
print("클러스터 개수:", len(np.unique(model.labels_)))

# 3D 시각화
fig = plt.figure(figsize=(15, 9))
ax = fig.add_subplot(111, projection='3d')

scatter = ax.scatter(
    pca_df['PC1'], pca_df['PC2'], pca_df['PC3'],
    c=pca_df['kmeans_label'], marker='o', cmap='tab10'
)

ax.set_xlabel("PC1")
ax.set_ylabel("PC2")
ax.set_zlabel("PC3")
ax.set_title("3D PCA Result")

plt.show()
```

---

## \*문제점

- 분석한 내용들을 중간에 정리했지만, 보고서 작성할 때 작성 순서 및 방향에 대해서 논의가 오래걸림
- 팀원과의 소통을 하며 복잡한 인사이트 정리에 대해서 해결해 나갔지만, 작업 속도가 느림

## \* 회고

- 보고서 작성 직전 팀원들과 인사이트에 대해서 한 번더 논의 및 정리하는 시간이 필요할 것 같다
- 보고서 작성 때문에 시간이 없어서 확인하지 못한 점(추가분석)들이 아쉬웠다
