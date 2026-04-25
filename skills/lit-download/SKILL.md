---
name: lit-download
description: >
  学术文献智能发现、批量下载与深度解析引擎。TRIGGER when the user wants to: batch download academic
  papers/PDFs on a research topic; bulk fetch literature from search queries; discover and download
  papers comprehensively on any subject; build a literature library from scratch; 下载文献, 批量下载论文,
  文献下载, 帮我找文献, paper download, batch download, bulk fetch, PDF download, download papers,
  文献获取, 找论文, 收集文献, literature collection.
  DO NOT trigger for: downloading a single known URL; non-academic file downloads; reading a paper already on disk.
---

# Lit-Download V7.0: 多源智能文献发现与下载

## 用户请求
$ARGUMENTS

## 核心配置

```
OPENALEX_API_KEY = 7k74faeETXNQj8gG7jvCqR
OPENALEX_EMAIL = zhangjie@cufe.edu.cn
经管类 Field IDs: 14=Business/Management, 20=Economics/Econometrics/Finance
```

---

## Phase 0: 输出目录与检索模式

1. 用户指定了路径 → 用用户的
2. 未指定 → `~/Desktop/放一下/{主题英文简写}/`
3. 目录结构:
   ```
   {output_dir}/
   ├── pdfs/              # 所有下载的PDF
   ├── manifest.json      # 全局下载清单
   └── search_plan.md     # 检索方案记录
   ```

### 检索模式自动选择

根据用户请求自动判断检索模式：

| 模式 | 触发条件 | 搜索源 |
|------|----------|--------|
| **全面检索** | 默认模式，探索性主题 | OpenAlex + Google Scholar |
| **NBER工作论文** | 用户提到NBER/工作论文/working paper | NBER API (via OpenAlex) |
| **顶刊定向** | 用户提到期刊名/缩写/顶刊 | 指定期刊的OpenAlex搜索 |
| **订阅摘要** | 用户提到"定期"/"最新"/"这周"/"这个月" | 基于Research Profile的周期检索 |

用户也可以通过参数显式指定：`--source nber`、`--source JPubE,AER`、`--mode digest`

---

## Phase 1: Brainstorming 主题拆解

**核心原则**: 一次检索覆盖率极低。必须拆成多个子方面分别检索。

### 拆解方法

用 Sequential Thinking MCP 进行 X/Y 轴拆解:

- **维度X (理论焦点)**: 2-4 个核心概念
- **维度Y (方法论/对象)**: 2-4 个方法或实证对象
- 交叉组合生成 6-12 组检索关键词

### 关键词设计规则

- 英文用引号包裹精确短语: `"energy transition policy"`
- 每组 2-4 个概念，不过宽不过窄
- 包含同义词变体: policy / governance / regulation
- 时间锁定: 近5年 `publication_year:2021-2026`（除非用户另有要求）
- 优先按引用数排序: `sort=cited_by_count:desc`

### Research Interest Profile (可选增强)

如果用户提供了研究方向描述或之前用过本工具，构建 Research Interest Profile 优化检索：

```json
{
  "interest_id": "fiscal-competition",
  "label": "财政竞争",
  "enabled": true,
  "method_keywords": ["tax competition", "fiscal decentralization", "intergovernmental fiscal relations"],
  "query_aliases": ["tax competition", "fiscal federalism", "race to the bottom"],
  "exclude_keywords": ["corporate tax avoidance", "transfer pricing"],
  "logic": "OR"
}
```

**Profile 的作用**:
- `method_keywords` → 用于与搜索结果做关键词匹配评分
- `query_aliases` → 自动扩展为额外的搜索查询
- `exclude_keywords` → 从结果中过滤不相关论文
- `logic` → OR=任一匹配即可, AND=全部匹配才算

Profile 保存到 `{output_dir}/research_profile.json`，下次同类主题可复用。

### 拆解示例（主题: "数字经济与就业"）

