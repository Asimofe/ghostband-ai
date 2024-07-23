import requests
import time

# 플라스크가 실행되는 서버의 URL, 예시: http://123.123.123.123:1234
server_ip = '127.0.0.1:5000'

def stop_model():
    url = f'{server_ip}/stop_process'
    response = requests.post(url)
    if response.status_code == 200:
        print('Process terminated successfully')
        print(response.json())
    else:
        print('Failed to terminate process')
        print(response.json())

if __name__ == '__main__':
    
    # 프로세스 중지 req
    stop_model()

