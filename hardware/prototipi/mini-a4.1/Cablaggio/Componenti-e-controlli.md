# Paky76 Mini A4.1 — Componenti e controllo prima dell’accensione

Aprire **Schema-interconnessioni.svg** per vedere l’interruttore S1 insieme a entrambe le schede. S1 è il riferimento di assemblaggio del cablaggio. SW1 e SW2 sono i tasti di interazione saldati sul frontale.

| Parte | Componente | Montaggio |
| --- | --- | --- |
| Principale U1 | Seeed XIAO ESP32-S3, 113991114, C20467913 | JLCPCB, lato superiore. USB-C integrata |
| Principale J1, frontale J1 | JST SH 6 vie, C160392 | JLCPCB su entrambe. Cavo dritto pin per pin |
| Principale J2 | Due piazzole passanti BAT-SW | Saldatura manuale. Pin 1 positivo da S1, pin 2 negativo |
| Frontale J2 | JST SH 4 vie, C160390 | JLCPCB. Cavo OLED da adattare alla piedinatura del display |
| Frontale SW1, SW2 | Due Panasonic EVQP7A01P, C79167 | JLCPCB. Verificare corsa dei tasti nella scocca |
| S1 | Nidec MFS201N-Z a slitta | Fianco sinistro del guscio, montaggio manuale |
| Batteria | LiPo protetta 1S da 350 mAh, 4,2 V a fine carica | Cablaggio con connettore volante e polarità verificata |
| Display | SH1106 128×64, 3,3 V, I²C | Montaggio manuale e prova di ingombro |
| Antenna | 2,4 GHz compatibile XIAO | Collegare quella del modulo o procurarla a parte se assente |

| Pin comune J1 | Funzione | Arrivo |
| --- | --- | --- |
| 1 | GND | Frontale J2 pin 1 e un contatto di SW1/SW2 |
| 2 | 3V3 | Frontale J2 pin 2 |
| 3 | SDA | Frontale J2 pin 3, XIAO GPIO5 |
| 4 | SCL | Frontale J2 pin 4, XIAO GPIO6 |
| 5 | LEFT_N | SW1, XIAO GPIO2 |
| 6 | RIGHT_N | SW2, XIAO GPIO1 |

I cavi commerciali JST SH possono variare nell’ordine dei fili. Verificare pin a pin con il multimetro, a dispositivi scollegati, senza dedurre la polarità dal colore. S1 interrompe il positivo batteria. Il negativo resta diretto. Per S1 identificare il comune e la posizione ON con il multimetro e isolare tutti i terminali.

Per l’OLED, un SH1106 nativo I²C con quattro fili semplifica il cablaggio. Verificare dimensioni e fissaggi rispetto alla cornice. Il Waveshare OLED (B) usato per le quote della scocca esce di fabbrica in SPI. Per usarlo con il nostro frontale, servono la configurazione I²C (BS0=0, BS1=1, DIN=0, CLK=1) e la gestione di CS, D/C e RST secondo il disegno del produttore. Collegare senza supposizioni sulla posizione dei pin. [Documentazione Waveshare](https://www.waveshare.com/wiki/1.3inch_OLED_(B))

### Condizioni da confermare sul primo campione

1. **A freddo** — S1 aperto in OFF, continuità in ON, nessun corto VBAT–GND, polarità misurata prima di collegare la cella. Controllare continuità delle sei vie e orientamento dei connettori.
2. **Solo USB** — Avvio della XIAO e rilevamento OLED a 0x3C o 0x3D. Verificare che premendo i tasti singolarmente il firmware sposti lo sguardo nel verso previsto. Provare anche entrambi i tasti.
3. **Solo batteria** — Avvio in ON e spegnimento in OFF. Controllare caduta di tensione al cursore e assenza di reset a display attivo.
4. **USB e batteria** — In ON misurare la corrente di carica a batteria parzialmente scarica e la temperatura in scocca. In OFF la XIAO può avviarsi via USB, mentre il percorso di carica della batteria è aperto.
5. **Guscio chiuso** — Provare corsa e ritorno dei tasti, accesso a USB-C e S1, ritenzione di display e batteria e assenza di pressione su cavi e cella.
