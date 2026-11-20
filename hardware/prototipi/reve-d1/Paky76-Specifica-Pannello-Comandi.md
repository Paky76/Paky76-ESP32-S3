# Paky76 — Pannello comandi e interruttore

Specifica per la prossima revisione della PCB e della scocca. Riferimento di base: Paky76 Rev.D. Schema, layout e file PCBA della Rev.D non incorporano queste aggiunte.

## Comandi sul frontale

Disporre cinque pulsanti tattili normalmente aperti su una piccola PCB frontale, con quattro direzioni a croce e OK al centro. Posizionare il LED RGB accanto al display. Scegliere posizione, passo tra i pulsanti e altezza degli attuatori sulla scocca definitiva. Tenere RESET e BOOT accessibili sul fianco o sul retro, con attuatori incassati per evitare pressioni involontarie.

| Tasto | Funzione nel menu |
| --- | --- |
| ↑ e ↓ | Scorrere le voci o cambiare il valore selezionato |
| ← | Tornare alla schermata precedente |
| → | Aprire un sottomenu o spostarsi tra i campi |
| OK | Aprire il menu dalla schermata principale e confermare la selezione |

Voci iniziali: rete, volume, luminosità, data e ora, fotocamera e microSD. Usare debounce software e mostrare gli errori a display. Le modifiche confermate vanno salvate prima di mostrare la conferma.

## Collegamento elettrico

Usare un connettore polarizzato a 4 poli tra la scheda principale e il frontale, con pin assegnati nell'ordine 1 = 3,3 V, 2 = GND, 3 = SDA, 4 = SCL. Bus I²C iniziale a 100 kHz su SDA GPIO21 e SCL GPIO47, gli stessi previsti per il RTC. Dimensionare una sola coppia di pull-up sul ramo 3,3 V principale. Usare cablaggio corto e verificare fronti e margini di tensione con il pannello collegato.

Espansore proposto TCA9534 a 3,3 V. A0/A1/A2 a GND, indirizzo I²C a 7 bit 0x20. Disaccoppiamento 100 nF vicino al componente. Leggere i cinque tasti tramite polling. Installare pull-up esterni sugli ingressi P0–P4 e collegare ogni pulsante tra ingresso e GND.

| I/O | Funzione |
| --- | --- |
| P0–P4 | Su, giù, sinistra, destra, OK |
| P5–P7 | Rosso, verde, blu |

Usare un LED RGB ad anodo comune a 3,3 V e una resistenza distinta per ogni colore, dimensionata dalla tensione diretta e dalle specifiche di corrente dell'espansore. Puntare inizialmente a pochi mA per canale, verificando luminosità e limiti cumulativi. Inizializzare il registro di uscita a livello alto prima di abilitare P5–P7 come uscite. Colori di base: verde = rete connessa, blu lampeggiante = connessione in corso, ambra = modalità offline, rosso = errore. Il firmware può combinare i colori e temporizzare i lampeggi. Se serve attenuazione fluida, usare un driver LED PWM dedicato.

SW1 RESET conserva il collegamento a ESP_EN. SW2 BOOT conserva ESP_BOOT su GPIO0. Il RESET hardware riavvia l'ESP32. Per programmare tenere BOOT durante il rilascio del RESET.

## Interruttore generale

Prevedere un interruttore meccanico ON/OFF sulla linea positiva a 5 V, a monte della diramazione verso scheda, amplificatore e convertitore 3,3 V di camera/microSD. L'interruttore va montato sulla scocca con connessione al cablaggio di alimentazione. La portata DC deve superare la corrente massima e considerare l'inrush dei rami a valle. Tenere comune la massa. Con USB di servizio collegata, prevedere isolamento o selezione dell'alimentazione per evitare rialimentazione attraverso VBUS. La pila RTC alimenta il solo orologio mentre l'interruttore è su OFF.

## Verifica prima del rilascio

Verificare ingombri e corsa dei tasti, stabilità I²C con RTC e frontale, cinque comandi nel menu, LED nei quattro stati, modalità BOOT/RESET e assenza di alimentazione residua sui rami spenti. Verificare anche il comportamento dopo interruzione durante una scrittura su microSD, prevedendo espulsione software prima dello spegnimento ordinario. Restano da disegnare e verificare in KiCad PCB principale e frontale, connettori, selezione USB/alimentatore, cablaggio e frontale stampabile.
