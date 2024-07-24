#!/bin/bash

# 아래의 파일들에 존재하는 특정 변수를 수정합니다.
# "./1-text2attribute_model/predict.sh"
# "./1-text2attribute_model/stage2_pre.py"
# "./2-attribute2music_model/interactive_1billion.sh"
# "./2-attribute2music_model/remi2midi.py"
# "./ghostBand_flask/app.py"
# "./ghostBand_req_test/test_music_gen_req.py"
# "./ghostBand_req_test/test_process_stop_req.py"

# 수정할 변수
PATH_VARIABLE_NAME="project_path"
# ghostBand_ai_composition 디렉토리의 절대 경로를 입력하세요
NEW_PATH="/home/UserName/ghostBand_ai_composition"

# 수정할 변수
SERVER_URL_VARIABLE_NAME="server_ip"
# 플라스크 서버를 실행할 PC의 URL을 입력하세요
SERVER_URL="127.0.0.1:5000"

# 수정할 파일 목록
FILES=(
  "./1-text2attribute_model/predict.sh"
  "./1-text2attribute_model/stage2_pre.py"
  "./2-attribute2music_model/interactive_1billion.sh"
  "./2-attribute2music_model/remi2midi.py"
  "./ghostBand_flask/app.py"
)

# 파일을 순회하며 project_path 수정
for FILE in "${FILES[@]}"; do
  if [[ $FILE == *.py ]]; then
    sed -i "s|^\($PATH_VARIABLE_NAME *= *\).*|\1'$NEW_PATH'|" "$FILE"
  elif [[ $FILE == *.sh ]]; then
    sed -i "s|^\($PATH_VARIABLE_NAME *= *\).*|\1\"$NEW_PATH\"|" "$FILE"
  else
    echo "지원하지 않는 파일 형식: $FILE"
  fi
done

# server_ip 수정
sed -i "s|^\($SERVER_URL_VARIABLE_NAME *= *\).*|\1'$SERVER_URL'|" "./ghostBand_flask/app.py"
sed -i "s|^\($SERVER_URL_VARIABLE_NAME *= *\).*|\1'$SERVER_URL'|" "./ghostBand_req_test/test_music_gen_req.py"
sed -i "s|^\($SERVER_URL_VARIABLE_NAME *= *\).*|\1'$SERVER_URL'|" "./ghostBand_req_test/test_process_stop_req.py"

echo "변수 project_path 수정 완료: $PATH_VARIABLE_NAME = $NEW_PATH"
echo "변수 server_ip 수정 완료: $SERVER_URL_VARIABLE_NAME = $SERVER_URL"
echo "./ghostBand_flask/app.py의 최하단에 존재하는 진입점 코드블럭의 app.run() 매개변수 port도 수정해주세요"
