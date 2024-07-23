# Use MuseCoco with flask / jongha1257@gmail.com

import logging
import json
import subprocess
import os
import random
import time
from flask import Flask, request, jsonify, send_file, make_response
from flask_cors import CORS 

app = Flask(__name__)
#CORS(app, resources={r"/api/*": {"origins": "*"}})


# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 현재 실행 중인 프로세스의 PID를 저장하기 위한 전역 변수
current_pid = None
stop_flag = False
project_path = "/home/clark/workspace/muzic/musecoco/"

# 허용할 IP 주소 목록
# allowed_ips = {}

# @app.before_request
# def block_ips():
#     if request.remote_addr not in allowed_ips:
#         message = {
#             'status': 403,
#             'message': 'Forbidden: Your IP address is not allowed to access this resource.'
#         }
#         return make_response(jsonify(message), 403)



available_artist = {
    'beethoven': 'Beethoven',
    'mozart': 'Mozart',
    'chopin': 'Chopin',
    'schubert': 'Schubert',
    'schumann': 'Schumann',
    'bach-js': 'Bach',
    'haydn': 'Haydn',
    'brahms': 'Brahms',
    'handel': 'Handel',
    'tchaikovsky': 'Tchaikovsky',
    'mendelssohn': 'Mendelssohn',
    'dvorak': 'Dvorak',
    'liszt': 'Liszt',
    'stravinsky': 'Stravinsky',
    'mahler': 'Mahler',
    'prokofiev': 'Prokofiev',
    'shostakovich': 'Shostakovich',
}

# Attribute2Text 변환
def create_music_description(instruments, genre, time_signature, playtime, bars, pitch_range, key, tempo):
    template = ("The use of [instruments] is vital to the music's overall sound and performance. "
                "This music follows the style of [Artist]. "
                "It follows a [time_signature] time signature and has a playtime of approximately [playtime] seconds. "
                "The music spans about [bars] bars and utilizes a pitch range of [pitch_range] octaves. "
                "Composed in the [key] key and played at a [tempo] tempo, it falls under the [genre] genre.")
    selected_instruments = ', '.join(instruments[:-1]) + ', and ' + instruments[-1] if len(instruments) > 1 else instruments[0]

    artist = random.choice(list(available_artist.values()))

    # 템플릿에 사용자 입력 값을 삽입
    description = template.replace("[instruments]", selected_instruments)
    description = description.replace("[Artist]", artist) 
    description = description.replace("[time_signature]", time_signature)
    description = description.replace("[playtime]", str(playtime))
    description = description.replace("[bars]", str(bars))
    description = description.replace("[pitch_range]", str(pitch_range))
    description = description.replace("[key]", key)
    description = description.replace("[tempo]", tempo)
    description = description.replace("[genre]", genre)

    result = [{"text": description}]
    
    with open("/home/clark/workspace/muzic/musecoco/1-text2attribute_model/data/music_description.json", "w", encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False)
    return result

def get_child_pids(parent_pid):
    try:
        result = subprocess.run(['pgrep', '-P', str(parent_pid)], capture_output=True, text=True, check=True)
        return [int(pid) for pid in result.stdout.split()]
    except subprocess.CalledProcessError:
        return []

