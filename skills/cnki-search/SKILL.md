---
name: cnki-search
description: >
  CNKI (中国知网) academic paper search via Chrome DevTools. TRIGGER when the user wants to:
  search CNKI/知网 for Chinese academic papers; find Chinese journal articles; search for
  dissertations/theses on CNKI.
  Keywords: 知网搜索, CNKI搜索, 中文论文, 中国知网, 中文期刊, 学位论文.
  DO NOT trigger for Google Scholar, ScienceDirect, or other non-CNKI searches.
---

# CNKI 知网搜索

通过 Chrome DevTools MCP 在 CNKI 搜索学术论文。

## 工作流 (2 tool calls)
1. `mcp__chrome-devtools__navigate_page` → `https://kns.cnki.net/kns8s/search`
2. `mcp__chrome-devtools__evaluate_script` — 填入关键词、搜索、抓取结果

## 搜索+提取脚本
```javascript
async () => {
  const query = "关键词";
  await new Promise((r,j)=>{let n=0;const c=()=>{if(document.querySelector('input.search-input'))r();else if(++n>30)j('timeout');else setTimeout(c,500);};c();});
  const outer = document.querySelector('#tcaptcha_transform_dy');
  if (outer && outer.getBoundingClientRect().top >= 0) return { error: 'captcha' };
  const input = document.querySelector('input.search-input');
  input.value = query;
  input.dispatchEvent(new Event('input', { bubbles: true }));
  document.querySelector('input.search-btn')?.click();
  await new Promise((r,j)=>{let n=0;const c=()=>{if(document.body.innerText.includes('条结果'))r();else if(++n>30)j('timeout');else setTimeout(c,500);};c();});
  const outer2 = document.querySelector('#tcaptcha_transform_dy');
  if (outer2 && outer2.getBoundingClientRect().top >= 0) return { error: 'captcha' };
  const rows = document.querySelectorAll('.result-table-list tbody tr');
  const results = Array.from(rows).map((row, i) => ({
    n: i+1,
    title: row.querySelector('td.name a.fz14')?.innerText?.trim(),
    href: row.querySelector('td.name a.fz14')?.href,
    authors: Array.from(row.querySelectorAll('td.author a.KnowledgeNetLink')).map(a=>a.innerText?.trim()).join('; '),
    journal: row.querySelector('td.source a')?.innerText?.trim(),
    date: row.querySelector('td.date')?.innerText?.trim(),
    citations: row.querySelector('td.quote')?.innerText?.trim(),
    downloads: row.querySelector('td.download')?.innerText?.trim()
  }));
  return { query, total: document.querySelector('.pagerTitleCell')?.innerText?.match(/([\d,]+)/)?.[1], results };
}
```

## 验证码检测
`#tcaptcha_transform_dy` 的 `getBoundingClientRect().top >= 0` 表示弹出

## 关键选择器
搜索框: `input.search-input` | 搜索按钮: `input.search-btn` | 标题: `td.name a.fz14`

## 搜索关键词
$ARGUMENTS
