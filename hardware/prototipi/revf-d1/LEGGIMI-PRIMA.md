# Paky76 Rev.F / D1 — Preparazione dell'ordine

Carica Gerber-RevF-DFM.zip nel preventivo JLCPCB. PCB a quattro strati, 66 × 42 mm, spessore nominale 1,60 mm. Richiedi Standard PCBA e verifica la pannellizzazione. Scegli una sola coppia BOM/CPL:

- PCBA-Top: 34 posizioni sul lato superiore. Il portapila BT1 resta da saldare a mano sul lato inferiore. Acquistare Keystone 500, ad esempio Mouser 534-500, e una CR1220 da 3 V. Fori e piste di BT1 sono presenti nei Gerber.
- PCBA-Completa: 35 posizioni. Usala se JLCPCB conferma disponibilità del Keystone 500 C238121 e montaggio passante sul retro. Il CPL di BT1 indica il centro della sede circolare della pila. Far verificare posizione, lato e polarità.

U5 C51106 è il MCP7940N-I/SN in SOIC-8. Y1 C252399 è il quarzo da 32,768 kHz, CL 7 pF. C8/C9 C376804 sono 8,2 pF C0G, valori iniziali a verificare sul campione. Controlla tutte le disponibilità nel tuo carrello, in particolare U5, Y1, C8/C9 e i connettori. Fai confermare il piazzamento in vista 2D e il trattamento del pad termico del modulo ESP32. Usa solo file Rev.F, perché la Rev.E ha un altro RTC.

## Collaudo

I²C: indirizzo RTC 0x6F, SDA GPIO21 e SCL GPIO47, pull-up 4,7 kΩ a 3,3 V. A scheda alimentata, impostare data e ora con il driver MCP7940N, abilitare ST in RTCSEC e VBATEN in RTCWKDAY. Verificare OSCRUN. Controllare avvio del quarzo e deriva al variare di temperatura e alimentazione. Disconnettere il 5 V e verificare che l'ora avanzi al riavvio offline con la pila inserita. Usare una pila primaria da 3 V e rispettare la polarità.

ERC, DRC e confronto schema/PCB sono puliti. Accettazione CAM, compatibilità fisica della scocca e collaudo funzionale restano da completare. Il firmware RTC da collaudo non è incluso. Lo slot microSD sulla PCB, la croce, il LED RGB e l'interruttore generale sono sviluppi separati.
