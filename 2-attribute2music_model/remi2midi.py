import os
import sys
from midiprocessor import MidiDecoder, MidiEncoder


# 명령줄 인수로 받은 current_time 값
if len(sys.argv) < 2:
    print("Usage: python remi2midi.py <current_time>")
    sys.exit(1)

date = sys.argv[1]

# ghostBand_ai_composition 프로젝트 디렉토리의 절대경로를 입력하세요
project_path = '/home/UserName/ghostBand_ai_composition'

midi_root = f"{project_path}/2-attribute2music_model/generation/{date}/linear_mask-1billion-attribute2music/infer_test/topk15-t1.0-ngram0"
midi_decoder = MidiDecoder("REMIGEN2")

print(midi_decoder)

new_midi_name = f"{date}.mid"
# new_midi_name = f"{current_time}.mid"

midi_list = []
error_midi_list = []

for folder_name in os.listdir(midi_root):
    folder_dir = os.path.join(midi_root, folder_name)
    # not folder, Using_pred_labels.txt etc
    if os.path.isfile(folder_dir):
        continue
        
    # remi_name: 0.txt, 1.txt...
    remi_dir = os.path.join(folder_dir, 'remi')
    midi_dir = os.path.join(folder_dir, 'midi')


    for remi_name in os.listdir(remi_dir):
        if remi_name == "0.txt":
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


