#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")"
server=runtime/llama.cpp/build/bin/llama-server
model=models/qwen2.5-0.5b-instruct-q4_k_m.gguf
if [[ ! -x "$server" || ! -s "$model" ]]; then
  echo 'Esegui prima bash installa.sh.' >&2
  exit 1
fi
exec "$server" --model "$model" --host 127.0.0.1 --port "${PAKY76_PORT:-8080}" --ctx-size 2048 --threads 3 --parallel 1
