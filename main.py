from Module.YoutubeDownloader import download_youtube_video
from Module.Transcription import *
from Module.LanguageTasks import extract_highlight_only
from Module.VideoClipper import VideoClipper
from dotenv import load_dotenv
import json
import os

load_dotenv()

def main():
    url = input("Enter YouTube video URL: ").strip()

    merged_path, _, audio_path = download_youtube_video(url)

    if merged_path:
        print(f"\nDownload complete! Saved to: {merged_path}")
    else:
        print("\nDownload or merge failed.")
        
    print('\nTranscribing audio...')    
    transcription, audio = audio_transcribe(audio_path) 
    os.makedirs("Output", exist_ok=True)
    save_transcript_json(transcription, audio)
    save_transcript_srt(transcription, audio)
    
    if transcription:
        print("\nTranscription complete!")
        print("\n Extracting highlight segments using GPT...")
        highlighted_transcript = extract_highlight_only(transcription)

        print(f"\n Found {len(highlighted_transcript)} highlight segments:")
        for h in highlighted_transcript:
            print(f"[{h['start']} - {h['end']}]")

        with open("Output/highlight_transcript.json", "w", encoding="utf-8") as f:
            json.dump(highlighted_transcript, f, indent=2, ensure_ascii=False)
        print("\n✂️ Clipping video/audio by highlight timestamps...")
        clipper = VideoClipper(input_video_path=merged_path, output_dir="Input")
        clip_list = [
            {"id": f"clip{idx+1:03}", "start": h["start"], "end": h["end"]}
            for idx, h in enumerate(highlighted_transcript)
        ]
        clipper.extract_clips(clip_list)
        
    else:
        print("\nTranscription failed.")
    
if __name__ == "__main__":
    main()
