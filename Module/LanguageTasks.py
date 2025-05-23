import json
import tiktoken
import os
from openai import OpenAI  
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def count_tokens(text, model="gpt-4"):
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))

def extract_highlight_only(transcript, max_tokens=3000, model="gpt-4"):
    

    formatted_segments = []
    total_tokens = 0

    for i, seg in enumerate(transcript):
        line = f"[{seg.start:.2f} - {seg.end:.2f}] {seg.text}"
        tokens = count_tokens(line, model=model)
        if total_tokens + tokens > max_tokens:
            break
        formatted_segments.append(f"{i}: {line}")
        total_tokens += tokens

    full_script = "\n".join(formatted_segments)

    prompt = f"""
유튜브 쇼츠 영상 편집자입니다. 영상 전체 자막을 주겠습니다.
각 줄은 자막의 인덱스, 시간, 텍스트로 구성되어 있습니다.

가장 흥미롭고 감정적으로 강한 한 부분만 선택해서 출력하세요.
각 하이라이트는 다음과 같은 JSON 형식으로 1개만 반환하세요:

[
  {{ "start": 15.2, "end": 18.1 }}
]

스크립트:
{full_script}
"""

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are an expert YouTube Shorts editor."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            timeout=60  # 60 seconds timeout
        )

        content = response.choices[0].message.content.strip()

        try:
            highlights = json.loads(content)
            return highlights
        except json.JSONDecodeError:
            print("⚠️ GPT 응답이 JSON이 아님. 원본 출력:\n", content)
            return []

    except Exception as e:
        print("❌ GPT highlight extraction failed:", e)
        return []
