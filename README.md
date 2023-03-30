# SMART: a Spoken Media Automatic Reconstruction Tool
## 배경
- 인간이 일상 속에서 다른 이들과 정보를 공유하기 위해 가장 많이 사용하는 수단은 바로 대화입니다. 대화는 가장 자연스러운 의사소통 수단이면서, 매우 쉽게 자신만의 언어로 정보를 전달할 수 있지만, 중요하고 복잡한 내용이나 매우 많은 양의 정보를 다룰 때에는 여러 가지 문제점이 존재합니다.
- 각 발화는 일시적이며 한번 끝나면 따로 녹취를 하지 않는 한 다시 들을 방법이 없습니다. 또한 똑같은 내용을 여러 사람에게 반복적으로 전달하기 위해 같은 말을 반복하는 것은 매우 피곤한 일입니다.
- 이러한 대화 내용을 나중에도 참고하기 좋은 형태로 정리하려면, 녹취록을 작성하거나 핵심 내용만 정리하는 등의 귀찮은 작업이 필요합니다.
- 이 레포지토리에서는 인간이 입으로 내뱉은 모든 형태의 대화 정보를 실시간으로 입력 받아, STT를 거쳐 자동으로 텍스트로 변환하고, 이에 그치지 않고 다른 언어로 번역하거나 핵심 내용 위주로 요약문을 작성하는 등 대화 내용을 이해하는데 도움이 되는 다양한 정보들을 생성해주는 프로그램인 SMART(Spoken Media Automatic Reconstruction Tool)를 개발하고자 합니다.

## 주요 기능 및 UI

![HCI-이성진-SMART](https://user-images.githubusercontent.com/44901828/228768201-2841fce4-db73-44ed-9909-8689ea95f749.png)

- 프로그램을 실행하고 시작 버튼을 누르면, 현재 진행중인 대화가 마이크로 녹음되고 일정 시간 주기로 텍스트로 변환됩니다.
- 변환된 텍스트는 대화가 지속되는 한 계속 누적되는데, 특정 글자수 기준으로 자동으로 단락이 나누어집니다.
- 새로운 단락이 생성되면, 자동으로 해당 단락의 내용을 바탕으로 번역이나 요약, 중요 키워드 추출 등의 작업을 수행한 결과를 출력해 줍니다.
- 이를 바탕으로, 현재 진행중인 발화를 듣는 청자들이 이해하는데 도움이 되고, 외국어 발화를 듣는 중이거나 중간 흐름을 놓친 경우에도 쉽게 따라갈 수 있습니다.

## 기반 기술
- 실시간으로 녹음된 발화를 텍스트로 저장하기 위해 OpenAI에서 공개한 Whisper Large 모델을 사용합니다. Whisper는 open-source STT 모델로, 다양한 언어를 인식하여 transcribing을 진행하고 이를 다른 언어로 번역할 수 있는 기능을 갖추고 있습니다.
- Real-time speech recognition 방식은 https://github.com/davabase/whisper_real_time 레포지토리를 기반으로 개발을 진행했습니다.
- 번역을 위해 Papago API를, 요약 기능을 위해 summarization task에 튜닝된 모델을 자체적으로 서빙하여 사용했습니다.

## 기대효과
- 단순히 프로그램을 실행하고 대화하는 것 만으로도, 대화 내용을 놓치지 않도록 구조적으로 정리된 정보를 실시간으로 생성하여 보여줄 수 있습니다. 예를 들면 외국어로 진행하는 강의를 듣거나 긴 대화 내용 도중 흐름을 놓쳤을 때, 실시간으로 생성해주는 정보를 바탕으로 잘 따라갈 수 있을 것입니다.

<br>

Original repository info

---


# Real Time Whisper Transcription

![Demo gif](demo.gif)

This is a demo of real time speech to text with OpenAI's Whisper model. It works by constantly recording audio in a thread and concatenating the raw bytes over multiple recordings.

To install dependencies simply run
```
pip install -r requirements.txt
```
in an environment of your choosing.

Whisper also requires the command-line tool [`ffmpeg`](https://ffmpeg.org/) to be installed on your system, which is available from most package managers:

```
# on Ubuntu or Debian
sudo apt update && sudo apt install ffmpeg

# on Arch Linux
sudo pacman -S ffmpeg

# on MacOS using Homebrew (https://brew.sh/)
brew install ffmpeg

# on Windows using Chocolatey (https://chocolatey.org/)
choco install ffmpeg

# on Windows using Scoop (https://scoop.sh/)
scoop install ffmpeg
```

For more information on Whisper please see https://github.com/openai/whisper

The code in this repository is public domain.