```
维度X: digital economy, digital transformation, AI adoption, platform economy
维度Y: employment effects, job displacement, labor market, wage inequality

检索组合:
1. "digital economy" employment panel data
2. "AI adoption" labor market effects
3. "digital transformation" job displacement
4. "platform economy" wage inequality
5. "digitalization" employment China
6. "robot adoption" employment manufacturing
```

将检索方案写入 `{output_dir}/search_plan.md`。

---

## Phase 2A: OpenAlex 结构化搜索 (主引擎)

**OpenAlex 是主发现引擎**。优势:
- 2.5亿+ 篇论文，经管类覆盖率 98.6%（最高）
- 直接返回 `best_oa_location.pdf_url`（OA 论文直接拿 PDF）
- 支持按 Topic/Field/Subfield 精确筛选
- 按引用数排序，优先高影响力论文
- 免费 API key，每天 $1 额度（约1000次搜索）

### 2A.1: 通用关键词搜索（全面检索模式）

```bash
# OA论文（可直接下载）
curl -s "https://api.openalex.org/works?search={encoded_query}&filter=primary_topic.field.id:20|14,publication_year:2021-2026,is_oa:true&per_page=25&sort=cited_by_count:desc&api_key=7k74faeETXNQj8gG7jvCqR"

# 全部论文（含付费）
curl -s "https://api.openalex.org/works?search={encoded_query}&filter=primary_topic.field.id:20|14,publication_year:2021-2026&per_page=25&sort=cited_by_count:desc&api_key=7k74faeETXNQj8gG7jvCqR"
```

**筛选参数说明**:
- `primary_topic.field.id:20|14` — 限定经济学(Field 20) 或 商业管理(Field 14)
- `is_oa:true` — 优先OA论文（可直接下载PDF）
- `per_page=25` — 每组取25篇
- `sort=cited_by_count:desc` — 高引用优先

### 2A.2: NBER 工作论文搜索（NBER模式）

NBER 是经济学最重要的工作论文来源，论文质量极高（很多后来发表在AER/JPE等顶刊）。

```bash
# 搜索NBER工作论文
curl -s "https://api.openalex.org/works?search={encoded_query}&filter=primary_location.source.id:S27349830,publication_year:2021-2026&per_page=25&sort=publication_year:desc&api_key=7k74faeETXNQj8gG7jvCqR"
```

**NBER 搜索要点**:
- `primary_location.source.id:S27349830` — NBER Working Papers 的 OpenAlex Source ID
- 按发表日期倒序（`publication_year:desc`），NBER论文时效性比引用数更重要
- NBER 论文几乎都是 OA（免费PDF），下载成功率接近100%
- NBER PDF URL 格式: `https://www.nber.org/system/files/working_papers/w{number}/w{number}.pdf`

### 2A.3: 顶刊定向搜索（顶刊模式）

使用 CUFE 期刊目录（2025版）中的 145+ 本 AAA/AA 级期刊，按 OpenAlex Source ID 精确筛选。

#### 期刊别名速查表

| 别名 | 全称 | OpenAlex Source ID | CUFE等级 |
|------|------|-------------------|----------|
| AER | American Economic Review | S23254222 | AAA |
| JPE | Journal of Political Economy | S95323914 | AAA |
| QJE | Quarterly Journal of Economics | S203860005 | AAA |
| RES | Review of Economic Studies | S88935262 | AAA |
| ECMA | Econometrica | S95464858 | AAA |
| JPubE | Journal of Public Economics | S26877950 | AAA |
| JUE | Journal of Urban Economics | S26877950 | AAA |
| JHE | Journal of Health Economics | S26877950 | AAA |
| JDE | Journal of Development Economics | S26877950 | AAA |
| JMonE | Journal of Monetary Economics | S26877950 | AAA |
| JIE | Journal of International Economics | S26877950 | AAA |
| JLE | Journal of Labor Economics | S26877950 | AAA |
| JEE | Journal of Environmental Economics and Management | S26877950 | AAA |
| REStat | Review of Economics and Statistics | S26877950 | AAA |
| EJ | Economic Journal | S26877950 | AAA |
| JASA | Journal of the American Statistical Association | S4394736638 | AAA |
| APSR | American Political Science Review | S26877950 | AAA |
| AJPS | American Journal of Political Science | S26877950 | AAA |
| JPAM | Journal of Policy Analysis and Management | S26877950 | AA |
| EnergyE | Energy Economics | S26877950 | - |
| EnergyP | Energy Policy | S13631 | - |

