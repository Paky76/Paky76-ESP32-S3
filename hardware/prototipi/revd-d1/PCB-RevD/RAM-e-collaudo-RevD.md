# Paky76 Rev.D — Memoria e carico di lavoro

U1 è ESP32-S3-WROOM-1-N16R8 (JLCPCB C2913202). Il modulo integra 16 MB di flash e 8 MB di PSRAM octal. Il SoC ha 512 KB di SRAM interna, in parte occupata da sistema e firmware. Per questo profilo si mantiene U1 e non si aggiungono chip RAM. Verificare che il produttore monti proprio la variante N16R8.

## Limiti di progetto del primo firmware

| Funzione | Budget PSRAM | Ipotesi |
| --- | --- | --- |
| Audio e riconoscimento comandi | 2 MiB | Modello quantizzato italiano da selezionare, front end, arena e campioni. Due secondi di PCM mono a 16 kHz e 16 bit occupano 64.000 byte. |
| Acquisizione e decodifica immagini | 1 MiB | Una camera, QVGA o risoluzione inferiore, buffer JPEG con limite esplicito. Un fotogramma RGB565 a 320 × 240 occupa 153.600 byte. |
| Display e animazioni | 0,5 MiB | Trasferimenti del display a blocchi con buffer DMA dedicati. |
| Modello visivo e area di inferenza | 2 MiB | Modello leggero da selezionare, per esempio rilevamento di presenza a bassa frequenza. |
| Extra runtime | 0,5 MiB | Code, metadati, frammentazione e componenti applicativi allocati in PSRAM. |
| Riserva | 2 MiB | Obiettivo di margine al picco. |

Sono limiti progettuali, non consumi misurati o prestazioni garantite. Pianificare allocazione massima di 6 MiB in PSRAM, riuso dei buffer e lettura della microSD a blocchi. Misurare la latenza tra acquisizione, lettura microSD e inferenza. Se i modelli scelti superano i budget, ridurre risoluzione, frequenza o concorrenza e ripetere il collaudo.

## Collaudo sul primo campione

1. Configurare ESP-IDF per ESP32-S3, flash 16 MB e PSRAM octal. All'avvio leggere capacità PSRAM e log di inizializzazione.
2. Tenere buffer DMA critici, stack e risorse sensibili alla latenza nella RAM interna secondo le API dei driver. Rilevare heap minimo e blocco contiguo massimo separatamente per SRAM interna, memoria DMA e PSRAM.
3. Eseguire comandi vocali e animazione durante acquisizione dalla camera e lettura dalla microSD, prima senza rete e poi con Wi-Fi attivo. Registrare frame persi, overruns audio, latenze ed errori di allocazione.
4. Accettare il profilo solo dopo prova prolungata senza reset, errori o cali di alimentazione, con riserva PSRAM vicina al budget e memoria DMA sufficiente per le allocazioni successive. Misurare anche la linea 3,3 V nei picchi. La camera e il lettore microSD usano l'alimentazione separata prevista nel documento di cablaggio.

Documentazione Espressif
- https://documentation.espressif.com/esp32-s3-wroom-1_wroom-1u_datasheet_en.pdf
- https://docs.espressif.com/projects/esp-idf/en/stable/esp32s3/api-guides/external-ram.html
- https://docs.espressif.com/projects/esp-sr/en/latest/esp32s3/benchmark/README.html
