#!/usr/bin/env python3
"""Assistente italiano con registrazione a richiesta e inferenza locale."""

import argparse
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import urllib.request

ROOT = Path(__file__).resolve().parent
SYSTEM_PROMPT = (
    "Sei Paky76, un assistente vocale offline. Rispondi in italiano, "
    "in massimo due frasi chiare, senza Markdown. Se non sai una cosa, dillo."
)


def run(command, timeout):
    try:
        subprocess.run(command, check=True, timeout=timeout, stdout=subprocess.DEVNULL)
    except subprocess.CalledProcessError as error:
        raise RuntimeError(f"{command[0]} ha restituito {error.returncode}") from error
    except subprocess.TimeoutExpired as error:
        raise RuntimeError(f"{command[0]} ha superato {timeout} secondi") from error


def transcribe(config, wav, directory):
    output = directory / "trascrizione"
    run([config.whisper, "-m", str(config.asr_model), "-f", str(wav),
         "-l", "it", "-nt", "-otxt", "-of", str(output), "-t", "3"], 120)
    return output.with_suffix(".txt").read_text(encoding="utf-8").strip()


def answer(config, history, question):
    messages = [{"role": "system", "content": SYSTEM_PROMPT}, *history,
                {"role": "user", "content": question}]
    body = json.dumps({"messages": messages, "max_tokens": 128,
                       "temperature": 0.45, "stream": False}).encode()
    request = urllib.request.Request(
        f"http://127.0.0.1:{config.port}/v1/chat/completions",
        data=body, headers={"Content-Type": "application/json"})
    # Avoid system proxies, including when the device is offline.
    with urllib.request.build_opener(urllib.request.ProxyHandler({})).open(
        request, timeout=180
    ) as response:
        result = json.load(response)
    try:
        content = result["choices"][0]["message"]["content"].strip()
    except (KeyError, IndexError, AttributeError, TypeError) as error:
        raise RuntimeError("llama-server ha restituito una risposta inattesa") from error
    if not content:
        raise RuntimeError("Il modello ha restituito una risposta vuota")
    return content


def speak(config, text, output):
    run([config.piper_python, "-m", "piper", "-m", str(config.voice),
         "-f", str(output), "--", text], 90)
    run([config.aplay, "-q", "-D", config.output_device, str(output)], 120)


def prepare(config):
    files = []
    if config.text is None:
        files.append(config.asr_model)
    if not config.silent:
        files.extend([config.voice, config.voice.with_suffix(".onnx.json")])
    for file in files:
        if not file.is_file():
            raise RuntimeError(f"Modello mancante: {file}. Esegui installa.sh.")


def handle_turn(config, history, directory):
    started = time.monotonic()
    if config.text is not None:
        question = config.text.strip()
    else:
        wav = directory / "input.wav"
        if config.wav:
            wav = config.wav
        else:
            print(f"Parla ora ({config.seconds} secondi).", flush=True)
            run([config.arecord, "-q", "-D", config.input_device, "-t", "wav",
                 "-f", "S16_LE", "-r", "16000", "-c", "1",
                 "-d", str(config.seconds), str(wav)], config.seconds + 10)
            started = time.monotonic()
        question = transcribe(config, wav, directory)
    if not question or question.startswith("[") and question.endswith("]"):
        print("Nessun parlato riconosciuto.", flush=True)
        return
    question = question[:1000]
    print(f"Tu: {question}", flush=True)
    reply = answer(config, history, question)
    print(f"Paky76: {reply}", flush=True)
    print(f"Tempo fino alla risposta scritta: {time.monotonic() - started:.1f} s")
    if not config.silent:
        speak(config, reply, directory / "risposta.wav")
    history.extend([{"role": "user", "content": question},
                    {"role": "assistant", "content": reply}])
    del history[:-4]


def arguments():
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--text", help="Invia una domanda senza microfono")
    modes.add_argument("--wav", type=Path, help="Trascrive un WAV PCM mono a 16 kHz")
    parser.add_argument("--once", action="store_true", help="Registra subito e termina")
    parser.add_argument("--silent", action="store_true", help="Mostra soltanto il testo")
    parser.add_argument("--seconds", type=int, choices=range(2, 31), default=6, metavar="2-30")
    parser.add_argument("--port", type=int, default=8080)
    parser.add_argument("--input-device", default="default")
    parser.add_argument("--output-device", default="default")
    parser.add_argument("--arecord", default="arecord")
    parser.add_argument("--aplay", default="aplay")
    parser.add_argument("--whisper", default=str(ROOT / "runtime/whisper.cpp/build/bin/whisper-cli"))
    parser.add_argument("--piper-python", default=str(ROOT / "runtime/piper/bin/python"))
    parser.add_argument("--asr-model", type=Path, default=ROOT / "models/ggml-base.bin")
    parser.add_argument("--voice", type=Path, default=ROOT / "models/it_IT-paola-medium.onnx")
    return parser.parse_args()


def main():
    config = arguments()
    try:
        prepare(config)
        history = []
        if config.once or config.text is not None or config.wav:
            with tempfile.TemporaryDirectory(prefix="paky76-") as directory:
                handle_turn(config, history, Path(directory))
            return 0

        print("Paky76 pronto. Invio per parlare, q per uscire.")
        while input("> ").strip().lower() != "q":
            try:
                with tempfile.TemporaryDirectory(prefix="paky76-") as directory:
                    handle_turn(config, history, Path(directory))
            except (OSError, RuntimeError, ValueError) as error:
                print(f"Errore nel turno: {error}", file=sys.stderr)
        return 0
    except (KeyboardInterrupt, EOFError):
        return 0
    except (OSError, RuntimeError, ValueError) as error:
        print(f"Errore: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
