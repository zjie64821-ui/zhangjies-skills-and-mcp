# Google Scholar 搜索

通过 Chrome DevTools MCP 在 Google Scholar 搜索学术论文。

## 工作流
1. **导航**: `mcp__chrome-devtools__navigate_page` → `https://scholar.google.com/scholar?q={URL编码关键词}&hl=en&num=10`
2. **提取结果**: `mcp__chrome-devtools__evaluate_script` 抓取 DOM

## 提取脚本核心逻辑
```javascript
async () => {
  for (let i = 0; i < 20; i++) {
    if (document.querySelector('#gs_res_ccl') || document.querySelector('#gs_captcha_ccl')) break;
    await new Promise(r => setTimeout(r, 500));
  }
  if (document.querySelector('#gs_captcha_ccl') || document.body.innerText.includes('unusual traffic')) {
    return { error: 'captcha', message: 'Google Scholar 需要验证码，请在浏览器中完成。' };
  }
  const items = document.querySelectorAll('#gs_res_ccl .gs_r.gs_or.gs_scl');
  const results = Array.from(items).map((item, i) => {
    const titleEl = item.querySelector('.gs_rt a');
    const meta = item.querySelector('.gs_a')?.textContent || '';
    const parts = meta.split(' - ');
    return {
      n: i + 1,
      title: titleEl?.textContent?.trim(),
      href: titleEl?.href,
      authors: parts[0]?.trim(),
      journalYear: parts[1]?.trim(),
      citedBy: item.querySelector('.gs_fl a[href*="cites"]')?.textContent?.match(/\d+/)?.[0] || '0',
      dataCid: item.getAttribute('data-cid'),
      fullTextUrl: (item.querySelector('.gs_ggs a') || item.querySelector('.gs_or_ggsm a'))?.href || '',
      snippet: item.querySelector('.gs_rs')?.textContent?.trim()?.substring(0, 200)
    };
  });
  return { total: document.querySelector('#gs_ab_md')?.textContent?.trim(), results };
}
```

## 验证码处理
返回 `{error: 'captcha'}` 时，告知用户在浏览器中完成验证码后重试。

## 注意
- 无公共 API，全部通过 DOM 抓取
- `dataCid` 是唯一标识符，用于引用导出和"被引"追踪
- 控制请求频率避免触发验证码
- 默认 `num=10`（最大 20）

## 后续操作
- 翻页：修改 URL 的 `start=` 参数
- 被引追踪：使用 `gs-cited-by` 逻辑
- 导出 Zotero：使用 `gs-export` 逻辑

## 搜索关键词
$ARGUMENTS
