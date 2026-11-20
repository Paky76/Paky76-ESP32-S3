#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")"
if [[ "$(uname -m)" != aarch64 ]]; then
  echo 'Usa Raspberry Pi OS a 64 bit su Raspberry Pi.' >&2
  exit 1
fi
sudo apt-get update
sudo apt-get install -y alsa-utils build-essential ca-certificates cmake curl git python3-venv
mkdir -p runtime models
for project in whisper.cpp llama.cpp; do
  if [[ ! -d "runtime/$project/.git" ]]; then
    git clone --depth 1 "https://github.com/ggml-org/$project.git" "runtime/$project"
  fi
done
cmake -S runtime/whisper.cpp -B runtime/whisper.cpp/build -DCMAKE_BUILD_TYPE=Release
cmake --build runtime/whisper.cpp/build --target whisper-cli -j2
cmake -S runtime/llama.cpp -B runtime/llama.cpp/build -DCMAKE_BUILD_TYPE=Release -DLLAMA_CURL=OFF
cmake --build runtime/llama.cpp/build --target llama-server -j2
python3 -m venv runtime/piper
runtime/piper/bin/python -m pip install piper-tts
download() {
  local name="$1" url="$2"
  if [[ ! -s "models/$name" ]]; then
    curl --fail --location --retry 3 --output "models/$name.part" "$url"
    mv "models/$name.part" "models/$name"
  fi
}
download ggml-base.bin https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-base.bin
download qwen2.5-0.5b-instruct-q4_k_m.gguf https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct-GGUF/resolve/main/qwen2.5-0.5b-instruct-q4_k_m.gguf
voice=https://huggingface.co/rhasspy/piper-voices/resolve/main/it/it_IT/paola/medium
download it_IT-paola-medium.onnx "$voice/it_IT-paola-medium.onnx"
download it_IT-paola-medium.onnx.json "$voice/it_IT-paola-medium.onnx.json"
printf '%s\n' 'Installazione conclusa. Avvia ./avvia-modello.sh e usa python3 paky76.py in un altro terminale.'
