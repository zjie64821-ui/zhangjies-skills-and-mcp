---
name: datapipeline
description: >
  Python 数据处理管道引擎. TRIGGER when the user wants to: clean, transform, merge, or process
  datasets; build data pipelines; perform feature engineering; handle missing data; deduplicate records;
  standardize variables; create panel data; batch process CSV/Excel files; automate repetitive data
  operations; convert between data formats; scrape or collect data; build panel datasets for econometrics.
  Keywords: 数据处理, 数据清洗, 合并数据, 去重, 面板数据构建, 特征工程, 批量处理, pandas,
  dataframe, pipeline, ETL, 数据管道, 数据转换, 全局去重, 对数化, 标准化分类, 数据匹配,
  data cleaning, merge datasets, deduplication, feature engineering, data pipeline, panel data.
  DO NOT trigger for econometric regression analysis (use stata) or pure visualization.
---

# Python 数据处理管道引擎

## 核心原则
1. **可复现**: 每个处理步骤生成独立 Python 脚本，命名 `Step{n}_{描述}.py`
2. **防御性编程**: 每步验证数据完整性（行数、缺失率、唯一值）
3. **中间态保留**: 关键步骤输出中间 CSV，便于回溯和调试

## 标准管道模板

### Step 0: 数据探查
```python
import pandas as pd
import numpy as np

df = pd.read_csv("input.csv")
print(f"Shape: {df.shape}")
print(f"Columns: {df.columns.tolist()}")
print(f"Dtypes:\n{df.dtypes}")
print(f"Missing:\n{df.isnull().sum()}")
print(f"Duplicates: {df.duplicated().sum()}")
```

### Step 1: 数据清洗
```python
def clean_data(df):
    # 去重
    before = len(df)
    df = df.drop_duplicates(subset=['id', 'year'])
    print(f"Dedup: {before} → {len(df)}")

    # 缺失值处理
    # 策略1: 删除关键字段缺失行
    df = df.dropna(subset=['key_var'])
    # 策略2: 填充
    df['var'] = df['var'].fillna(df['var'].median())

    # 类型转换
    df['year'] = df['year'].astype(int)
    df['amount'] = pd.to_numeric(df['amount'], errors='coerce')

    return df
```

### Step 2: 变量构建
```python
def engineer_features(df):
    # 对数化
    df['ln_var'] = np.log(df['var'] + 1)

    # 滞后项
    df = df.sort_values(['id', 'year'])
    df['var_lag1'] = df.groupby('id')['var'].shift(1)

    # 增长率
    df['var_growth'] = df.groupby('id')['var'].pct_change()

    # 交互项
    df['x1_x2'] = df['x1'] * df['x2']

    # 分类变量编码
    df['cat_encoded'] = df['category'].astype('category').cat.codes

    return df
```

### Step 3: 数据合并
```python
def merge_datasets(left, right, keys, how='left'):
    """安全合并：验证合并前后行数"""
    before = len(left)
    merged = left.merge(right, on=keys, how=how)
    after = len(merged)
    if how == 'left' and after != before:
        print(f"WARNING: 行数变化 {before} → {after}")
        print("可能存在一对多匹配，请检查右表重复")
    print(f"Merge: {before} x {len(right)} → {after} ({how} join on {keys})")
    return merged
```

### Step 4: 面板数据构建
```python
def build_panel(df, id_col, time_col):
    """构建平衡/非平衡面板"""
    panel_ids = df[id_col].unique()
    time_periods = sorted(df[time_col].unique())

    # 创建完整面板骨架
    idx = pd.MultiIndex.from_product(
        [panel_ids, time_periods],
        names=[id_col, time_col]
    )
    panel = pd.DataFrame(index=idx).reset_index()

    # 合并数据
    panel = panel.merge(df, on=[id_col, time_col], how='left')

    # 检查面板平衡性
    obs_per_id = panel.groupby(id_col).size()
    balanced = (obs_per_id == len(time_periods)).all()
    print(f"Panel: {len(panel_ids)} units × {len(time_periods)} periods = {len(panel)} obs")
    print(f"Balanced: {balanced}")

    return panel
```

### Step 5: 批量文件处理
```python
import glob
from pathlib import Path

def batch_process(input_dir, output_dir, process_fn):
    """批量处理目录下所有文件"""
    files = glob.glob(f"{input_dir}/*.csv")
    print(f"Found {len(files)} files")

    Path(output_dir).mkdir(exist_ok=True)

    results = []
    for f in files:
        df = pd.read_csv(f)
        result = process_fn(df)
        out_path = f"{output_dir}/{Path(f).stem}_processed.csv"
        result.to_csv(out_path, index=False)
        results.append(result)
        print(f"  ✓ {Path(f).name} → {Path(out_path).name}")

    combined = pd.concat(results, ignore_index=True)
    combined.to_csv(f"{output_dir}/combined.csv", index=False)
    print(f"Total: {len(combined)} rows")
    return combined
```

### Step 6: 数据质量报告
```python
def quality_report(df, name="dataset"):
    """生成数据质量报告"""
    report = {
        'name': name,
        'rows': len(df),
        'cols': len(df.columns),
        'missing_pct': (df.isnull().sum().sum() / (len(df) * len(df.columns)) * 100),
        'dup_rows': df.duplicated().sum(),
        'numeric_cols': df.select_dtypes(include=np.number).columns.tolist(),
        'cat_cols': df.select_dtypes(exclude=np.number).columns.tolist(),
    }
    for k, v in report.items():
        print(f"  {k}: {v}")
    return report
```

## 常用模式

### 文本→数值映射（政策分类）
```python
mapping = {
    '关键词1': '类别A',
    '关键词2': '类别B',
}
df['category'] = df['text_field'].map(
    lambda x: next((v for k, v in mapping.items() if k in str(x)), '未分类')
)
```

### 分组聚合
```python
agg = df.groupby(['province', 'year']).agg(
    total=('amount', 'sum'),
    count=('id', 'count'),
    mean_val=('score', 'mean'),
).reset_index()
```

## 输出规范
- 文件命名: `Step{n}_{操作描述}_{日期}.py`
- 中间文件: `中间结果/Step{n}_{描述}.csv`
- 日志: 每步打印处理前后行数和关键字段统计
- 编码: 统一 UTF-8，CSV 写入用 `encoding='utf-8-sig'`

## 用户需求
$ARGUMENTS
