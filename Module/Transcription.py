import json
from datetime import timedelta
from faster_whisper import WhisperModel
import torch

device = 'cuda' if torch.cuda.is_available() else 'cpu'

# 자막 생성
def audio_transcribe(audio_file):
    model = WhisperModel("large-v3", device=device, compute_type=('float16' if device == 'cuda' else 'int8'))
    segments, info = model.transcribe(audio_file, beam_size=5, patience= 2, word_timestamps=True)

    # 각 문장 및 단어 별 타임스탬프를 포함한 자막 저장
    print(f'Detected language: {info.language} (Probability={info.language_probability:.2f})\n')
    segments = list(segments)

    # 문장 출력
    for seg in segments:
        print(f'[{seg.start:.2f}s → {seg.end:.2f}s] {seg.text}')
        # 문장 속 단어 출력
        for w in seg.words:
            print(f'   {w.start:.2f}s–{w.end:.2f}s: {w.word}')
        print()
    return segments, audio_file

# JSON으로 자막 저장
def save_transcript_json(segments, audio_file):  
    try:    
        json_path = audio_file.rsplit('.', 1)[0] + '.json'
        with open(json_path, 'w', encoding='utf-8') as jf:
            json.dump([{
                "start": seg.start,
                "end": seg.end,
                "text": seg.text,
                "words": [{"start": w.start, "end": w.end, "word": w.word} for w in seg.words]
            } for seg in segments], jf, ensure_ascii=False, indent=2)
        
        print(f'Transcript file saved to: {json_path}')
        
    except Exception as e:
        print(f'Failed to save transcript: {e}')

# SRT로 자막 저장
def save_transcript_srt(segments, audio_file):
    def timestamp(seconds: float) -> str:
        td = timedelta(seconds=seconds)
        hrs, rem = divmod(td.seconds, 3600)
        mins, secs = divmod(rem, 60)
        millis = td.microseconds // 1000
        return f'{hrs:02}:{mins:02}:{secs:02},{millis:03}'
    
    try:
        srt_path = audio_file.rsplit('.', 1)[0] + '.srt'
        
        with open(srt_path, 'w', encoding='utf-8') as sf:
            for index, seg in enumerate(segments, start=1):
                sf.write(f"{index}\n")
                sf.write(f"{timestamp(seg.start)} --> {timestamp(seg.end)}\n")
                sf.write(f"{seg.text.strip()}\n\n")
        
        print(f'Subtitle file saved to: {srt_path}')
        
    except Exception as e:
        print(f'Failed to save subtitle: {e}')
