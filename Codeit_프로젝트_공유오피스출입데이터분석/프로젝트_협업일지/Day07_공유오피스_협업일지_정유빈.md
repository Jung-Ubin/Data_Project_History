# Day - 7 협업 일지(중급2)

#### 일자: 2025-09-12 / 정유빈

---

### 팀원들과 논의한 일

- 보고서 최종 마무리 진행 논의
- 발표 자료 작성 논의

## \* 오늘 + 내가 한 일

- 보고서 마무리 작업 진행
- 보고서 하는 동안 팀원들이 작업하는 발표자료 정리
- 발표자료 작업 합류 후 진행

## \* 사용했던 코딩

- PCA 로딩값 확인

```python
# PCA 실행할 때 사용했던 feature만 다시 가져오기
features = [col for col in scaled_df.columns if col != 'kmeans_label']

# 로딩값 추출
loadings = pd.DataFrame(
    pca_2.components_.T,
    columns=['PC1', 'PC2', 'PC3', 'PC4', 'PC5'],
    index=features
)

# 1행 5열 subplot
fig, axes = plt.subplots(1, 5, figsize=(25, 6))

for i, pc in enumerate(['PC1', 'PC2', 'PC3', 'PC4', 'PC5']):
    # 절댓값 기준 상위 10개
    top10 = loadings[pc].abs().sort_values(ascending=False).head(10)

    # 실제 값(부호 포함) 그래프
    loadings.loc[top10.index, pc].sort_values().plot.barh(ax=axes[i])
    axes[i].set_title(f"Top 10 Loadings - {pc}")
    axes[i].set_xlabel("Loading Value")

plt.tight_layout()
plt.show()
```

---

## \*문제점

- 보고서 작성이 늦게 끝나 발표 자료를 아직 완성하지 못함 → 주말에 시간내서 만들기로 함
- 이번 프로젝트는 분석에서 놓치거나 급하게 진행하여 부족한 점이 많다고 느껴져 아쉬운 마음이 큼

## \* 회고

- 팀장으로써 할 일을 분할하여 진행하였지만,
- 각 팀원들 분석에서도 어려움이 많아 문제를 해결하기 위해
- 팀원들과 논의하는 부분에서 시간을 많이 소비하여
- 보고서 및 분석에 있어서 부족한 점이 많아 개인적으로 아쉬운 생각이 듦
