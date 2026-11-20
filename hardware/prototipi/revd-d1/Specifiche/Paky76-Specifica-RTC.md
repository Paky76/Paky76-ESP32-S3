# Paky76 — batteria tampone per data e ora

Prevedere un RTC esterno sulla PCB con portapila SMD sostituibile per CR1220 da 3 V. La pila alimenta solo VBACKUP del RTC. L'alimentazione ordinaria del RTC e i pull-up I²C fanno capo alla linea +3V3 della scheda. La massa è comune. La CR1220 è una cella primaria: disabilitare il circuito di ricarica del RTC e verificare che non riceva corrente di carica.

| Elemento | Scelta di progetto |
| --- | --- |
| RTC candidato | Micro Crystal RV-3028-C7, C2829066. JLCPCB mostrava stock pubblico zero alla verifica. Confermare approvvigionamento prima di congelare il footprint. |
| Batteria e portapila | CR1220, portapila SMD per 12 mm come Keystone 3000. Verificare l'accesso dalla scocca e lo spazio necessario per estrarre la cella. Inserire la pila dopo l'assemblaggio. |
| Bus I²C | SDA GPIO21 (pad 23 U1), SCL GPIO47 (pad 24 U1), entrambi liberi sulla Rev.D. Pull-up alla 3,3 V principale, da dimensionare con il layout e la capacità del bus. |
| Prima accensione | Impostare data e ora via Wi-Fi/SNTP o configurazione iniziale. Programmare e rileggere la configurazione persistente del backup del RTC, perché la commutazione è disattivata all'uscita di fabbrica. Tenere la ricarica disabilitata. |
| Avvio offline | Leggere il RTC e validare lo stato prima di datare eventi, foto e registrazioni. Tenere l'ora in UTC e applicare il fuso Europe/Rome nell'interfaccia. |
| Collaudo | Impostare l'ora, staccare il 5 V, verificare che la 3,3 V principale si spenga e riaccendere senza rete dopo almeno 24 ore. Controllare ora, deriva e stato RTC. Ripetere la prova con pila assente per verificare la gestione dell'ora non valida. |

La CR1220 preserva l'ora. Gli avvisi mentre l'alimentazione principale è scollegata richiederebbero un dispositivo ancora alimentato. Il timer RTC dell'ESP32-S3 perde il riferimento all'accensione dopo un'interruzione totale.

Questa specifica è per la prossima revisione. La Rev.D pubblicata contiene ancora schema e PCB privi del circuito RTC e del portapila. Prima di ordinare una versione con batteria occorrono inserimento e instradamento in KiCad, verifica meccanica, ERC/DRC e aggiornamento dei file PCBA.

- [Micro Crystal — RV-3028-C7 e commutazione backup](https://www.microcrystal.com/fileadmin/Media/Products/RTC/App.Manual/RV-3028-C7_App-Manual.pdf)
- [JLCPCB — RV-3028-C7](https://jlcpcb.com/partdetail/Micro_Crystal-RV_3028C7/C2829066)
- [Espressif — System Time](https://docs.espressif.com/projects/esp-idf/en/latest/esp32s3/api-reference/system/system_time.html)
