---
name: policy-eval
description: >
  LLM 政策文本评估引擎. TRIGGER when the user wants to: evaluate policy documents using LLM,
  batch assess policy intensity or relevance, build policy evaluation frameworks, analyze policy
  texts at scale, construct policy indices/indicators, measure policy strength, compare policy
  string across regions or time periods, perform content analysis of government documents.
  Keywords: 政策评估, 政策强度, 政策文本, LLM评估, 批量评估, 政策指数, 政策测度,
  OIST框架, DeCE, Chain-of-Thought评估, Krippendorff's Alpha, 政策打分, 政策量化,
  policy evaluation, policy intensity, LLM assessment, policy scoring, content analysis,
  政策分类, 政策编码, 政府文件分析, 政策效应.
  DO NOT trigger for econometric regression on policy data (use stata) or data cleaning alone.
---

# LLM 政策文本评估引擎

## 核心原则
1. **结构化评估**: 使用明确的评估框架（维度→指标→子指标→二级指标）
2. **可复现**: 每次评估记录模型、温度、prompt 版本
3. **质量验证**: Krippendorff's Alpha ≥ 0.8 为一致性合格线
4. **批量高效**: 并行调用 API，断点续传，异常自动重试

## 评估框架模板

### OIST 四维框架（参考能源转型研究）
```
O - 目标导向 (Objectives)
  ├── 战略目标清晰度
  ├── 阶段性目标设定
  └── 量化指标完备性

I - 工具手段 (Instruments)
  ├── 财政工具（补贴/税收）
  ├── 行政工具（审批/监管）
  ├── 市场工具（交易/配额）
  └── 信息工具（披露/标准）

S - 严格程度 (Strictness)
  ├── 强制性条款数量
  ├── 惩罚机制明确度
  └── 执行时限紧迫性

T - 时间维度 (Timeline)
  ├── 短期措施密度
  ├── 中长期规划完备性
  └── 修订/更新机制
```

### 评估 Prompt 模板
```
你是一位政策分析专家。请根据以下评估框架，对给定的政策文本进行评估。

## 评估框架
{framework_description}

## 评估规则
1. 每个二级指标评分范围: 0-5
2. 0 = 无相关内容; 5 = 有明确、详细、可执行的规定
3. 必须提供证据引用（引用原文具体条款）
4. 使用 Chain-of-Thought 推理

## 政策文本
{policy_text}

## 输出格式
请以 JSON 格式输出:
{{
  "大类": {{
    "细分指标": {{
      "子指标": {{
        "二级指标": {{
          "score": <0-5>,
          "evidence": "<原文引用>",
          "reasoning": "<推理过程>"
        }}
      }}
    }}
  }}
}}
```

## Python 评估器模板

```python
import json
import time
from pathlib import Path
from openai import OpenAI

class PolicyAssessor:
    def __init__(self, model="deepseek-chat", temperature=0.1):
        self.client = OpenAI(
            api_key="your-api-key",
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
        )
        self.model = model
        self.temperature = temperature

    def assess_single(self, policy_text, framework_prompt):
        """评估单份政策文本"""
        messages = [
            {"role": "system", "content": framework_prompt},
            {"role": "user", "content": f"政策文本:\n{policy_text}"}
        ]
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=self.temperature,
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)

    def batch_assess(self, policy_dir, output_dir, framework_prompt):
        """批量评估目录下所有政策文件"""
        files = list(Path(policy_dir).glob("*.docx")) + \
                list(Path(policy_dir).glob("*.pdf")) + \
                list(Path(policy_dir).glob("*.txt"))
        print(f"Found {len(files)} policy files")

        results = []
        for i, f in enumerate(files):
            try:
                text = self._read_file(f)
                result = self.assess_single(text, framework_prompt)
                result['_source'] = f.name
                result['_model'] = self.model
                result['_temperature'] = self.temperature
                results.append(result)
                print(f"  [{i+1}/{len(files)}] ✓ {f.name}")
            except Exception as e:
                print(f"  [{i+1}/{len(files)}] ✗ {f.name}: {e}")
                continue

        # 保存结果
        out_path = Path(output_dir) / f"results_{self.model}_T{self.temperature}.json"
        with open(out_path, 'w', encoding='utf-8') as fp:
            json.dump(results, fp, ensure_ascii=False, indent=2)
        return results

    def _read_file(self, filepath):
        """读取政策文件（支持 docx/pdf/txt）"""
        if filepath.suffix == '.docx':
            import docx
            doc = docx.Document(filepath)
            return '\n'.join([p.text for p in doc.paragraphs])
        elif filepath.suffix == '.pdf':
            import pdfplumber
            with pdfplumber.open(filepath) as pdf:
                return '\n'.join([p.extract_text() or '' for p in pdf.pages])
        else:
            return filepath.read_text(encoding='utf-8')
```

## 质量验证

### 评估者间一致性（多轮重复测试）
```python
from sklearn.metrics import cohen_kappa_score
import numpy as np

def krippendorff_alpha(ratings):
    """计算 Krippendorff's Alpha"""
    # ratings: list of lists, each inner list = one unit's ratings across coders
    # 简化实现，实际建议用 krippendorff 包
    pass

def variance_analysis(results_df):
    """方差分析：模型×温度×轮次"""
    # 跨轮次计算每个指标的均值、方差、标准差
    stats = results_df.groupby(['model', 'temperature', 'indicator']).agg(
        mean=('score', 'mean'),
        std=('score', 'std'),
        var=('score', 'var'),
        count=('score', 'count')
    )
    return stats
```

### 异常检测
```python
def detect_anomalies(results_df):
    """检测评估异常（格式错误、超范围值、无意义文本）"""
    anomalies = []
    for idx, row in results_df.iterrows():
        # 检查分数范围
        if not (0 <= row['score'] <= 5):
            anomalies.append((idx, 'out_of_range', row['score']))
        # 检查证据字段
        if len(str(row['evidence'])) < 5:
            anomalies.append((idx, 'no_evidence', row['evidence']))
        # 检查无意义输出
        nonsense = ['极速', '极否', '极光', 'error', 'N/A']
        if any(n in str(row.get('evidence', '')) for n in nonsense):
            anomalies.append((idx, 'nonsense_output', row['evidence']))
    return anomalies
```

## 强度计算模型

```python
def compute_intensity(scores_df):
    """从评估分数计算政策强度指数"""
    # 方法1: 等权加总
    intensity = scores_df.groupby('policy_id')['score'].mean()

    # 方法2: AHP 权重
    weights = {'O': 0.3, 'I': 0.3, 'S': 0.25, 'T': 0.15}
    intensity = scores_df.pivot_table(
        index='policy_id', columns='dimension', values='score'
    ).apply(lambda row: sum(row[dim] * w for dim, w in weights.items()), axis=1)

    return intensity
```

## 输出规范
- 评估结果: CSV（大类, 细分指标, 子指标, 二级指标, 评估结果, 证据）
- 强度指数: 面板数据 CSV（policy_id, year, region, intensity_score）
- 质量报告: 包含 Krippendorff's Alpha、异常率、有效评估数
- 日志: 模型版本、温度、评估时间、token 消耗

## 用户需求
$ARGUMENTS
