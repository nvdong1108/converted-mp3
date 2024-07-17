

import os
import subprocess
import speech_recognition as sr
from pydub import AudioSegment

ffmpeg_path = subprocess.Popen(["where", "ffmpeg"], stdout=subprocess.PIPE).communicate()[0].decode().strip()
ffprobe_path = subprocess.Popen(["where", "ffprobe"], stdout=subprocess.PIPE).communicate()[0].decode().strip()

if not ffmpeg_path:
    raise EnvironmentError("ffmpeg không được tìm thấy trong PATH")
if not ffprobe_path:
    raise EnvironmentError("ffprobe không được tìm thấy trong PATH")

print("ffmpeg path:", ffmpeg_path)
print("ffprobe path:", ffprobe_path)

audio_file = r"C:\SourceCode\DongNV\Git\ConvertedMP3\File 6.mp3"

# Đảm bảo AudioSegment sử dụng đúng trình chuyển đổi
AudioSegment.converter = ffmpeg_path
AudioSegment.ffprobe = ffprobe_path

# Chuyển đổi MP3 thành WAV
sound = AudioSegment.from_file(audio_file, format="mp3", ffmpeg=ffmpeg_path, ffprobe=ffprobe_path)

chunk_length_ms = 10000  # 10 giây
chunks = len(sound) // chunk_length_ms + 1
for i in range(chunks):
    start = i * chunk_length_ms
    end = (i + 1) * chunk_length_ms
    segment = sound[start:end]
    segment.export(f"converted_part_{i}.wav", format="wav", parameters=["-ac", "1"])  # Thêm tham số để xử lý âm thanh


# sound = AudioSegment.from_mp3(audio_file)
# sound.export("converted.wav", format="wav")

recognizer = sr.Recognizer()

recognized_text = ""

for i in range(chunks):
    with sr.AudioFile(f"converted_part_{i}.wav") as source:
        audio_data = recognizer.record(source)
        text = recognizer.recognize_google(audio_data)
        recognized_text += text + " "


# Mở file .wav và chuyển đổi thành văn bản
# with sr.AudioFile("converted.wav") as source:
#     audio_data = recognizer.record(source)
#     text = recognizer.recognize_google(audio_data)

print("Recognized text:", recognized_text)