"""
The script purpose is to download videos and reels from Youtube and split them to single images.
There is transitional step - converting webm to mp4 format since Pillow lib is not supported that extension
"""

import os
import argparse
import datetime
import numpy as np
from PIL import Image
from yt_dlp import YoutubeDL
from moviepy.editor import VideoFileClip


def argument_parsing() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--links_to_videos", type=str, nargs='+', required=True, dest='urls',
                        help="List of video URL's to download"
                         """Example:
                         --links_to_videos
                         https://youtube.com/shorts/V
                         https://youtube.com/shorts/y
                         https://youtube.com/shorts/N""",
                        default=os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                             f'{str(datetime.date.today())}_output'))
    parser.add_argument("--output", type=str, required=True,
                        help="Path where to save the outputs: videos and images")

    args = parser.parse_args()
    return args


def download_video(url: str, downloaded_videos_out: str) -> None:
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': os.path.join(downloaded_videos_out, '%(title)s.%(ext)s'),
        'noplaylist': True,
        'quiet': True}

    with YoutubeDL(ydl_opts) as ydl:
        ydl.extract_info(url, download=True)

    return None


def convert_video(video: str, converted_videos_out: str) -> None:
    clip = VideoFileClip(video)

    video_path_mp4 = os.path.join(converted_videos_out, os.path.basename(video).replace('.webm', '.mp4'))
    clip.write_videofile(video_path_mp4, codec="libx264", audio=False)

    return None


def split_video_into_frames(video_mp4: str, output_folder: str) -> None:

    out = os.path.join(output_folder, os.path.basename(video_mp4)[:-4])
    os.makedirs(out, exist_ok=True)
    clip = VideoFileClip(video_mp4)
    fps = clip.fps
    duration = clip.duration
    for frame_id in range(int(duration * fps)):
        frame = clip.get_frame(frame_id / fps)
        frame = np.array(frame)
        pil_image = Image.fromarray(frame.astype(np.uint8))
        frame_name = f"{out}/frame_{frame_id}.jpg"

        pil_image.save(frame_name)

    return None


def run_download_video(urls: list, output: str):

    """download videos by url"""
    downloaded_videos_out = os.path.join(output, 'downloaded_videos')
    os.makedirs(downloaded_videos_out, exist_ok=True)
    for url in urls:
        download_video(url, downloaded_videos_out)

    """convert videos from .webm to .mp4"""
    converted_videos_out = os.path.join(output, 'converted_videos')
    os.makedirs(converted_videos_out, exist_ok=True)
    for video in os.listdir(downloaded_videos_out):
        convert_video(os.path.join(downloaded_videos_out, video), converted_videos_out)

    """split video to frames"""
    single_images = os.path.join(output, 'single_images')
    os.makedirs(single_images, exist_ok=True)

    for conv_video in os.listdir(converted_videos_out):
        split_video_into_frames(os.path.join(converted_videos_out, conv_video), single_images)


if __name__ == '__main__':

    args = argument_parsing()
    os.makedirs(args.output, exist_ok=True)
    run_download_video(args.urls, args.output)
