import yt_dlp
import os
import sys
import moviepy as mp
import logging

# 配置日志记录
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 配置选项
DEFAULT_FORMAT = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'

# 修改 download_and_convert 函数以使用配置选项
def download_and_convert(url, output_dir="."):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 配置yt-dlp下载选项
    ydl_opts = {
        'format': DEFAULT_FORMAT,  # 使用配置选项
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
    }
    try:
        # 下载视频
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            if 'entries' in info:
                # 处理多个视频的情况
                for entry in info['entries']:
                    if entry is not None:
                        video_title = entry.get('title', 'unknown_title')
                        video_ext = entry.get('ext', 'mp4')
                        video_file = f"{video_title}.{video_ext}"
                        video_path = os.path.join(output_dir, video_file)
                        try:
                            ydl.download([entry['webpage_url']])
                            if os.path.exists(video_path) and os.access(video_path, os.R_OK):
                                video = mp.VideoFileClip(video_path)
                                audio = video.audio
                                audio_path = os.path.join(output_dir, f"{video_title}.mp3")
                                audio.write_audiofile(audio_path)
                                logging.info(f'已生成音频文件: {audio_path}')
                            else:
                                logging.error(f'无法访问视频文件: {video_path}')
                        except Exception as e:
                            logging.error(f'处理视频 {video_title} 时出错: {str(e)}')
            else:
                # 处理单个视频的情况
                video_title = info.get('title', 'unknown_title')
                video_ext = info.get('ext', 'mp4')
                video_file = f"{video_title}.{video_ext}"
                video_path = os.path.join(output_dir, video_file)
                ydl.download([url])
                if os.path.exists(video_path) and os.access(video_path, os.R_OK):
                    video = mp.VideoFileClip(video_path)
                    audio = video.audio
                    audio_path = os.path.join(output_dir, f"{video_title}.mp3")
                    audio.write_audiofile(audio_path)
                    logging.info(f'已生成音频文件: {audio_path}')
                else:
                    logging.error(f'无法访问视频文件: {video_path}')
    except Exception as e:
        logging.error(f'处理过程中出错: {str(e)}')

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("使用方法: python bilibili_downloader.py <B站视频URL> [输出目录]")
        sys.exit(1)
    
    url = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "downloads"
    
    download_and_convert(url, output_dir)
