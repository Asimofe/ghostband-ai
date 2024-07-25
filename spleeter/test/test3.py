import subprocess

# MusicXML 파일을 PDF로 변환합니다.
for i in range(len(parts.parts)):
    subprocess.run(["musescore", f"path/to/your/instrument_{i}.xml", "-o", f"path/to/your/instrument_{i}.pdf"])

