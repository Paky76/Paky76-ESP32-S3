# Paky76 ESP32-S3

Paky76 è un assistente da scrivania con display, microfono, speaker e una videocamera opzionale. Il progetto prevede comandi semplici offline e risposte più articolate tramite JARVIS e Ollama su un PC o un server della rete locale.

**Revisione attuale Rev.G / D2.** Due PCB assemblabili e una scocca stampabile. Entrambe le schede hanno superato i controlli elettrici e di layout in KiCad. Il pacchetto è pronto per il preventivo del primo lotto. Il firmware applicativo, il collaudo fisico e l'accettazione del montaggio da parte di JLCPCB restano da completare.

[Pacchetto JLCPCB](hardware/prototipi/revg-d2/Paky76-RevG-D2-JLCPCB.zip) · [Istruzioni di caricamento](hardware/prototipi/revg-d2/LEGGIMI-PRIMA.md) · [Manuale di assemblaggio](hardware/prototipi/revg-d2/Paky76-Manuale-Assemblaggio-RevG-D2.pdf) · [Datasheet](hardware/prototipi/revg-d2/Paky76-Datasheet-RevG-D2.pdf) · [File di stampa 3D](hardware/prototipi/revg-d2/Scocca-D2/)

**Aggiornamento meccanico D2.1.** [Scarica gli STL aggiornati e il sorgente OpenSCAD](hardware/prototipi/revg-d2/Paky76-RevG-Scocca-D2.1.zip). Usa le [quote e le istruzioni D2.1](hardware/prototipi/revg-d2/Scocca-D2.1/MONTAGGIO-D2.1.md) per stampare la scocca corrente. Il pacchetto di fabbricazione Rev.G include la scocca D2 storica.

## Hardware

| Gruppo | Dotazione |
| --- | --- |
| Scheda principale | ESP32-S3-WROOM-1-N16R8, USB-C, RESET e BOOT, slot microSD J9 sul retro, RTC MCP7940N con batteria tampone CR1220 |
| Interfacce | Display SPI, speaker, microfono I²S, una videocamera SPI esterna, espansione LTE opzionale |
| Pannello comandi | Quattro frecce e OK su una PCB dedicata, collegata in I²C. LED RGB sul frontale, pilotato dal pannello |
| Alimentazione | Ingresso da 5 V e interruttore generale cablato nella scocca |
| Scocca D2 | Frontale, chassis, clip del display e copritasto in formato STL, con sorgente OpenSCAD |

## Funzioni previste

- **Offline.** Menu sul display, timer, volume e comandi brevi. La flash da 16 MB ospita il firmware, la PSRAM da 8 MB serve per l'elaborazione e la microSD conserva file e modelli compatibili. Un piccolo modello per comandi o riconoscimento locale va ancora selezionato e provato. La capacità della microSD da sola non determina quali modelli possono girare.
- **Sulla rete locale.** L'ESP32 può fare da terminale per un backend JARVIS e un LLM eseguito tramite Ollama. L'integrazione applicativa è in sviluppo.
- **Controlli fisici.** Frecce e OK per il menu, LED multicolore per stato e avvisi, orologio mantenuto a dispositivo spento tramite CR1220.

## Preventivo

La scheda principale e il pannello comandi si caricano come due PCB distinti. La scheda principale richiede Standard PCBA su entrambi i lati per montare lo slot microSD, anche scegliendo di saldare a mano il portapila. Il pannello si assembla sul lato Top. Prima di confermare la produzione, verificare disponibilità, orientamento dei componenti nel render CAM e pannellizzazione con JLCPCB.

## Archivio revisioni

- [Rev.F / D1](hardware/prototipi/revf-d1/LEGGIMI-PRIMA.md)

### Rev.D / D1


| Risorsa | Contenuto |
| --- | --- |
| [Istruzioni del prototipo](hardware/prototipi/revd-d1/LEGGIMI-PRIMA.md) | Stato della revisione, caricamento JLCPCB e stampa |
| [Schema, PCB e file JLCPCB](hardware/prototipi/revd-d1/PCB-RevD/) | KiCad, Gerber, BOM, CPL, report ERC/DRC e cablaggio |
| [File di stampa 3D](hardware/prototipi/revd-d1/Stampa-3D/) | OpenSCAD e STL |
| [Datasheet PDF](hardware/prototipi/revd-d1/Paky76-Datasheet-RevD-D1.pdf) | Specifiche, alimentazione, pinout e stato di validazione |
| [Manuale di assemblaggio PDF](hardware/prototipi/revd-d1/Paky76-Manuale-Assemblaggio-D1.pdf) | Sequenza di montaggio, cablaggio e viste CAD |
| [Specifiche RTC e pannello](hardware/prototipi/revd-d1/Specifiche/) | Requisiti e collegamenti previsti per la prossima revisione |
| [Pacchetto completo Rev.D / D1](hardware/prototipi/revd-d1/Paky76-Pacchetto-Prototipo-RevD-D1.zip) | Tutti i file del prototipo in un archivio |
