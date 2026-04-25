# YouTube 视频下载器

使用 yt-dlp 下载 YouTube 视频，支持多种质量和格式。

## 使用方法
```bash
# 默认：最高质量 MP4
python "/Users/zhangjie/.gemini/skills/youtube-downloader/scripts/download_video.py" "URL"

# 指定质量
python "/Users/zhangjie/.gemini/skills/youtube-downloader/scripts/download_video.py" "URL" -q 720p

# 指定格式
python "/Users/zhangjie/.gemini/skills/youtube-downloader/scripts/download_video.py" "URL" -f webm

# 仅音频 MP3
python "/Users/zhangjie/.gemini/skills/youtube-downloader/scripts/download_video.py" "URL" -a

# 自定义输出目录
python "/Users/zhangjie/.gemini/skills/youtube-downloader/scripts/download_video.py" "URL" -o /path/to/dir
```

## 质量选项
- `best` (默认) / `1080p` / `720p` / `480p` / `360p` / `worst`

## 格式选项
- `mp4` (默认) / `webm` / `mkv`

## 默认输出目录
`/mnt/user-data/outputs/`（可用 -o 自定义）

## 用户请求
$ARGUMENTS