#### 顶刊搜索方式

**单刊搜索**:
```bash
curl -s "https://api.openalex.org/works?search={encoded_query}&filter=primary_location.source.id:S23254222,publication_year:2021-2026&per_page=25&sort=cited_by_count:desc&api_key=7k74faeETXNQj8gG7jvCqR"
```

**多刊搜索（AAA级经济五顶刊）**:
```bash
curl -s "https://api.openalex.org/works?search={encoded_query}&filter=primary_location.source.id:S23254222|S95323914|S203860005|S88935262|S95464858,publication_year:2021-2026&per_page=50&sort=cited_by_count:desc&api_key=7k74faeETXNQj8gG7jvCqR"
```

**使用 OpenAlex MCP 更方便**:
- `search_in_journal_list` → 内置 FT50/UTD24/AJG 期刊列表，一步到位
- `search_works_in_venue` → 按期刊名精确搜索

#### 全量AAA/AA期刊搜索（最全面）

当用户要求"顶刊"但不指定具体期刊时，搜索全部AAA级经管期刊:
```bash
# AAA级经济学+政治学期刊（约30本）
curl -s "https://api.openalex.org/works?search={encoded_query}&filter=primary_topic.field.id:20,publication_year:2021-2026&per_page=50&sort=cited_by_count:desc&api_key=7k74faeETXNQj8gG7jvCqR"
```
然后对结果按 `primary_location.source.display_name` 过滤，仅保留 AAA/AA 期刊列表中的论文。

### 提取关键字段

从每个 result 提取:
- `id` (OpenAlex ID, 如 W2741809807)
- `doi` (DOI)
- `title` (标题)
- `publication_year` (年份)
- `cited_by_count` (引用数)
- `primary_location.source.display_name` (期刊名)
- `primary_location.source.id` (期刊Source ID，用于期刊等级判定)
- `is_oa` (是否OA)
- `open_access.oa_status` (gold/green/bronze/hybrid/diamond/closed)
- `best_oa_location.pdf_url` (OA PDF直链，最关键)
- `best_oa_location.landing_page_url` (着陆页)
- `type` (论文类型: article/review/book-chapter 等)

### 可选: 用 OpenAlex MCP Server

如果 MCP 可用，可调用 OpenAlex MCP 工具辅助搜索:
- `search_works`: 关键词搜索
- `search_in_journal_list`: 按 FT50/UTD24/AJG 期刊列表筛选（经管类特化）
- `get_work`: 获取单篇详情
- `search_works_in_venue`: 按特定期刊搜索

---

## Phase 2B: Google Scholar 补充搜索 (覆盖增强)

**Google Scholar 是覆盖最广的搜索引擎**（~3.9亿篇），用于补充 OpenAlex 遗漏的论文。
特别适合抓取：工作论文(NBER/SSRN)、会议论文、预印本、非英文文献。

### 为什么需要双重搜索

根据 Martin-Martin et al. (2021, Scientificometrics) 对 310 万条引文的分析:
> "Google Scholar 的引文包含了 WoS 和 Scopus 中引文的超集"

OpenAlex 的结构化搜索精度高但可能遗漏:
- 最新发表的论文（Google Scholar 索引更快）
- 工作论文和预印本（NBER, SSRN, RePEc）
- 非主流期刊和区域性论文

### 搜索方法

通过 Chrome DevTools MCP 自动化 Google Scholar 搜索:

```
1. navigate_page → https://xs.gupiaoq.com/scholar?q={encoded_query}&as_ylo=2021&as_sdt=0,5
   （使用镜像站 xs.gupiaoq.com，官方 scholar.google.com 可能无法访问）
2. take_snapshot → 提取搜索结果
3. 对每条结果提取: 标题、作者、年份、期刊、引用数、DOI/链接
4. 如果有 "下一页" → 翻页继续提取（最多3页 = ~30篇）
5. 用标题/DOI 与 OpenAlex 结果去重
```

