# [ghostBand_ai_composition 프로젝트의 절대경로]/1-text2attribute_model
#cd /home/clark/workspace/muzic/ghostBand_ai_composition/1-text2attribute_model

python main.py \
    --do_predict \
    --model_name_or_path=IreneXu/MuseCoco_text2attribute \
    --test_file=data/music_description.json \
    --attributes=data/att_key.json \
    --num_labels=num_labels.json \
    --output_dir=./tmp \
    --overwrite_output_dir
