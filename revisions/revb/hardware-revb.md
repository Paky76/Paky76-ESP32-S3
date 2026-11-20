# Specifica di integrazione Rev.B

## Forma e disposizione

Personaggio originale color avorio opaco con inserti verde petrolio, base stabile con due piedini, volto inclinato nella calotta e griglia microforata sul petto. Il volto usa lo ST7789 Waveshare SKU 15867 da 240 × 240. La scheda entra nella base, la calotta ospita modulo LCD e cablaggio. Prevedere una piastra posteriore avvitata per assistenza, pulsanti accessibili e sportellino nano-SIM separato sotto la base. Quote di ingombro iniziali circa 78 × 62 × 94 mm, da rifinire con connettori, antenna e speaker effettivi.

| Sottosistema | Scelta Rev.B |
|---|---|
| MCU | ESP32-S3-WROOM-1-N8, conservando l'interfaccia ST7789 e USB della Rev.A. |
| Voce | Amplificatore digitale MAX98357A con alimentazione 5 V e uscita differenziale. Speaker candidato da 28 mm, 4 Ω, 3 W, montato con guarnizione e vano acustico separato. Limite software e misura temperatura/distorsione a volume massimo. |
| Cellulare | Quectel EG915U-EU LTE Cat 1 bis candidato, con modem a 3,8 V nominali, interfaccia UART, nano-SIM estraibile e antenna LTE interna da qualificare. |
| SIM | Nano-SIM fisica per il pilotaggio. eSIM futura tramite eUICC e profilo abilitato dal fornitore, dopo verifica della procedura di provisioning e della variante del modem. Prevedere solo una SIM attiva nel primo prototipo. |
| Alimentazione | Ingresso USB-C di alimentazione separato dalla USB dati del primo prototipo. Alimentatore 5 V / 3 A candidato con rilevamento corrente Type-C. Buck separato per LTE, linea 3,3 V per ESP/display, linea 5 V per audio. USB dati con rilevamento VBUS e isolamento per prevenire alimentazioni incrociate e ritorno di corrente. |
| Scocca | Pareti non metallizzate, spazio dedicato all'antenna LTE e zona liberata attorno all'antenna Wi-Fi. Nessuna batteria nel progetto corrente. |

## Pin proposti

| Segnale | GPIO ESP32-S3 |
|---|---|
| LCD DIN / CLK / CS / DC / RST | 11 / 12 / 10 / 9 / 8 |
| LCD retroilluminazione | 7, dopo verifica elettrica |
| USB D− / D+ | 19 / 20 |
| Amplificatore I²S BCLK / LRCLK / DOUT | 4 / 5 / 6 |
| UART LTE TX MCU / RX MCU | 15 / 16 |
| UART LTE RTS MCU / CTS MCU | 1 / 2 |
| Modem PWRKEY / RESET | 17 / 18, attraverso pilotaggio idoneo e con temporizzazioni da datasheet |

Verificare la variante esatta del modulo e il livello UART del modem. Progettare traslazione bidirezionale per i versi UART, alimentazione e protezione ESD della SIM secondo reference design del modem. Portare l'uscita audio direttamente ai due morsetti dello speaker: il carico è flottante. Separare il percorso RF a impedenza controllata da clock I²S e ramo speaker.

## Decisioni prima del PCB

- Collegare il modem su scheda di valutazione per misurare transitori TX, registrazione in rete, bande supportate e APN reale. Dimensionare rail, condensatori ed eventuale protezione dalle sovracorrenti su quelle misure.
- Provare scheda audio MAX98357A e speaker nel volume di carico. Verificare intelligibilità, ronzii LTE e stabilità mentre modem e speaker lavorano insieme.
- Confermare Wi-Fi come connessione preferita e LTE come riserva. Implementare modem AT/PPP o trasporto equivalente con backoff, verifica di connettività e limite traffico. Esporre lo stato nel pannello.
- Separare configurazione locale e voce. Il backend TTS con TLS restituisce audio PCM o un formato decodificabile. L'ESP riproduce via I²S e sincronizza visemi o animazione della bocca. Valutare il servizio, latenza e consumo dati prima della scelta finale.
- Acquisire disegno e misure reali di display, SIM, speaker e antenne. Chiudere il CAD meccanico e collaudare la portata radio anche con la calotta montata. Per il prodotto UE completare le verifiche radio ed EMC applicabili.

## Riferimenti

- [Quectel EG915U](https://www.quectel.com/product/lte-cat-1-bis-eg915u-series/)
- [Quectel EG915U hardware design](https://images.quectel.com/python/sites/2/2023/05/Quectel_EG915U_Series_QuecOpen_Hardware_Design_V1.0.pdf)
- [Analog Devices MAX98357A](https://www.analog.com/en/products/max98357a.html)
- [Waveshare 15867](https://www.waveshare.com/1.3inch-LCD-Module.htm)
- [Web Serial in Chrome](https://developer.chrome.com/docs/capabilities/serial)
