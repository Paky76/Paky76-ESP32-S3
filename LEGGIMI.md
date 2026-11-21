# Paky76 Mini A5 • OLED quadrato da 1,5″

**Per le due PCB già ordinate.** La principale A4 e il frontale A1 restano identici alla consegna A4.1. Alla A5 appartengono la scocca stampabile, il montaggio e lo sketch per il display nuovo. 

## Documentazione A5

- [Manuale illustrato](Documentazione/Paky76-Mini-A5-Manuale-Assemblaggio.pdf)
- [Schema elettrico a simboli, pagina unica A3](Documentazione/Paky76-Mini-A5-Schema-Elettrico.pdf)
- [Tavola di cablaggio, pagina unica A3](Documentazione/Paky76-Mini-A5-Schema-Cablaggio-Completo.pdf)
- [Schemi di collegamento](Documentazione/Paky76-Mini-A5-Schemi-Collegamento.pdf)
- [Datasheet tecnico](Documentazione/Paky76-Mini-A5-Datasheet.pdf)
- [Viste CAD e tavole quotate](Documentazione/Figure/)
- [Piedinatura rapida](Cablaggio/Pinout-OLED-SH1107.md)

## Prima di assemblare

- Display I²C **a 4 pin**, SH1107G-02, 128 × 128, PCB **34 × 47 mm**. I dati dichiarati indicano 11,3 mm di spessore massimo, area visibile 28,86 × 28,86 mm e quattro fori Ø 2,2 mm. Il CAD assume interasse **29 × 42 mm** e finestra spostata di **3 mm** verso il connettore. Controllare le quote sul pezzo reale o con la dima prima di stampare la cornice definitiva.
- Riutilizzare XIAO, connettori, pulsanti, S1 Nidec MFS201N-Z e LiPo protetta 1S già previsti per A4.1. Per il display usare un cavetto **JST SH 4 vie 1,0 mm lato frontale** e fili o terminali compatibili con il passo **2,54 mm lato OLED**. Quantità e codici dei componenti sulle PCB sono nelle BOM originali.
- Ingombro nominale del guscio chiuso **49 × 54 × 41,6 mm** esclusi occhiello, copritasti e cursore. Lunghezza con occhiello **61,5 mm**. Il maggior spessore dà spazio al display, ai JST e ai cavi.
- Schede nude: U1 ha anche due pad batteria sotto al modulo. Far saldare entrambi secondo la procedura SMD; la sola saldatura delle castellazioni laterali lascia incompleto quel collegamento.

## Stampa e montaggio

| File in Meccanica | Quantità | Indicazione |
| --- | ---: | --- |
| `tray.stl` | 1 | Guscio, fondo piatto sul piano. Controllare e aggiungere supporti al ripiano batteria nel profilo Cura. |
| `bezel.stl` | 1 | Cornice quadrata. Stampare con la faccia esterna sul piano. |
| `button.stl` | 2 | Copritasti per SW1 e SW2. Stampare in verticale con la flangia sul piatto. |
| `oled_gauge.stl` | 1 facoltativa | Dima del PCB OLED per confrontare contorno e fori. |
| `fit_check.stl` | 1 facoltativa | Provino per verificare scorrimento nel passaggio Ø 3,35 mm. |
| Altre dime | Secondo necessità | Principale, frontale, batteria e interruttore. |

Usare Cura al 100% sulla Sidewinder X1. Punto di partenza per gli accoppiamenti: layer 0,20 mm. Gli STL si usano senza ridimensionamento. Modificare nel sorgente OpenSCAD `oled_mounts`, `oled_window_y` e `button_length` se le misure del campione lo richiedono.

