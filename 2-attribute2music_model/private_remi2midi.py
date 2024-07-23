import os
import sys
from midiprocessor import MidiDecoder, MidiEncoder


def get_larger_file(directory):
    # 파일 경로 생성
    file1 = os.path.join(directory, '0.txt')
    file2 = os.path.join(directory, '1.txt')
    
    # 두 파일의 존재 여부 확인
    if not os.path.isfile(file1) or not os.path.isfile(file2):
        raise ValueError("디렉토리에 '0.txt'와 '1.txt' 파일이 있어야 합니다.")
    
    # 각 파일의 크기 가져오기
    size1 = os.path.getsize(file1)
    size2 = os.path.getsize(file2)

    # 더 큰 파일 이름 반환
    if size1 > size2:
        larger_file = "0.txt"
    else:
        larger_file = "1.txt"

    return larger_file



# 명령줄 인수로 받은 current_time 값
if len(sys.argv) < 2:
    print("Usage: python remi2midi.py <current_time>")
    sys.exit(1)

date = sys.argv[1]
midi_root = f"/home/clark/workspace/muzic/ghostBand_ai_composition/2-attribute2music_model/generation/{date}/linear_mask-1billion-attribute2music/infer_test/topk15-t1.0-ngram0"
midi_decoder = MidiDecoder("REMIGEN2")

print(midi_decoder)

new_midi_name = f"{date}.mid"
# new_midi_name = f"{current_time}.mid"

midi_list = []
error_midi_list = []

#remi_file = get_larger_file(midi_root)

for folder_name in os.listdir(midi_root):
    folder_dir = os.path.join(midi_root, folder_name)
    # not folder, Using_pred_labels.txt etc
    if os.path.isfile(folder_dir):
        continue
        
    # remi_name: 0.txt, 1.txt...
    remi_dir = os.path.join(folder_dir, 'remi')
    midi_dir = os.path.join(folder_dir, 'midi')

    remi_file = get_larger_file(remi_dir)


    for remi_name in os.listdir(remi_dir):
        if remi_name == remi_file:
            with open(os.path.join(remi_dir, remi_name), 'r') as f:
                hypo_str = f.read()
            
            # since the seq looks like this: prefix <seq> remi
            # we have to get the remi tokens by discard the prefix tokens and <seq>
            # orginal:
            # remi_token = hypo_str.split(" ")[sep_pos[id_] + 1:]
            remi_token = hypo_str.split(" <sep> ")[1].split(" ")
            os.makedirs(midi_dir, exist_ok=True)
            # midi_save_path = os.path.join(midi_dir, remi_name.replace('.txt', '.mid'))
            midi_save_path = os.path.join(midi_dir, new_midi_name)
            midi_list.append(midi_save_path)
            try:
                midi_obj = midi_decoder.decode_from_token_str_list(remi_token)
                midi_obj.dump(midi_save_path)
            except:
                error_midi_list.append(midi_save_path)



print(len(midi_list))

print(len(error_midi_list))

