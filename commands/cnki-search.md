# CNKI 知网搜索

通过 Chrome DevTools MCP 在 CNKI 搜索学术论文。

## 工作流
1. **导航**: 使用 `mcp__chrome-devtools__navigate_page` → `https://kns.cnki.net/kns8s/search`
2. **搜索+提取**: 使用 `mcp__chrome-devtools__evaluate_script` 执行搜索并抓取结果

## 搜索脚本核心逻辑
```javascript
async () => {
  const query = "关键词";
  // 等待搜索框
  await new Promise((r, j) => {
    let n = 0;
    const c = () => { if (document.querySelector('input.search-input')) r(); else if (++n > 30) j('timeout'); else setTimeout(c, 500); };
    c();
  });
  // 检查验证码
  const outer = document.querySelector('#tcaptcha_transform_dy');
  if (outer && outer.getBoundingClientRect().top >= 0) return { error: 'captcha' };
  // 填入关键词并搜索
  const input = document.querySelector('input.search-input');
  input.value = query;
  input.dispatchEvent(new Event('input', { bubbles: true }));
  document.querySelector('input.search-btn')?.click();
  // 等待结果
  await new Promise((r, j) => {
    let n = 0;
    const c = () => { if (document.body.innerText.includes('条结果')) r(); else if (++n > 30) j('timeout'); else setTimeout(c, 500); };
    c();
  });
  // 提取结果
  const rows = document.querySelectorAll('.result-table-list tbody tr');
  const results = Array.from(rows).map((row, i) => ({
    n: i + 1,
    title: row.querySelector('td.name a.fz14')?.innerText?.trim(),
    href: row.querySelector('td.name a.fz14')?.href,
    authors: Array.from(row.querySelectorAll('td.author a.KnowledgeNetLink')).map(a => a.innerText?.trim()).join('; '),
    journal: row.querySelector('td.source a')?.innerText?.trim(),
    date: row.querySelector('td.date')?.innerText?.trim(),
    citations: row.querySelector('td.quote')?.innerText?.trim(),
    downloads: row.querySelector('td.download')?.innerText?.trim()
  }));
  return { query, total: document.querySelector('.pagerTitleCell')?.innerText?.match(/([\d,]+)/)?.[1], results };
}
```

## 验证码处理
检查 `#tcaptcha_transform_dy` 的 `getBoundingClientRect().top >= 0`（腾讯验证码预加载 DOM 在 top:-1000000px，仅 top>=0 时为真正弹出）

## 关键选择器
| 元素 | 选择器 |
|------|--------|
| 搜索框 | `input.search-input` |
| 搜索按钮 | `input.search-btn` |
| 结果总数 | `.pagerTitleCell` |
| 标题链接 | `td.name a.fz14` |
| 作者 | `td.author a.KnowledgeNetLink` |
| 期刊 | `td.source a` |
| 日期 | `td.date` |
| 被引 | `td.quote` |
| 下载 | `td.download` |

## 搜索关键词
$ARGUMENTS