@app.route('/run_model', methods=['POST'])
def run_model():
    global current_pid, stop_flag

    if stop_flag:
        stop_flag = False  # 플래그를 초기화하여 새 작업이 시작될 수 있도록 함

    if current_pid:
        return jsonify({'message': 'A process is already running'}), 400

    data = request.get_json() or {}
    selected_instruments = data.get("selected_instruments", [])
    genre = data.get("genre", "")
    time_signature = data.get("time_signature", "")
    playtime = data.get("playtime", "")
    bars = data.get("bars", "")
    pitch_range = data.get("pitch_range", "")
    key = data.get("key", "")
    tempo = data.get("tempo", "")
    current_time = data.get("current_time", "")
    app.config['CURRENT_TIME'] = current_time

    description = create_music_description(selected_instruments, genre, time_signature, playtime, bars, pitch_range, key, tempo)
    logger.info(f'Description created: {description}')

    midi_path = f"../2-attribute2music_model/generation/{current_time}/linear_mask-1billion-attribute2music/infer_test/topk15-t1.0-ngram0/0/midi/{current_time}.mid"
    sheet_music_path_pdf = f"../2-attribute2music_model/generation/{current_time}/linear_mask-1billion-attribute2music/infer_test/topk15-t1.0-ngram0/0/midi/{current_time}.pdf"

    try:
        # predict.sh 파일 실행
        process = subprocess.Popen(['bash', '/home/clark/workspace/muzic/musecoco/1-text2attribute_model/predict.sh'])
        current_pid = process.pid
        logger.info(f'predict.sh started with PID {current_pid}')
        process.wait()
        logger.info('predict.sh executed successfully.')

        if stop_flag:
            raise Exception('Process stopped by user.')

        # stage2_pre.py 파일 실행
        process = subprocess.Popen(['python3', '/home/clark/workspace/muzic/musecoco/1-text2attribute_model/stage2_pre.py'])
        current_pid = process.pid
        logger.info(f'stage2_pre.py started with PID {current_pid}')
        process.wait()
        logger.info('stage2_pre.py executed successfully.')

        if stop_flag:
            raise Exception('Process stopped by user.')

        # interactive_1billion.sh 파일 실행
        process = subprocess.Popen(['bash', '/home/clark/workspace/muzic/musecoco/2-attribute2music_model/interactive_1billion.sh', '0', '1', current_time])
        current_pid = process.pid
        logger.info(f'interactive_1billion.sh started with PID {current_pid}')
        process.wait()
        logger.info('interactive_1billion.sh executed successfully.')

        if stop_flag:
            raise Exception('Process stopped by user.')

        # remi2midi.py 파일 실행
        process = subprocess.Popen(['python3', '/home/clark/workspace/muzic/musecoco/2-attribute2music_model/remi2midi.py', current_time])
        current_pid = process.pid
        logger.info(f'remi2midi.py started with PID {current_pid}')
        process.wait()
        logger.info('remi2midi.py executed successfully.')

        if stop_flag:
            raise Exception('Process stopped by user.')

        # 악보 변환 명령어 실행
        process = subprocess.Popen(['xvfb-run', '-a', 'musescore3', midi_path, '-o', sheet_music_path_pdf])
        current_pid = process.pid
        logger.info(f'musescore3 started with PID {current_pid}')
        process.wait()
        logger.info(f'Successfully converted {current_time}.mid to {current_time}.pdf')

        if stop_flag:
            raise Exception('Process stopped by user.')

        # 모든 작업이 완료되면 current_pid를 None으로 리셋
        current_pid = None

    except Exception as e:
        logger.error(f'An error occurred: {e}')
        current_pid = None
        return jsonify({'message': 'An error occurred', 'error': str(e)}), 500

    file_urls = [
        # your server ip address
        #f'http://{server ip address}:5005/download_file/{current_time}.mid',
        #f'http://{server ip address}:5005/download_file/{current_time}.pdf'
    ]

    return jsonify({'message': 'Data received and description created', 'file_urls': file_urls})

@app.route('/stop_process', methods=['POST'])
def stop_process():
    global stop_flag, current_pid

    if not current_pid:
        return jsonify({'message': 'No process is currently running'}), 400

    stop_flag = True

    try:
        # 현재 PID와 자식 PID들을 가져와서 종료
        pids_to_terminate = [current_pid] + get_child_pids(current_pid)
        for pid in pids_to_terminate:
            subprocess.run(['kill', '-9', str(pid)], check=True)
            logger.info(f'Process with PID {pid} terminated successfully.')

        current_pid = None
        return jsonify({'message': 'Process terminated successfully.'})
    except subprocess.CalledProcessError as e:
        logger.error(f'An error occurred while terminating the process: {e}')
        return jsonify({'message': 'An error occurred while terminating the process', 'error': str(e)}), 500


    

@app.route('/download_file/<filename>', methods=['GET'])
def download_file(filename):
    current_time = app.config.get('CURRENT_TIME', 'No current time set')
    
    # 파일 경로 설정
    file_path = os.path.join(f'/home/clark/workspace/muzic/musecoco/2-attribute2music_model/generation/{current_time}/linear_mask-1billion-attribute2music/infer_test/topk15-t1.0-ngram0/0/midi', filename)
    
    # 파일을 클라이언트에 전송
    return send_file(file_path, as_attachment=True)  

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005)
