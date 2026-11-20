# Paky76 Rev.B · Modelli configurabili

## Tre modalità

| Modalità | Esecuzione | Disponibilità |
|---|---|---|
| Provider online | Gateway su PC/server, con OpenAI Responses, Anthropic Messages oppure DeepSeek Chat Completions | Adattatori implementati e verificati con risposte simulate. Servono chiavi e un modello abilitato per prove reali. |
| Modello interno | Gateway su rete fidata, verso un endpoint compatibile OpenAI come Ollama | Adattatore implementato. Il modello gira sull'host locale. |
| Base senza Internet | Firmware ESP32-S3, risposte testuali a pochi comandi | Accessibile dalla dashboard USB o Wi-Fi locale. Il firmware non richiede un modello generativo per questi comandi. |

La dashboard può inviare al firmware sia comandi base sia richieste al gateway. La Paky76 effettua direttamente la richiesta HTTPS quando è collegata al Wi-Fi e configurata. L'uscita vocale delle risposte, l'eventuale ingresso microfono e LTE end-to-end restano da integrare e collaudare. Nessuna scelta automatica inoltra prompt dal modello interno ai provider online.

## Prova del gateway

Da questa directory, impostare con un gestore di segreti o con variabili d'ambiente:

- `PAKY_AI_PROVIDER` su `openai`, `anthropic`, `deepseek`, `local` oppure `basic`.
- `PAKY_AI_MODEL` sul nome effettivo del modello, obbligatorio salvo in modalità base.
- `PAKY_UPSTREAM_KEY` per i servizi esterni. Resta sul server. Per una rete interna con autenticazione, usare un endpoint HTTPS.
- `PAKY_LOCAL_URL` per il server interno, per esempio `http://127.0.0.1:11434/v1/chat/completions` quando Ollama gira sullo stesso host.

Avviare con `python3 ai/gateway.py`. Il server ascolta su `127.0.0.1:8766` e richiede `PAKY_GATEWAY_TOKEN` di almeno 24 caratteri. Inviare a `POST /v1/ask` un JSON come `{"prompt":"Ciao"}` con header `Authorization: Bearer <token>`. La risposta contiene testo, provider e modello. Per raggiungerlo dalla Paky76, usare l'accesso HTTPS descritto sotto. Le chiavi dei provider non vanno nella dashboard, nei sorgenti o sul dispositivo.

## Collegamento dispositivo → gateway

1. Pubblicare `/v1/ask` sulla rete prevista tramite un reverse proxy HTTPS sul server del gateway. Lasciare Python su loopback e conservare l'header Authorization. La risposta verso il dispositivo deve avere un Content-Length valido.
2. Copiare `firmware/include/gateway_config.example.h` in `gateway_config.local.h`. Inserire URL HTTPS completo, CA che firma il certificato del proxy, token del gateway e server NTP raggiungibile. Il nome TLS deve corrispondere a quello nell'URL. Il file locale è escluso da Git. Per la produzione rimangono da definire provisioning e rotazione delle credenziali.
3. Compilare e caricare il firmware. Connettere la Paky76 al Wi-Fi e aprire la dashboard via USB o Wi-Fi locale. Scegliere **Modello via gateway HTTPS**. La Paky76 invia la richiesta al server, mentre la dashboard legge l'esito senza bloccare la configurazione. Con **Comandi offline**, la richiesta resta sul dispositivo.
4. Per una rete chiusa, usare DNS e NTP interni, un certificato verificato dalla CA configurata e un gateway impostato su `local`.

La verifica automatica copre il polling della dashboard e il contratto del gateway con adattatori simulati. Serve una prova su ESP32-S3 con il certificato del server effettivo e un modello abilitato.

## CPU e memoria

La base funziona con l'ESP32-S3-WROOM-1-N8 attuale. Per futuri modelli compatti di riconoscimento comandi o parole chiave, valutare **ESP32-S3-WROOM-1-N16R8**, con 16 MB flash e 8 MB PSRAM. Validare mappa dei pin riservati, avvio, firmware, partizioni, memoria di picco, prestazioni e disponibilità prima di aggiornare la BOM. Un modello generativo locale richiede un host più adatto, per esempio il server Ollama già presente in rete. L'aumento di flash da solo non fornisce RAM di inferenza o prestazioni sufficienti.

- [OpenAI Responses API](https://platform.openai.com/docs/api-reference/responses/create)
- [Anthropic Messages API](https://docs.anthropic.com/en/api/messages)
- [DeepSeek Chat Completions](https://api-docs.deepseek.com/api/create-chat-completion)
- [Ollama compatibilità OpenAI](https://docs.ollama.com/api/openai-compatibility)
- [Espressif ESP32-S3-WROOM-1](https://www.espressif.com/sites/default/files/documentation/esp32-s3-wroom-1_wroom-1u_datasheet_en.pdf)
