# 단컴한 인생: Ghost Band - AI 작곡

본 프로젝트는 [SW중심대학 디지털 경진대회_SW와 생성AI의 만남 : SW 부문]에 참여하는 팀인 "단컴한 인생"의 프로젝트 Ghost Band의 주요 기능인 AI 작곡 기능을 Flask로 구현한 프로젝트입니다.  
  
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
이 레포지토리에는 GhostBand의 AI 작곡 기능만 포함되어 있습니다.  
Flutter로 구현된 모바일앱과 나머지 기능은 다음 레포지토리를 참고하시기 바랍니다.

## 출처 및 라이센스
이 프로젝트에서 사용하는 생성 모델인 MuseCoco는 Microsoft Research Asia의 일부 연구원들과 외부 협력자들에 의해 시작된 AI 음악 연구 프로젝트인 Muzic의 하위 프로젝트입니다.   
MuseCoco 모델을 사용하기 위해 Github에서 Muzic 레포지토리를 복제하였으며, 이 프로젝트를 수정하여 Ghost Band 프로젝트의 AI 작곡 기능을 구현하였습니다.  
Muzic는 MIT License를 따르는 오픈소스 프로젝트이며 원본 레포지토리의 출처는 다음과 같습니다.

- [Muzic Github] https://github.com/microsoft/muzic
- [MuseCoco Github] https://github.com/microsoft/muzic/tree/main/musecoco

악보 변환 기능에 사용되는 MuseScore는 Werner Schweer가 제작한 악보 제작 프로그램으로 GPL version 3.0 License를 따르는 오픈소스 프로젝트입니다.  
MuseScore3 3.2.3 버전을 사용하였으며 원본 레포지토리의 출처는 다음과 같습니다.

- [MuseScore Github] https://github.com/musescore/MuseScore

---
작성자: 이철민  
E-mail: jongha1257@gmail.com
