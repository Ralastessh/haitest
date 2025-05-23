import os
import ffmpeg

def convert_m4a_to_wav(input_file):
    output_file = os.path.splitext(input_file)[0] + '.wav'
    try:
        ffmpeg.input(input_file).output(output_file, ar=16000, ac=1, format='wav').run(overwrite_output=True)
        print(f'Successfully converted to WAV')
    except ffmpeg.Error as e:
        print(f'Converting is failed! | {e}')
        