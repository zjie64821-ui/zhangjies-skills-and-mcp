---
name: youtube-dl
description: >
  YouTube video downloader using yt-dlp. TRIGGER when the user wants to: download a YouTube video,
  save a YouTube video offline, extract audio from YouTube as MP3, download videos with specific
  quality or format requirements.
  Keywords: YouTube下载, 下载视频, YouTube, download video, yt-dlp, save video.
  DO NOT trigger for non-YouTube video URLs or streaming tasks.
---

# YouTube 视频下载器

## 使用方法
```bash
python "/Users/zhangjie/.gemini/skills/youtube-downloader/scripts/download_video.py" "URL" [选项]
```

## 选项
| 参数 | 说明 | 默认 |
|------|------|------|
| `-q` | 质量: best/1080p/720p/480p/360p/worst | best |
| `-f` | 格式: mp4/webm/mkv | mp4 |
| `-a` | 仅音频 MP3 | off |
| `-o` | 输出目录 | `/mnt/user-data/outputs/` |

## 示例
```bash
# 720p MP4
python .../download_video.py "URL" -q 720p
# 仅音频
python .../download_video.py "URL" -a
```

## 用户请求
$ARGUMENTS
