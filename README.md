# 단컴한 인생: Ghost Band - AI 작곡

## 업데이트
[2024. 07. 25.] 악기 소리 뮤트, 악보 추출 기능에 관한 코드가 `spleeter` 디렉토리에 추가 되었습니다.
- 해당 기능에 대한 설명은 추후에 업데이트 될 예정입니다.
- 해당 기능을 실행하기 위한 모델 파일은 현재 레포지토리에 저장되어있지 않으며 기능 실행 시 자동으로 설치됩니다.

## 목차
- [단컴한 인생: Ghost Band - AI 작곡](#단컴한-인생-ghost-band---ai-작곡)
  - [업데이트](#업데이트)
  - [목차](#목차)
  - [개요](#개요)
  - [주의사항](#주의사항)
  - [실행 가이드](#실행-가이드)
  - [출처 및 라이센스](#출처-및-라이센스)
  - [연락처](#연락처)
- [Ghost Band - 악보 추출, 악기 소리 뮤트](#ghost-band---악보-추출-악기-소리-뮤트)
  - [연락처](#연락처-1)


## 개요
본 프로젝트는 [SW중심대학 디지털 경진대회_SW와 생성AI의 만남 : SW 부문]에 참여하는 팀인 "단컴한 인생"의 프로젝트 Ghost Band의 주요 기능인 AI 작곡 기능을 MuseCoco(Generation Symbolic Music from Text) 모델과 Flask를 사용하여 구현한 프로젝트입니다.  
  
AI 작곡 기능의 파이프라인은 다음과 같습니다.

- 1-Stage: Text-to-Attribute Predict
  - Flutter로 구현된 모바일 앱을 통해 사용자로부터 음악 작곡을 위한 Attribute를 HTTP로 전달받습니다.
  - 해당 Attribute를 기반으로 생성되는 음악의 다양성을 위해 사용 가능한 아티스트 중 한명을 포함시켜 Text 형태로 변환합니다.  
  - 변환된 Text를 BERT 모델을 통하여 사용된 Attribute를 예측하고 Attribute2muic generation 단계에 사용되는 입력 파일 형태로 변환합니다.  

- 2-Stage: Attribute-to-Music Generation
  - 입력 파일과 Attribute2music 모델을 통해 음악을 REMI 파일의 생성하고, 이를 통해 MIDI 파일로 변환합니다.
  - MIDI 파일을 오픈소스로 공개된 악보제작 프로그램인 MuseScore3를 사용하여 악보로 변환합니다.
  - 이후 모바일 앱에서 다운로드 요청이 오면 생성된 MIDI 파일과 악보를 HTTP를 통해 전달합니다.




## 주의사항
본 프로젝트는 Ubuntu 20.04.6 LTS version에서 구현되고 테스트하였으므로 이외의 운영체제에서 원할히 실행되지 않을 수 있음을 알려드립니다.

이 레포지토리에는 GhostBand의 프론트엔드는 포함되어 있지 않습니다.  
- 만약 요청 테스트를 하고자 한다면 `ghostBand_ai_composition/ghostBand_req_test` 폴더를 확인하세요.  

2-Stage에서 사용되는 모델은 아래의 파일에서 링크를 확인하고 직접 설치해야 합니다.
- `ghostBand_ai_composition/2-attribute2music_model/checkpoints/linear_mask-1billion/README.md`
- 만약 설치가 안된다면 아래의 링크에서 checkpoint를 확인하여 주세요.
- [원본 Github 링크](https://github.com/microsoft/muzic/tree/main/musecoco#ii-attribute-to-music-generation-1)



## 실행 가이드
만약 본 프로젝트를 직접 실행하고자 한다면 아래의 가이드라인을 참고하여 진행해주세요.  

1. 환경 설정 ([출처](https://github.com/microsoft/muzic/tree/main/musecoco))
    ```
    conda create -n MuseCoco python=3.8
    conda activate MuseCoco
    conda install pytorch=1.11.0 -c pytorch
    pip install -r requirements.txt  # g++ should be installed to let this line work.
    ```

2. Flask 설치
    ```
    # Flask 설치
    pip install flask
    # 설치 확인
    python -m flask --version
    ```
3. 실행 파일 수정   
  Flask를 통해 MuseCoco 모델을 실행하기 위해선 몇가지 파일의 변수를 수정해야합니다.  
  먼저 `ghostBand_ai_composition/path_setting.sh` 파일에서 변수 `NEW_PATH`와 `SERVER_URL`을 수정하고 실행해주세요.
     ```
     # 변수 NEW_PATH, SERVER_URL 수정 후 실행
     bash path_setting.sh
     ```
    이때 입력한 `SERVER_URL`의 포트번호를 `ghostBand_ai_composition/ghostBand_flask/app.py`의 진입점 코드블럭 내 app.run()에 동일한 포트번호를 입력해야 합니다.

4. app.py 실행  
    `ghostBand_ai_composition/ghostBand_flask` 경로에서 Flask 앱을 실행합니다.
    ```
    #Flask 앱 실행
    python app.py
    ```
5. 음악 생성 Request 전송  
    실행한 Flask 앱으로 음악 생성 Request를 보내기 위해 `ghostBand_ai_composition/ghostBand_req_test` 경로에서 다음과 같이 파일을 실행합니다. 
    ```
    python test_music_gen_req.py
    ```
    생성이 끝나면 MIDI 파일과 악보를 다운받으며 필요 시 스크립트를 수정하여 사용해주세요.  
    
    만약 생성 도중 중지 요청을 보내려면 동일한 경로에서 다음과 같이 스크립트를 실행해주세요.
    ```
    python test_process_stop_req.py
    ```




## 출처 및 라이센스
이 프로젝트에서 사용하는 생성 모델인 MuseCoco는 Microsoft Research Asia의 일부 연구원들과 외부 협력자들에 의해 시작된 AI 음악 연구 프로젝트인 Muzic의 하위 프로젝트입니다.   
MuseCoco 모델을 사용하기 위해 Github에서 Muzic 레포지토리를 복제하였으며, MuseCoco 프로젝트를 수정하여 Ghost Band 프로젝트의 AI 작곡 기능을 구현하였습니다.  
Muzic는 MIT License를 따르는 오픈소스 프로젝트이며 원본 레포지토리의 출처는 다음과 같습니다.

- [Muzic Github] https://github.com/microsoft/muzic
- [MuseCoco Github] https://github.com/microsoft/muzic/tree/main/musecoco

악보 변환 기능에 사용되는 MuseScore는 Werner Schweer가 제작한 악보 제작 프로그램으로 GPL version 3.0 License를 따르는 오픈소스 프로젝트입니다.  
MuseScore3 3.2.3 버전을 사용하였으며 원본 레포지토리의 출처는 다음과 같습니다.

- [MuseScore Github] https://github.com/musescore/MuseScore

## 연락처
기타 문의사항이 있다면 아래의 E-mail을 통해 연락해주세요.  
- 작성자: 이철민  
- E-mail: jongha1257@gmail.com

# Ghost Band - 악보 추출, 악기 소리 뮤트

추후 작성 예정

## 연락처
- 작성자: 이재영
