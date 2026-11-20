# Paky76 Pi — Prototipo vocale italiano offline

Il programma registra una domanda di durata configurabile quando premi Invio, la trascrive con Whisper, passa il testo a Qwen2.5 0.5B locale e riproduce la risposta con Piper (voce Paola). Dopo aver installato dipendenze e modelli, il programma parla soltanto con il server sul loopback 127.0.0.1. Il contesto conserva due scambi nella RAM; registrazioni e file vocali temporanei vengono rimossi al termine di ogni turno gestito.

## Banco prova

- Raspberry Pi Compute Module 4 da 8 GB **Lite**, scheda IO Board ufficiale, alimentatore compatibile con la carrier e microSD con Raspberry Pi OS a 64 bit. Puoi usare anche un Raspberry Pi 4 o 5 da 8 GB se già disponibile, con il suo alimentatore e Raspberry Pi OS 64 bit.
- Un dispositivo audio USB con microfono e uscita cuffie o altoparlante. Tastiera e monitor oppure un terminale SSH. Per la prima prova usa cuffie o un altoparlante a volume moderato.
- Per questo banco prova avvii l'ascolto da terminale. Display, pulsantiera Rev.H e scocca richiedono l'integrazione successiva con una carrier dedicata.

## Installazione e avvio

Nel terminale del Pi, dalla directory che contiene i file:

```bash
bash installa.sh
bash avvia-modello.sh
```

L'installazione richiede internet e scarica i modelli. Lascia il server in esecuzione. Da un secondo terminale prova prima una domanda testuale:

```bash
python3 paky76.py --text "Spiegami in una frase come funziona un orologio." --silent
```

Poi esegui la prova vocale:

```bash
python3 paky76.py
```

Premi Invio per parlare e poi aspetta la risposta. Per terminare, digita q. Se serve specificare la scheda audio, individua i nomi con `arecord -L` e `aplay -L`. Esempio:

```bash
python3 paky76.py --input-device plughw:CARD=Device,DEV=0 --output-device plughw:CARD=Device,DEV=0
```

Adatta CARD e DEV alla tua periferica. Puoi passare un WAV mono PCM 16 bit a 16 kHz con `--wav domanda.wav` e usare `--seconds 10` per domande più lunghe. Per modificare la porta del modello, impostala con `PAKY76_PORT` per il server e `--port` per il client.

## Collaudo

1. Controlla che la domanda testuale produca una risposta in italiano.
2. Registra frasi in italiano a distanza normale e verifica trascrizione, pertinenza della risposta e intelligibilità della voce.
3. Dopo l'installazione scollega la rete e ripeti la prova dalla console locale. Verifica il tempo dalla fine della registrazione alla risposta scritta e misura separatamente il tempo fino al primo audio.
4. Annota modello, tempi e memoria di picco sul Pi prima di scegliere dissipazione e dimensioni della nuova carrier.

La catena software è provata nel workspace con sostituti di microfono, Whisper, llama-server, Piper e riproduzione. Installazione ARM64, inferenza con i modelli reali e audio sul banco restano da verificare sul Pi. La conversazione con il modello 0.5B è un primo riferimento per misurare qualità e latenza.

[Whisper.cpp](https://github.com/ggml-org/whisper.cpp) · [llama.cpp](https://github.com/ggml-org/llama.cpp) · [Modello Qwen GGUF](https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct-GGUF) · [Piper CLI](https://github.com/OHF-Voice/piper1-gpl/blob/main/docs/CLI.md) · [Voce Paola](https://huggingface.co/rhasspy/piper-voices/tree/main/it/it_IT/paola/medium) · [CM4 IO Board](https://www.raspberrypi.com/products/compute-module-4-io-board/)