1. **Guscio.** Montare S1 sul fianco sinistro, con terminali isolati. Posare la principale sugli appoggi bassi, componenti verso l’interno e USB-C allineata all’apertura opposta all’occhiello. Accedere alle viti posteriori dalle asole del ripiano. Provare l’inserimento del cavo USB reale.
2. **Batteria.** Usare inizialmente la dima sul ripiano, più vicina all’occhiello che alla USB-C. Far passare una ritenzione morbida nelle asole del ripiano e interporre uno strato isolante adeguato. La cella, i suoi fili e l’isolante devono stare sotto il frontale senza compressione e senza contatto con viti o terminali. Tenere il connettore della batteria scollegato finché non è terminata la prova USB.
3. **Frontale.** Orientare il lato componenti verso il display. Il J2 OLED è verso il bordo USB-C. Inserire il cavo J1 a 6 vie tra le schede, pin 1→1 fino a 6→6, e appoggiare il frontale sulle quattro colonnine. Verificare la continuità del cavo.
4. **Cornice.** Dall’interno, inserire entrambi i copritasti nel proprio passaggio con la flangia larga dentro. Lo stelo deve scorrere e i pulsanti devono tornare liberi a riposo. Montare l’OLED con il vetro verso la finestra e la fila dei quattro pin verso il lato USB-C. Dall’interno avvitare il PCB OLED ai quattro supporti con viti M2 corte, indicativamente M2×4 da verificare con il pezzo in mano, così da non bucare la faccia esterna o caricare il vetro. Provare prima con la dima. Usare i fori della scheda, senza fare pressione sul vetro o sul flat.
5. **Chiusura.** Inserire il cavetto display. Accostare la cornice verificando lo spazio dietro l’header OLED e sopra i JST, e mantenere una piccola ansa per poter riaprire. I fili devono stare fuori dagli appoggi e dai copritasti. Le quattro viti M2 di chiusura attraversano cornice e PCB frontale e impegnano le colonnine del guscio. Il CAD lascia circa **20,9 mm** tra fondo della sede testa e colonnina, con circa **4 mm** di foro utile. Provare viti **M2×23** o una lunghezza con 2–3 mm di presa effettiva, in base alla testa e al pezzo stampato. Scegliere a secco anche le lunghezze delle viti della principale e di S1.

## Cablaggio esatto

| J2 frontale | OLED I²C secondo il disegno della variante 4 pin |
| --- | --- |
| Pin 1 GND | Pin 2 GND |
| Pin 2 3V3 | Pin 1 VCC |
| Pin 3 SDA | Pin 4 SDA |
| Pin 4 SCL | Pin 3 SCL |

Il testo commerciale cita anche «pin 2 VDD». Il disegno a 4 pin indica l’ordine riportato sopra. **Prima di alimentare, verificare le serigrafie del modulo ricevuto e collegare per nome del segnale.** Usare 3,3 V. Sul modulo a 4 pin non è previsto il cablaggio esterno RES della vecchia configurazione Waveshare a 7 pin.

S1 è sul positivo della LiPo verso J2 **della principale**, pin 1 VBAT. Il negativo va al pin 2 GND. Con USB scollegata, OFF isola la batteria. Con USB collegata, la XIAO può alimentarsi via USB anche in OFF. Per ricaricare mettere S1 su ON. Controllare polarità e isolamento a freddo con il multimetro.

## Firmware e collaudo

1. In Arduino IDE installare il core **esp32 by Espressif Systems** e la libreria **U8g2**. Selezionare **XIAO_ESP32S3**. Aprire `Firmware/Paky76MiniSH1107/Paky76MiniSH1107.ino` e caricarlo con il cavo USB-C dati e batteria scollegata.
2. Aprire il monitor seriale a 115200 baud. Lo sketch cerca 0x3C e 0x3D a 100 kHz con SDA su GPIO5 e SCL su GPIO6. Riprova ogni 2 secondi se non vede il modulo. Un ACK conferma il bus, non il tipo di controller.
3. Verificare che gli occhi occupino il pannello correttamente e che SW1/SW2 spostino lo sguardo nel verso atteso. Se serve, cambiare `U8G2_R0` in `U8G2_R1`, `U8G2_R2` o `U8G2_R3` e ricompilare. Dopo 30 s di inattività il display si spegne e si riattiva premendo un tasto. L’ESP32 resta alimentato.
4. Con USB scollegata, verificare la polarità e collegare la batteria con S1 in OFF. Provare l’accensione in ON e lo spegnimento in OFF. Con USB collegata e S1 in ON verificare la ricarica e la temperatura. Prova OLED, gioco dei tasti e cablaggio prima di chiudere il guscio.

Verifiche eseguite: file KiCad e JLCPCB identici alla A4.1, mesh STL chiuse e logica firmware provata su host con periferiche simulate. Firma del driver verificata sul sorgente U8g2. In questo ambiente l’installazione del core ESP32 è fallita per l’accesso agli indici Arduino. Compilazione per la XIAO, ingombri sul componente reale e prova di alimentazione/ricarica restano da eseguire.