### Google Scholar 镜像站优先级

1. **推荐**: `https://xs.gupiaoq.com/` （最佳兼容性，支持BibTeX）
2. **优先**: `https://scholar.lanfanshu.cn/` （稳定，引用弹窗需口令）
3. **备选**: `https://so.6465.net/` / `https://so.673.org/` / `https://sci.673.org/`
4. **备选**: `https://scholar.aigrogu.com/` / `https://www.defineabc.com/`

### Google Scholar 结果解析

搜索结果页面的 DOM 结构:
```html
<div class="gs_r gs_or gs_scl">
  <h3 class="gs_rt">
    <a href="{paper_url}">{title}</a>
  </h3>
  <div class="gs_a">{authors} - {journal}, {year} - {publisher}</div>
  <div class="gs_fl">
    <a href="{cited_by_url}">被引用 {count} 次</a>
  </div>
</div>
```

用 evaluate_script 提取:
```javascript
(() => {
  return Array.from(document.querySelectorAll('.gs_r.gs_or.gs_scl')).map(el => ({
    title: el.querySelector('.gs_rt a')?.textContent?.trim(),
    url: el.querySelector('.gs_rt a')?.href,
    meta: el.querySelector('.gs_a')?.textContent?.trim(),
    cited: el.querySelector('.gs_fl a[href*="cites"]')?.textContent?.match(/\d+/)?.[0],
    pdf_link: el.querySelector('.gs_or_ggsm a')?.href
  })).filter(r => r.title);
})()
```

### 去重与合并

- **主键**: DOI（如果有）或 标题前50字符
- Google Scholar 独有的论文（OpenAlex 未收录）→ 追加到 manifest
- 标记 `source: "google_scholar"`
- 如果 GS 提供了 PDF 直链（如 PDF [PDF] 标志），记录到 `gs_pdf_url`

### 注意事项

1. **频率限制**: Google Scholar 约10次搜索后会要求 CAPTCHA，需要间隔操作
2. **没有API**: 必须通过浏览器自动化，速度比 OpenAlex 慢
3. **元数据不完整**: GS 不返回 DOI，需要后续用标题去 Crossref/OpenAlex 匹配
4. **中文搜索**: GS 对中文论文覆盖较好，可以同时用中文关键词搜索

---

## Phase 2C: 智能排序与筛选 (新增)

借鉴 paper-finder 的多层排序机制，对合并后的搜索结果做智能排序。

### 排序维度

| 维度 | 权重 | 说明 |
|------|------|------|
| **关键词匹配度** | 35% | 查询词在标题/摘要中的匹配程度 |
| **引用影响力** | 25% | `cited_by_count`，经时间标准化 |
| **期刊等级** | 25% | AAA=3分, AA=2分, A=1分, 其他=0分 |
| **时效性** | 15% | 越新越高，NBER工作论文时效性加权 |

### 排序算法

```
score = 0.35 * keyword_match_score
      + 0.25 * normalized_citation_score
      + 0.25 * journal_rank_score
      + 0.15 * recency_score
```

**keyword_match_score**: 查询关键词出现在标题中=1.0, 摘要中=0.6, 仅作者关键词=0.3
**normalized_citation_score**: `min(cited_by_count / field_avg_citations, 1.0)`
**journal_rank_score**: AAA=1.0, AA=0.7, A=0.4, 其他=0.2
**recency_score**: 当年=1.0, 每往前1年-0.15, 最低0.1

### Zotero 语义相似度排序 (可选增强)

如果 Zotero MCP 可用且用户有文献库:
1. 调用 `mcp__zotero-mcp__semantic_search` 用用户的研究主题搜索已有文献
2. 提取最相关的5-10篇 Zotero 论文的标题和关键词
3. 对搜索结果中每篇论文，计算与 Zotero 参考文献的语义相似度
4. 作为额外 10% 权重加入排序:
   ```
   score = 0.90 * base_score + 0.10 * zotero_similarity_score
   ```

