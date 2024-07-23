import json

def create_music_description(instruments, genre, time_signature, playtime, bars, pitch_range, key, tempo):
    # 샘플 텍스트 템플릿
    template = ("[악기들], [박자], [재생 시간], [마디 수], [음역], [조성], [템포], [장르].")
    
    # 악기 리스트를 문장에 맞게 변환
    selected_instruments = ', '.join(instruments[:-1]) + ', and ' + instruments[-1] if len(instruments) > 1 else instruments[0]
    
    # 템플릿에 사용자 입력 값을 삽입
    description = template.replace("[악기들]", selected_instruments)
    description = description.replace("[설명]", "unique")  # 'unique'는 예시 설명
    description = description.replace("[박자]", time_signature)
    description = description.replace("[재생 시간]", str(playtime))
    description = description.replace("[마디 수]", str(bars))
    description = description.replace("[음역]", str(pitch_range))
    description = description.replace("[조성]", key)
    description = description.replace("[템포]", tempo)
    description = description.replace("[장르]", genre)

    # 결과를 딕셔너리 형태로 변환
    result = [{"text": description}]

    # 결과를 JSON 파일로 저장
    with open("./data/music_description.json", "w", encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False)

# 사용자 입력 예시
available_instruments = ["guitar", "piano", "bass", "drum", "keyboard", "sax"]
selected_instruments = ["piano","guitar", "bass", "drum"]
available_genre = ["new_age", "electronic", "rap", "religious", "international", "easy listening", "avant-garde", "RnB", "Latin", "children", "jazz", "classical", "comedy", "pop", "reggae", "stage", "folk", "blues", "vocal", "holiday", "country", "symphony"]
genre = "pop"
time_signature = "3/4"
playtime = 80
bars = 16
pitch_range = 4
key = "D major"
tempo = "moderate"

# 함수 호출
create_music_description(selected_instruments, genre, time_signature, playtime, bars, pitch_range, key, tempo)

