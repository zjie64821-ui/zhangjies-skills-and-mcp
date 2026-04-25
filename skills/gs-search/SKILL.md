---
name: gs-search
description: >
  Google Scholar academic paper search via Chrome DevTools. TRIGGER when the user wants to:
  search Google Scholar for academic papers; find English-language research articles;
  check citation counts; find open-access full-text links for papers.
  Keywords: Google Scholar搜索, 学术搜索, 英文论文, citation search, scholar.
  DO NOT trigger for CNKI, ScienceDirect, or general web searches.
---

# Google Scholar 搜索

通过 Chrome DevTools MCP 搜索 Google Scholar。

## 工作流 (2 tool calls)
1. `mcp__chrome-devtools__navigate_page` → `https://scholar.google.com/scholar?q={URL编码关键词}&hl=en&num=10`
2. `mcp__chrome-devtools__evaluate_script` — 抓取结果

## 提取脚本
```javascript
async () => {
  for(let i=0;i<20;i++){if(document.querySelector('#gs_res_ccl')||document.querySelector('#gs_captcha_ccl'))break;await new Promise(r=>setTimeout(r,500));}
  if(document.querySelector('#gs_captcha_ccl')||document.body.innerText.includes('unusual traffic'))return{error:'captcha',message:'需要验证码，请在浏览器中完成。'};
  const items=document.querySelectorAll('#gs_res_ccl .gs_r.gs_or.gs_scl');
  const results=Array.from(items).map((item,i)=>{
    const titleEl=item.querySelector('.gs_rt a');
    const meta=item.querySelector('.gs_a')?.textContent||'';
    const parts=meta.split(' - ');
    return{n:i+1,title:titleEl?.textContent?.trim(),href:titleEl?.href,authors:parts[0]?.trim(),journalYear:parts[1]?.trim(),citedBy:item.querySelector('.gs_fl a[href*="cites"]')?.textContent?.match(/\d+/)?.[0]||'0',dataCid:item.getAttribute('data-cid'),fullTextUrl:(item.querySelector('.gs_ggs a')||item.querySelector('.gs_or_ggsm a'))?.href||'',snippet:item.querySelector('.gs_rs')?.textContent?.trim()?.substring(0,200)};
  });
  return{total:document.querySelector('#gs_ab_md')?.textContent?.trim(),results};
}
```

## 注意
- `dataCid` 是唯一标识符，用于引用导出和被引追踪
- 控制频率避免验证码
- 默认 10 条/页（最大 20）

## 搜索关键词
$ARGUMENTS