### 排除过滤器

- `exclude_keywords` 中的关键词出现在标题/摘要中 → 过滤
- 书评(book-review)、勘误(erratum)、社论(editorial) → 过滤
- 非英语论文（除非用户要求） → 标记但不删除

排序后，仅保留 top N 篇（默认 N=80，用户可配置）进入下载管线。

---

## Phase 3: OA PDF 批量下载 (并行)

对 manifest 中有 `best_oa_location.pdf_url` 的论文，8 workers 并行 curl 下载:

```bash
curl -sL --max-time 30 -o "pdfs/{safe_title}.pdf" \
  -H "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)" \
  "{pdf_url}"
```

**验证**: 文件 > 5KB 才算成功，否则删除重试。

**NBER 论文特殊处理**: NBER PDF URL 可直接从 `landing_page_url` 推导:
- 着陆页: `https://www.nber.org/papers/w12345`
- PDF: `https://www.nber.org/system/files/working_papers/w12345/w12345.pdf`
- NBER 下载成功率接近 100%

**OA URL 下载成功率实测**:
| 来源 | 成功率 | 说明 |
|------|--------|------|
| NBER working papers | ~100% | 完全开放，最可靠 |
| institutional repo (ceibs, harvard) | ~90% | 最可靠 |
| arxiv.org | ~100% | 完全开放 |
| nature.com PDF | ~30% | 常被403 |
| ieeexplore PDF | ~50% | 部分可直下 |
| mdpi.com PDF | ~60% | 需浏览器环境 |

---

## Phase 4: OpenAlex Content API 下载 (缓存PDF)

对 OA 中没有直链但 OpenAlex 有缓存内容的论文:

```bash
curl -sL -o "pdfs/{safe_title}.pdf" \
  "https://api.openalex.org/content/works/{openalex_id}.pdf?api_key=7k74faeETXNQj8gG7jvCqR"
```

条件: `has_content.pdf == true` 的论文（约6000万篇有缓存）
成本: $0.01/篇，免费额度每天约100篇

---

## Phase 5: Unpaywall 补充 OA 检查

对 OpenAlex 未标记 OA 的论文，用 Unpaywall 补充检查:

```bash
curl -s "https://api.unpaywall.org/v2/{doi}?email=zhangjie@cufe.edu.cn"
→ best_oa_location.url_for_pdf
```

**注意**: OpenAlex 和 Unpaywall 由同一组织(OurResearch)运营，数据大量重叠。
此步仅作为补充，主要依赖 OpenAlex 自身的 OA 数据。

---

## Phase 6: 付费论文 → Sci-Hub + Chrome DevTools

对仍未下载的付费论文(closed)，走 Sci-Hub 批量下载。

### 6.1 确保专用浏览器运行

```
遵循 CLAUDE.md 中的 Chrome DevTools 专属浏览器规则:
1. 检查 curl -s http://127.0.0.1:9222/json/version 是否响应
2. 如果无响应 → 运行 bash ~/hbw_launcher.sh
3. 如果仍然失败 → pkill -9 -f "Google Chrome" → 清理 ~/.gemini/chrome_hbw_profile/Singleton* → 再运行 bash ~/hbw_launcher.sh
```

通过 Chrome DevTools MCP 连接，在 Sci-Hub 页面导航:
```
1. navigate_page → https://sci-hub.sg/{doi}
2. take_snapshot → 检查是否有 PDF
3. 如有 PDF 链接/iframe → 提取 URL → curl 下载
4. 如有 CAPTCHA → 点击"不是" → 等3-5s → 重新检查
```

### 6.2 Sci-Hub 批量下载规则 (2026实测)

