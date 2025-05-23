import os
import subprocess

class VideoClipper:
    def __init__(self, input_video_path, output_dir="Input"):
        self.input_video_path = input_video_path
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def extract_clips(self, clip_timestamps):
        for clip in clip_timestamps:
            clip_id = clip["id"]
            start = clip["start"]
            duration = float(clip["end"]) - float(clip["start"])

            output_video = os.path.join(self.output_dir, f"{clip_id}.mp4")
            output_audio = os.path.join(self.output_dir, f"{clip_id}.wav")

            # mp4 자르기
            subprocess.run([
                "ffmpeg", "-y", "-i", self.input_video_path,
                "-ss", str(start), "-t", str(duration),
                "-c", "copy", output_video
            ])

            # 오디오 추출
            subprocess.run([
                "ffmpeg", "-y", "-i", output_video,
                "-ar", "16000", "-ac", "1", output_audio
            ])

            print(f"✅ {clip_id}: 잘림 완료 → {output_video}, {output_audio}")