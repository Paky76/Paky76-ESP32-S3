# Paky76 Rev.G / D2 — File per il preventivo del prototipo

La consegna comprende due PCB assemblabili separatamente: scheda principale **83,25 × 42 mm** a 4 strati e pannello comandi **34 × 34 mm** a 4 strati. La scocca D2 è progettata per queste dimensioni. Le quote e l'accessibilità vanno provate sul campione. I file di questa revisione sono destinati al preventivo del primo lotto.

## Caricamento JLCPCB

1. Scheda principale: caricare Gerber-RevG-Principale.zip e scegliere Standard PCBA **Top + Bottom**. Lo slot microSD J9 è sul lato Bottom. Scegliere la coppia BOM/CPL in PCBA-Principale-Completa oppure in PCBA-Principale-BT1-Manuale. Nella seconda, BT1 si acquista a parte e si salda sul retro, ma J9 resta nella distinta e nel CPL.
2. Pannello: caricare Gerber-RevG-Pannello.zip e l'unica coppia BOM/CPL in PCBA-Pannello. Assemblaggio Top. I due fori M2 sono lavorazioni PCB. Chiedere conferma di pannellizzazione, quantità e modalità di consegna per entrambe le schede.
3. Verificare nel carrello la disponibilità effettiva di tutti i riferimenti. Controllare in particolare U1 ESP32-S3, U5 RTC, J8/J9, U1 e SW1–SW5 del pannello, slot e portapila sul retro della scheda principale. Il codice C238121 del portapila e il montaggio THT Bottom vanno confermati separatamente. Verificare pin 1 e orientamenti effettivi nel render CAM, soprattutto U1, U5, J9 e l'espansore del pannello.
4. Il montaggio del portapila e la pila sono operazioni diverse. Inserire la CR1220 dopo il montaggio. LED RGB, interruttore, cavi e moduli esterni sono componenti da montare nella scocca.

## Collegamenti

- **Pannello I²C:** J8 principale a J1 pannello, fili 1→1, 2→2, 3→3, 4→4. 1 = 3,3 V, 2 = GND, 3 = SDA GPIO21, 4 = SCL GPIO47. Verificare i numeri pin a entrambe le estremità. TCA9534PWR a 0x20 e RTC a 0x6F condividono i pull-up della scheda principale. Interfaccia iniziale 100 kHz.
- **Tasti:** P0–P4 attivi bassi. Nella D2 il pannello si monta con l'espansore rivolto verso il basso e i pulsanti verso il frontale. Mappa fisica con questo orientamento: P1 Su, P0 Giù, P3 Sinistra, P2 Destra, P4 OK. Fori M2 a 28 mm tra i centri con asse a 2 mm sopra OK. La corsa del gruppo plunger-pulsante va verificata prima del serraggio.
- **LED:** J2 pannello, pin 1 anodo comune 3,3 V, 2 catodo rosso, 3 catodo verde, 4 catodo blu. P5–P7 pilotano i tre colori in assorbimento, con resistenze sul pannello. Usare un LED diffuso RGB da 5 mm ad anodo comune compatibile con bassa corrente e 3,3 V, montato sul frontale. Verificare pinout, colori e luminosità del LED reale.
- **Interruttore:** riferimento C&K 7101SYZQE, pannello con foro nominale 6,65 mm. Commutare solo il +5 V DC a monte dei tre rami. Usare COM e una sola uscita; isolare il terzo terminale, le saldature e il cablaggio. Da qui ripartire verso alimentazione USB-C J1 tramite cavo/adattatore conforme, J5 audio a 5 V e regolatore dedicato 3,3 V per la camera. GND comune. Alimentatore regolato da 5 V, dimensionato sul carico reale. Per il servizio USB scollegare il cavo di alimentazione da J1 e tenere spento il cablaggio della scocca prima di collegare il PC.
- **Camera J7:** pin 1 GND, 2 SCK, 3 MOSI, 4 MISO, 5 CS camera, 6 SD_CS riservato alla scheda e da lasciare libero nel cablaggio. Camera esterna SPI con livelli 3,3 V e MISO in alta impedenza a CS alto. Alimentazione esterna dedicata. Slot J9 a bordo con CS GPIO42 e 3,3 V dalla scheda. Inizializzare la microSD in SPI tenendo CS camera alto, poi abilitare la camera.
- **Microfono:** J6 pin 1 3,3 V, 2 GND, 3 BCLK, 4 LRCLK, 5 DOUT verso GPIO14. Speaker fra i due pin di J3. J2 sulla scheda principale è il display, J4 è LTE opzionale con alimentazione propria. RESET e BOOT sono sulla scheda principale, accessibili tramite rimozione del frontale.

## Collaudo del primo campione

Verifiche digitali: ERC e DRC con parità schema/PCB su entrambe le schede, coerenza riferimenti BOM/CPL, STL chiusi e connessi. Le quote D2 sono iniziali. Le prove fisiche devono includere ritenzione RTC (abilitare ST e VBATEN), corrente e temperatura del regolatore 3,3 V con microSD, display e Wi-Fi attivi, integrità SPI, corsa dei tasti, LED, spegnimento e accesso alla microSD. Misurare 3,3 V nei picchi e in regime e verificare la temperatura di U2 in scocca prima dell'utilizzo continuativo. Espellere la microSD via software prima di togliere l'alimentazione. Il firmware applicativo e il collaudo in fabbrica richiedono attività sul campione.
