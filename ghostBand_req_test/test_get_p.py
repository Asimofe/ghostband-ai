import requests
import os
from datetime import datetime

now = datetime.now()
current_time = now.strftime("%Y%m%d_%H%M")

# 서버에 POST 요청 보내기
# 플라스크가 실행되는 서버의 URL/run_model, 예시: http://123.123.123.123:1234/run_model
url = ''
data = {
    "selected_instruments": ["guitar", "bass", "drum"],
    "genre": "jazz",
    "time_signature": "3/4",
    "playtime": "50",
    "bars": "13",
    "pitch_range": "5",
    "key": "C major",
    "tempo": "moderate",
    "current_time": current_time
}

response = requests.post(url, json=data)
response_data = response.json()

# 파일 URL 목록 받기
file_urls = response_data.get('file_urls', [])

# 각 파일을 다운로드하기 위해 curl 명령어 실행
for file_url in file_urls:
    file_name = file_url.split('/')[-1]
    os.system(f'curl -O {file_url}')

