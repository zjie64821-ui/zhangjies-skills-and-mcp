---
name: stata
description: >
  Stata 计量经济学分析引擎. TRIGGER when the user wants to: run regression analysis, DID/DID
  estimation, spatial Durbin model (SDM), panel data analysis, fixed effects regression, instrumental
  variables (IV/2SLS), propensity score matching (PSM), event study, parallel trend test, heterogeneity
  analysis, robustness check, mediation/moderation analysis, or any econometric estimation.
  Keywords: Stata, 回归, DID, 双重差分, SDM, 空间杜宾, 面板数据, 固定效应, 工具变量, PSM,
  事件研究, 平行趋势, 异质性分析, 稳健性检验, 中介效应, 调节效应, reghdfe, xtreg, areg,
  xsmle, spmat, spreg, ivreg2, psmatch2, regression, econometrics, spatial econometrics,
  计量, 实证分析, 经验分析.
  DO NOT trigger for pure Python data analysis (use datapipeline) or data cleaning alone.
---

# Stata 计量经济学分析引擎

## 核心原则
1. **代码即答案**: 生成完整可运行的 .do 文件，而非片段
2. **结果导向**: 每段代码附带预期输出格式和解读指南
3. **渐进式**: 先基准回归 → 再稳健性 → 再异质性 → 再机制

## 标准分析流程

### Phase 1: 数据准备
```stata
* 设置面板
xtset id year
* 或
xtset province city year

* 描述性统计
estpost summarize var1 var2 var3, detail
esttab using "desc_stats.rtf", cells("count mean sd min p50 max") replace

* 相关性矩阵
pwcorr var1 var2 var3, sig star(.05)

* VIF 检验（多重共线性）
reg y x1 x2 x3
estat vif
```

### Phase 2: 基准回归
```stata
* 混合 OLS
reg y x controls, robust

* 固定效应（双向）
reghdfe y x controls, absorb(id year) vce(cluster id)

* DID 估计
reghdfe y treat##post controls, absorb(id year) vce(cluster id)

* 空间杜宾模型 (SDM)
* 先构建空间权重矩阵
spmatrix using W.dta, name(W)
xsmle y x controls, fe wmat(W) model(sdm) effects
```

### Phase 3: 稳健性检验
```stata
* 1. 替换被解释变量
* 2. 替换核心解释变量
* 3. 缩尾处理 (winsor)
winsor2 var, cuts(1 99) replace
* 4. 排除特定样本（直辖市/特殊年份）
* 5. PSM-DID
psmatch2 treat controls, out(y) neighbor(1:1) caliper(0.05)
```

### Phase 4: 平行趋势（DID 专用）
```stata
* 事件研究法
gen event_time = year - policy_year
forvalues i = -5/-2 {
    local pre `pre' i(event_time)'
}
forvalues i = 0/5 {
    local post `post' i(event_time)'
}
reghdfe y `pre' `post' controls, absorb(id year) vce(cluster id)
* 基期 t-1 为参照组（已省略）
coefplot, keep(i(event_time)*) vertical yline(0) ciopts(recast(rcap))
```

### Phase 5: 异质性分析
```stata
* 按分组变量分样本回归
foreach g in 0 1 {
    reghdfe y x controls if group==`g', absorb(id year) vce(cluster id)
    est store group_`g'
}
esttab group_0 group_1, b(%9.4f) t(%9.4f) star(* 0.1 ** 0.05 *** 0.01)
```

### Phase 6: 机制分析（中介效应）
```stata
* Baron & Kenny 三步法
* Step 1: Y ~ X
reghdfe y x controls, absorb(id year) vce(cluster id)
* Step 2: M ~ X
reghdfe m x controls, absorb(id year) vce(cluster id)
* Step 3: Y ~ X + M
reghdfe y x m controls, absorb(id year) vce(cluster id)

* Sobel 检验
sgmediation y, mv(m) iv(x) cv(controls)
```

## 常用包安装
```stata
ssc install reghdfe, replace
ssc install ftools, replace
ssc install estout, replace
ssc install coefplot, replace
ssc install winsor2, replace
ssc install psmatch2, replace
ssc install sgmediation, replace
ssc install xsmle, replace
ssc install spatwmat, replace
```

## 输出格式规范
- 系数表: `b(%9.4f) t(%9.4f) star(* 0.1 ** 0.05 *** 0.01)`
- 描述性统计: `cells("count mean sd min p50 max")`
- 图表: 导出为 PNG/PDF，宽度 1200px
- 文件命名: `{分析类型}_{变量名}_{日期}.do`

## 注意事项
1. 始终使用 `reghdfe` 而非 `xtreg`（更高效、更灵活）
2. 聚类标准误默认用个体层面 `vce(cluster id)`
3. 面板数据先 `xtset`，报错先检查缺失值和重复
4. 中文路径问题：用 `unicode` 相关命令或避免中文路径

## 用户需求
$ARGUMENTS
