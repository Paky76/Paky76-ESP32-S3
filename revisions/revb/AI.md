# Paky76 Rev.B · Modelli configurabili

## Tre modalità

| Modalità | Esecuzione | Disponibilità |
|---|---|---|
| Provider online | Gateway su PC/server, con OpenAI Responses, Anthropic Messages oppure DeepSeek Chat Completions | Adattatori implementati e verificati con risposte simulate. Servono chiavi e un modello abilitato per prove reali. |
| Modello interno | Gateway su rete fidata, verso un endpoint compatibile OpenAI come Ollama | Adattatore implementato. Il modello gira sull'host locale. |
| Base senza Internet | Firmware ESP32-S3, risposte testuali a pochi comandi | Accessibile dalla dashboard USB o Wi-Fi locale. Il firmware non richiede un modello generativo per questi comandi. |

La dashboard prova la modalità base sul dispositivo. Il gateway espone un'unica API testuale su loopback. Il collegamento autonomo dispositivo → gateway via HTTPS, l'uscita vocale, l'eventuale ingresso microfono e LTE end-to-end devono ancora essere integrati e collaudati. Nessuna scelta automatica inoltra prompt dal modello interno ai provider online.

## Prova del gateway

Da questa directory, impostare con un gestore di segreti o con variabili d'ambiente:

- `PAKY_AI_PROVIDER` su `openai`, `anthropic`, `deepseek`, `local` oppure `basic`.
- `PAKY_AI_MODEL` sul nome effettivo del modello, obbligatorio salvo in modalità base.
- `PAKY_UPSTREAM_KEY` per i servizi esterni. Resta sul server. Per una rete interna con autenticazione, usare un endpoint HTTPS.
- `PAKY_LOCAL_URL` per il server interno, per esempio `http://127.0.0.1:11434/v1/chat/completions` quando Ollama gira sullo stesso host.

Avviare con `python3 ai/gateway.py`. Il server ascolta su `127.0.0.1:8766` e richiede `PAKY_GATEWAY_TOKEN` di almeno 24 caratteri. Inviare a `POST /v1/ask` un JSON come `{"prompt":"Ciao"}` con header `Authorization: Bearer <token>`. La risposta contiene testo, provider e modello. Per raggiungerlo dalla scocca prevista, completare un accesso HTTPS autenticato con certificato verificato dal firmware. Le chiavi dei provider non vanno nella dashboard, nei sorgenti o sul dispositivo.

## CPU e memoria

La base funziona con l'ESP32-S3-WROOM-1-N8 attuale. Per futuri modelli compatti di riconoscimento comandi o parole chiave, valutare **ESP32-S3-WROOM-1-N16R8**, con 16 MB flash e 8 MB PSRAM. Validare mappa dei pin riservati, avvio, firmware, partizioni, memoria di picco, prestazioni e disponibilità prima di aggiornare la BOM. Un modello generativo locale richiede un host più adatto, per esempio il server Ollama già presente in rete. L'aumento di flash da solo non fornisce RAM di inferenza o prestazioni sufficienti.

- [OpenAI Responses API](https://platform.openai.com/docs/api-reference/responses/create)
- [Anthropic Messages API](https://docs.anthropic.com/en/api/messages)
- [DeepSeek Chat Completions](https://api-docs.deepseek.com/api/create-chat-completion)
- [Ollama compatibilità OpenAI](https://docs.ollama.com/api/openai-compatibility)
- [Espressif ESP32-S3-WROOM-1](https://www.espressif.com/sites/default/files/documentation/esp32-s3-wroom-1_wroom-1u_datasheet_en.pdf)
