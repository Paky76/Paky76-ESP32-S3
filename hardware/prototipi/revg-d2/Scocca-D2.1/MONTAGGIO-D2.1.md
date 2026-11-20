# Paky76 Rev.G — Scocca D2.1

Questa revisione meccanica usa le due schede Rev.G. Per l'assemblaggio del pannello con i comandi ALPS usa la distinta `BOM-JLCPCB-RevG-C115351.csv`.

| Controllo | Riferimento e quota nominale |
| --- | --- |
| Scheda principale | 83,25 × 42 mm; appoggio sul piano Z = 9 mm e inserimento dal frontale |
| Antenna ESP32-S3 | Modulo sul lato posteriore. Il PCB termina a Y = 18,5 mm e il modulo a Y = 24,5 mm, quindi sporge di 6 mm. Parete interna posteriore a Y = 27,2 mm, con 2,7 mm di aria dalla punta. Tenere cavi e accessori metallici lontani dalla zona antenna e verificare il Wi-Fi con la scocca chiusa |
| Pannello comandi | 34 × 34 mm, cinque assi a passo 8 mm. Montaggio con tasti verso il frontale ed espansore verso il basso. Asse dei due fori M2 2 mm sopra OK, interasse 28 mm |
| Pulsanti | ALPS SKQGABE010, attuatore nominale 1,50 mm. Copritasti guidati da una sede con piano antirotazione, 0,35 mm di gioco assiale nominale a riposo. Impiegare 4 frecce e 1 OK |
| Display | Waveshare SKU 15867, ST7789 240 × 240. Scheda larga 31 mm e alta 45 mm nella scocca; quattro fissaggi a interasse 26 × 40 mm. Area attiva 23,4 × 23,4 mm, finestra da 24,8 mm con imbocco svasato da 28,2 mm |
| USB-C J1 | Porta sul frontale, centro X = 13 mm. Apertura 16 × 9 mm, centrata a Z = 10,8 mm. Provare la guaina del cavo effettivo |
| microSD J9 | Imbocco sul fianco destro, sotto il PCB. Passaggio largo 15 mm e alto 4,2 mm, con invito esterno per la presa. Provare inserimento, scatto ed estrazione |
| Periferiche | Griglia e sede per speaker nominale da Ø28 mm, LED RGB da Ø5 mm, porta ottica camera da Ø8 mm, presa microfono da Ø2,3 mm e foro interruttore da Ø6,65 mm. Il fissaggio interno dei moduli camera e microfono dipende dalle dimensioni dei moduli scelti |

## Stampa e montaggio

1. In Cura importa i file al 100%, in millimetri. Orientamento del frontale con la faccia esterna sul piatto e dello chassis con il retro sul piatto. Impostazione di partenza per Sidewinder X1 con ugello da 0,4 mm: strato da 0,20 mm e tre pareti. Controlla le anteprime dei ponti sopra i passaggi laterali e delle flange dei copritasti; usa supporti locali dove necessario.
2. Inserisci i copritasti da dietro, orientando la freccia in base alla sede. Fissa il pannello dai due punti M2. Ogni tasto deve tornare libero e scattare una volta alla pressione. Verifica il gioco prima di serrare.
3. Monta il display sui quattro appoggi, con viti M2 corte con lunghezza calibrata sui fori ciechi e sullo spessore del modulo. Controlla che il vetro non tocchi il frontale e che l'intera area attiva sia visibile. Lascia spazio al cavo sul retro.
4. Inserisci la scheda principale sulle guide, passa i cablaggi lontano dall'antenna e fissa frontale e chassis. Prova USB-C e microSD prima di serrare. Per la CR1220 e RESET/BOOT apri il frontale.
5. Sul primo esemplare controlla visibilità del display, accesso alle porte, corsa dei tasti, viti, cablaggi e qualità del segnale Wi-Fi. Le quote sono nominali CAD; il montaggio fisico e la tolleranza della stampante si verificano sul campione.

[Display Waveshare](https://www.waveshare.com/wiki/1.3inch_LCD_Module) · [Dimensioni e interassi display](https://www.tinytronics.nl/image/cache/data/product-3478/waveshare-1.3-inch-spi-ips-tft-lcd-display-module-240240-pixels-dimensions-1500x1500w.jpg) · [Datasheet Espressif](https://www.espressif.com/sites/default/files/documentation/esp32-s3-wroom-1_wroom-1u_datasheet_en.pdf)
