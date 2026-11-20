# Paky76 — Pacchetto di prototipazione

La scheda principale disponibile è la Rev.D. La scocca D1 aggiunge aperture per comandi, LED, obiettivo, microfono, lettore microSD e interruttore. Le quote vanno verificate con i componenti effettivi prima della stampa finale.

| Cartella o file | Contenuto |
| --- | --- |
| PCB-RevD | Sorgenti KiCad, Gerber, BOM, CPL, verifiche e pinout Rev.D |
| Stampa-3D | OpenSCAD e quattro STL in millimetri per Cura e Sidewinder X1 |
| Specifiche | RTC con CR1220 e pannello frontale con croce, LED RGB e interruttore |
| Paky76-Manuale-Assemblaggio-D1.pdf | Manuale illustrato con render ricavati da KiCad e dagli STL |

## Caricamento JLCPCB

In PCB-RevD usa Gerber-RevD-DFM.zip, BOM-JLCPCB-RevD.csv e CPL-JLCPCB-RevD.csv. Richiedi preventivo Standard PCBA Top e pannellizzazione per la PCB 66 × 42 mm. Verifica che JLCPCB confermi disponibilità dei 27 riferimenti, posizione e pin 1 dell'ESP32-S3, trattamento delle forature nel pad centrale e montaggio passante di J4, J6 e J7.

La Rev.D prevede il lettore microSD, il microfono e la camera come moduli cablati. Non acquistare la Rev.D se l'ordine deve includere slot microSD a bordo, RTC con portapila o pannello comandi assemblato: questi circuiti richiedono ancora una revisione KiCad e il relativo pacchetto PCBA. L'interruttore è previsto sul cablaggio comune a 5 V. I render sono viste dei file effettivi; non sono foto di un campione fabbricato.

## Stampa

Usare gli STL al 100%, importati in millimetri, sul profilo Cura della Sidewinder X1. Stampare un frontale, un chassis e quattro clip. Il supporto comandi è una dima di ingombro con fori allineati al frontale. Il fissaggio effettivo della scheda tasti e dei moduli va dimensionato sui componenti scelti. Aprire il sorgente OpenSCAD per ritoccare quote e posizioni prima di rigenerare le mesh.
