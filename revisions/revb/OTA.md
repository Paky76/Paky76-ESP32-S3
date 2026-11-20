# Paky76 Rev.B · Aggiornamento del firmware

## Prima preparazione via USB

1. Generare una chiave ECDSA P-256 con OpenSSL e custodire la chiave privata nel sistema di firma, fuori da Git. Esportare la chiave pubblica.
2. Copiare `firmware/include/ota_config.example.h` in `ota_config.local.h`. Compilare con la chiave pubblica PEM. Per l'aggiornamento online configurare anche URL HTTPS del pacchetto, CA del server e NTP.
3. Installare via cavo USB usando PlatformIO, includendo la nuova tabella delle partizioni. Fare il backup delle impostazioni da conservare prima del cambio di tabella. La tabella prevede due slot OTA da 3 MiB più la partizione OTA data.
4. Usare un numero crescente in `PAKY_FW_VERSION` per ogni release. Per firmare, usare il target 1 per `esp32s3`, 2 per `esp32s3_revb_audio`. Il firmatore confronta versione e target con il marcatore nel binario, e genera un pacchetto che lega firma, variante, versione, dimensione e SHA-256.

Esempio per la versione 2 della variante audio, dalla directory Rev.B:

```sh
python3 ota/package.py \
  --firmware firmware/.pio/build/esp32s3_revb_audio/firmware.bin \
  --version 2 --target 2 --key /percorso-privato/key.pem \
  --output Paky76-RevB-audio-2.pakyota
```

## Modalità di aggiornamento

- **Dashboard interna:** accedere alla pagina della Paky76 con le credenziali, scegliere il file `.pakyota` e caricarlo. Il dispositivo riavvia al termine di una scrittura riuscita.
- **Automatico online:** servire via HTTPS un pacchetto per la variante del dispositivo, con Content-Length, senza redirect o compressione di trasporto. L'interruttore nella dashboard è disattivato per impostazione iniziale. Una volta attivato, la Paky76 controlla al primo Wi-Fi disponibile dopo la sincronizzazione dell'orologio, poi ogni sei ore. I download in corso possono occupare temporaneamente il servizio della dashboard.
- Entrambe le modalità verificano la firma prima di scrivere, il limite dello slot, la variante e la versione. L'hash dell'immagine completa è verificato prima di selezionarla per il riavvio. Gli aggiornamenti online sono via **Wi-Fi**. Il trasporto LTE rimane da integrare.

## Collaudo da fare su esemplare fisico

Provare due versioni successive per ogni variante, con ripetizione da rete locale e online. Verificare firmatario errato, pacchetto alterato o troncato, versione precedente, variante incompatibile, certificato invalido, perdita Wi-Fi e interruzione di alimentazione in fasi diverse. Verificare la nuova versione in dashboard e la disponibilità della procedura di recupero USB.

La protezione contro versioni precedenti è applicativa. La validazione al primo avvio con rollback automatico e Secure Boot non sono configurati in questo firmware di sviluppo. Per la produzione definire recupero, gestione delle chiavi e politica di aggiornamento.

- [Espressif ESP32-S3 OTA](https://docs.espressif.com/projects/esp-idf/en/latest/esp32s3/api-reference/system/ota.html)
