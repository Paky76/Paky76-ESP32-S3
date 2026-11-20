# Paky76 ESP32-S3

Paky76 è un **assistente da scrivania interattivo** basato su ESP32-S3, con un display per occhi animati e menu, audio, una videocamera e una scocca stampabile in 3D. Il progetto esplora due modalità: azioni semplici eseguite sul dispositivo e risposte più articolate tramite un server JARVIS sulla rete locale.

**Stato del progetto:** prototipo hardware **Rev.E**, scocca di prova **D1**. Il repository contiene i sorgenti KiCad e i file per richiedere un preventivo di assemblaggio. Le funzioni applicative, l'integrazione meccanica e il collaudo fisico sono ancora in sviluppo.

> **Rev.E con batteria tampone:** RTC RV-3028-C7 e portapila CR1220 sul lato inferiore sono integrati nello schema e nella PCB. Le verifiche KiCad sono completate. Disponibilità dei componenti, montaggio passante sul retro e prova del backup restano da confermare. [Istruzioni Rev.E](hardware/prototipi/reve-d1/LEGGIMI-PRIMA.md) · [Pacchetto Rev.E](hardware/prototipi/reve-d1/Paky76-RevE-D1-RTC-CR1220.zip) · [Datasheet Rev.E](hardware/prototipi/reve-d1/Paky76-Datasheet-RevE-D1.pdf) · [Manuale Rev.E](hardware/prototipi/reve-d1/Paky76-Manuale-Assemblaggio-RevE-D1.pdf)

## Cosa potrà fare

| Uso previsto | Come funziona |
| --- | --- |
| **Interazione offline** | L'ESP32 esegue comandi brevi, aggiorna il display e riproduce suoni locali. Esempi da implementare: avviare un timer, regolare il volume o cambiare l'espressione degli occhi. Per i comandi vocali in italiano va ancora selezionato e collaudato un modello compatto. |
| **Assistente JARVIS sulla rete locale** | Paky76 può fare da terminale per un backend JARVIS su PC o server, con modelli eseguiti tramite Ollama. L'obiettivo è ricevere risposte e riprodurle sullo speaker tramite Wi‑Fi locale, anche senza un servizio cloud. L'integrazione software è da completare. |
| **Camera e memoria rimovibile** | Una videocamera SPI e un lettore microSD cablati possono condividere il bus di J7. La microSD può conservare immagini, audio e file di modelli compatibili con il firmware. Il funzionamento con entrambi i moduli collegati è da verificare sul campione. |
| **Menu e indicatori** | Il frontale D1 prevede le aperture per quattro frecce, un tasto OK e un LED RGB. La specifica prevede configurazione di rete, volume, luminosità, data e ora, camera e microSD, con indicazione dello stato di connessione. Pannello e firmware del menu sono in sviluppo. |

Gli **8 MB di PSRAM** sono destinati ai buffer e ai piccoli modelli locali, mentre i **16 MB di flash** ospitano firmware e dati. La capacità della microSD serve alla conservazione dei file. La conversazione libera è prevista tramite JARVIS e un LLM conversazionale a bordo dell'ESP32 resta da dimostrare.

## Hardware e scocca

- **Scheda principale:** ESP32-S3-WROOM-1-N16R8, PCB a quattro strati da 66 × 42 mm, USB-C e pulsanti RESET e BOOT.
- **Interfacce:** display SPI su J2, speaker su J3, modem LTE esterno opzionale su J4, alimentazione audio a 5 V su J5, microfono I²S su J6, camera e lettore microSD su J7. Il modem richiede alimentazione e cablaggio compatibili.
- **Scocca D1:** sorgente OpenSCAD e STL per Cura e Artillery Sidewinder X1. Frontale, chassis, clip display e dima dei comandi sono disponibili per prove di montaggio.
- **Sviluppi ancora previsti:** slot microSD saldato sulla scheda, pannello a cinque tasti con LED RGB e interruttore generale. La microSD si collega ancora come modulo esterno.

## File della Rev.D / D1 precedente

| Risorsa | Contenuto |
| --- | --- |
| [Istruzioni del prototipo](hardware/prototipi/revd-d1/LEGGIMI-PRIMA.md) | Stato della revisione, caricamento JLCPCB e stampa |
| [Schema, PCB e file JLCPCB](hardware/prototipi/revd-d1/PCB-RevD/) | KiCad, Gerber, BOM, CPL, report ERC/DRC e cablaggio |
| [File di stampa 3D](hardware/prototipi/revd-d1/Stampa-3D/) | OpenSCAD e STL |
| [Datasheet PDF](hardware/prototipi/revd-d1/Paky76-Datasheet-RevD-D1.pdf) | Specifiche, alimentazione, pinout e stato di validazione |
| [Manuale di assemblaggio PDF](hardware/prototipi/revd-d1/Paky76-Manuale-Assemblaggio-D1.pdf) | Sequenza di montaggio, cablaggio e viste CAD |
| [Specifiche RTC e pannello](hardware/prototipi/revd-d1/Specifiche/) | Requisiti e collegamenti previsti per la prossima revisione |
| [Pacchetto completo Rev.D / D1](hardware/prototipi/revd-d1/Paky76-Pacchetto-Prototipo-RevD-D1.zip) | Tutti i file del prototipo in un archivio |

Per il **preventivo JLCPCB**, usa Gerber, BOM e CPL della stessa Rev.D. Richiedi conferma del servizio Standard PCBA, della pannellizzazione, del piazzamento dell'ESP32 e del montaggio dei connettori. Il collaudo del primo campione deve verificare alimentazione, USB, display, audio, camera e microSD e l'adattamento alla scocca.