| 规则 | 详情 |
|------|------|
| **镜像优先级** | `sci-hub.sg` > `sci-hub.ru` > `sci-hub.ee`。`sci-hub.se` 已下线 |
| **CAPTCHA处理** | "你是机器人吗？" → 点击"不是" → 等3-5s → 自动跳转 |
| **fetch无效** | `fetch()` API 也被CAPTCHA拦截，只有真实页面导航能通过 |
| **PDF双选择器** | 同时检查 `<a href>` 和 `<iframe src>`（不同镜像DOM不同）|
| **频率控制** | 约每3-5次导航触发一次CAPTCHA，点击后session有效约10次 |

### 6.3 批量优化

收集所有 PDF URL → 8 workers 并行 curl 下载 → 每下载5篇检查进度

---

## Phase 7: 结果汇总与报告

### 7.1 更新 manifest.json

```json
{
  "topic": "用户主题",
  "search_mode": "full|nber|top_journal|digest",
  "search_queries": ["query1", "query2", ...],
  "research_profile": "interest_id (if used)",
  "timestamp": "2026-04-23 15:00",
  "ranking_config": {
    "keyword_weight": 0.35,
    "citation_weight": 0.25,
    "journal_rank_weight": 0.25,
    "recency_weight": 0.15,
    "zotero_similarity_enabled": false
  },
  "stats": {
    "total_papers": 120,
    "after_ranking_filter": 80,
    "oa_downloaded": 35,
    "openalex_content": 8,
    "unpaywall_downloaded": 5,
    "scihub_downloaded": 28,
    "failed": 44,
    "success_rate": "63%"
  },
  "papers": [
    {
      "doi": "10.1016/...",
      "openalex_id": "W123456",
      "title": "...",
      "year": 2024,
      "cited": 45,
      "journal": "Energy Policy",
      "journal_rank": "AA",
      "oa_status": "gold",
      "rank_score": 0.82,
      "search_query": "energy transition policy",
      "source": "openalex",
      "downloaded": true,
      "download_method": "openalex_oa",
      "pdf_path": "pdfs/title.pdf"
    }
  ]
}
```

### 7.2 打印汇总

```
╔════════════════════════════════════════════════════════════╗
║  Lit-Download V7.0 结果汇总                                ║
╠════════════════════════════════════════════════════════════╣
║  主题: energy transition policy                             ║
║  检索模式: 全面检索                                          ║
║  检索次数: 8 组关键词                                        ║
║  发现论文: 120 篇 (去重后)                                   ║
║  排序筛选: 80 篇 (按智能排序保留)                             ║
║  下载成功: 76/80 (95%)                                      ║
║    OpenAlex OA: 35 | Content API: 8                        ║
║    Unpaywall: 5 | Sci-Hub: 28                              ║
║  期刊分布: AAA 22篇 | AA 18篇 | 其他 40篇                   ║
║  总耗时: ~180s                                              ║
╚════════════════════════════════════════════════════════════╝
```

---

## Phase 8: 自动深度解析 (可选)

下载完成后，触发 `/research-master` 对 `pdfs/` 目录批量解析:
- 每篇PDF → Markdown笔记 + Obsidian Canvas
- 汇总生成 `文献资产登记表_精简摘要版.xlsx`
- 用户可回复"跳过解析"来跳过

---

## 下载管线优先级

```
Phase 2A: OpenAlex API 搜索 (~3s/25篇, 精确可编程)
Phase 2B: Google Scholar 浏览器搜索 (~15s/30篇, 覆盖最广)
         ↓ 去重合并
Phase 2C: 智能排序筛选 (关键词+引用+期刊+时效)
         ↓ 排序后取 top N
Phase 3:  OpenAlex OA直链 (免费, ~3s/批并行) → 成功率约25%
    ↓ 未命中的
Phase 4: OpenAlex Content API ($0.01/篇) → 成功率约10%
    ↓ 未命中的
Phase 5: Unpaywall 补充检查 → 成功率约5%
    ↓ 仍为closed的
Phase 6: Sci-Hub + Chrome DevTools (~8s/篇) → 成功率约60%
```

**综合成功率**: ~60-65%
**总耗时**: 100篇论文约 5-10 分钟

## 搜索引擎对比

| 指标 | OpenAlex | Google Scholar | Semantic Scholar | Crossref |
|------|----------|---------------|-----------------|----------|
| 论文量 | 2.5亿 | ~3.9亿 | ~2亿 | ~1.45亿 |
| 经管覆盖 | 98.6% (最高) | 最广但无精确数据 | CS偏强，经管偏弱 | 仅DOI |
| 可编程性 | 完全API | 无API(需浏览器) | API | API |
| 搜索精度 | 高(布尔/字段/Topic) | 低(仅关键词) | 中 | 中 |
| OA PDF直链 | 直接返回 | 部分有 | 部分有 | 无 |
| 新论文速度 | 较快(天级) | 最快(小时级) | 较慢(周级) | 快(天级) |
| **角色** | **主引擎** | **补充引擎** | 备选 | 不再使用 |

## 速度基准

| 方法 | 速度 | 成功率 | 成本 |
|------|------|--------|------|
| OpenAlex 搜索发现 | ~3s/25篇 | N/A | ~$0.001/次 |
| NBER 工作论文搜索 | ~3s/25篇 | N/A | ~$0.001/次 |
| 顶刊定向搜索 | ~3s/50篇 | N/A | ~$0.001/次 |
| Google Scholar 浏览器搜索 | ~15s/30篇 | N/A | 免费(有CAPTCHA) |
| OpenAlex OA PDF直链 | ~3s/批(并行) | ~25% | 免费 |
| NBER PDF直链 | ~3s/批(并行) | ~100% | 免费 |
| OpenAlex Content API | ~1s/篇 | ~10% | $0.01/篇 |
| Unpaywall | ~3s/批 | ~5% | 免费 |
| Sci-Hub + Chrome | ~8s/篇 | ~60% | 免费 |
| PyPaperBot | N/A | **0%** (2026失效) | N/A |

## 已知限制

1. 经管类论文多在付费墙后 (Elsevier, Wiley等)，OA比例约20-30%
2. OpenAlex Content API 缓存覆盖率经管类偏低（约10%有PDF缓存）
3. Sci-Hub 收录率约60%，2025-2026新论文更低
4. Sci-Hub CAPTCHA频率约每3-5次触发一次
5. 部分出版商(MDPI等)需要浏览器环境，curl被拒
6. PyPaperBot/scidownl 在2026年完全失效（无法处理CAPTCHA）
7. 顶刊模式中期刊别名需精确匹配，模糊匹配可能遗漏

## 经管类特化功能

### 顶刊筛选

OpenAlex 支持按期刊 Source ID 筛选，常用经管顶刊:
- Energy Policy: `S13631` (Source ID)
- Journal of Finance: 搜索 `primary_location.source.display_name:Journal of Finance`
- 可用 OpenAlex MCP 的 `search_in_journal_list` 工具，内置 FT50/UTD24/AJG 期刊列表

### NBER 工作论文

NBER 是经济学研究的前沿阵地:
- Source ID: `S27349830`
- 几乎100% OA，免费PDF
- 很多后来发表在五大顶刊
- 时效性强，比正式发表早6-18个月
- 按发表日期倒序比按引用排序更有价值

### Topic 精确匹配

OpenAlex 有 ~4500 个 Topics，经管类常用:
- 搜索时用 `primary_topic.display_name` 查看论文归属的 Topic
- 可用 Topic ID 精确筛选: `primary_topic.id:Txxxxx`

### CUFE 期刊目录集成

集成中央财经大学期刊目录（2025版）145+ 本期刊:
- **AAA (68本)**: 五大顶刊(AER/JPE/QJE/RES/ECMA) + JPubE/JUE/JHE 等
- **AA (87本)**: 次顶级期刊，经管各子领域最佳
- 每本期刊都有 OpenAlex Source ID，可直接用于API筛选
- 期刊等级用于智能排序中的 journal_rank_score

### Research Interest Profile 复用

首次使用时创建的 `research_profile.json` 可在后续同类主题中复用:
- 避免重复的关键词设计工作
- 排除词(exclude_keywords)持续过滤不相关论文
- query_aliases 自动扩展搜索覆盖面
