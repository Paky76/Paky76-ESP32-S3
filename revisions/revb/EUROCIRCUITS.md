# Paky76 Rev.B · Preparazione Eurocircuits

**Stato: banco prova e preparazione DFM. La Rev.B integrata è ancora da completare.**

## Banco prova

Lo schema nativo [Paky76-RevB-bench.kicad_sch](hardware/Paky76-RevB-bench.kicad_sch) aggiunge i segnali audio e modem al nucleo ESP32-S3/display/USB. Questo è lo schema del collegamento a moduli di valutazione. KiCad 9.0.2 ha rilevato **zero errori e zero avvisi ERC**.

| Interfaccia logica | Collegamenti nello schema, in ordine |
|---|---|
| J3 audio I²S | GND, GPIO4 BCLK, GPIO5 LRCLK, GPIO6 DOUT |
| J4 modem EVB | GND, GPIO15 TX MCU, GPIO16 RX MCU, GPIO1 RTS MCU, GPIO2 CTS MCU, GPIO17 PWRKEY, GPIO18 RESET, NC |

Usare moduli di valutazione alimentati secondo le rispettive specifiche, con massa comune e interfaccia a livelli verificati. J3 e J4 espongono soltanto logica e massa. Verificare il livello UART e la direzione dei segnali sulla variante specifica del modem. PWRKEY e RESET richiedono lo stadio di pilotaggio del reference design. La misura sul banco deve accertare la stabilità del rail del modem durante trasmissione LTE e quella del percorso audio a volume elevato. Il firmware corrente supporta la configurazione e il tono audio. La sessione dati LTE e il parlato restano da integrare.

## Generazione del pacchetto di revisione DFM

Servono i sorgenti nativi **Rev.B** con basename `hardware/Paky76-RevB` per schema, PCB e progetto KiCad, più `hardware/bom-revb-pcba.csv` con intestazioni `Reference,MPN,Description` ed eventuale `SPN`. Includere la popolazione del PCB per il PCBA e gestire display, speaker, antenne e cablaggi esterni nell'integrazione meccanica.

Dopo aver concordato la configurazione a quattro strati, esempio di comando dalla directory Rev.B:

```sh
python3 checks/eurocircuits_package.py --copper-layers 4 --output Paky76-RevB-Eurocircuits-DFM.zip
```

L'esportazione verifica ERC, DRC, parità schema–PCB e corrispondenza dei riferimenti fra BOM e CPL, poi produce Gerber, forature PTH/NPTH separate e report. È stata verificata in un'area temporanea con i file Rev.A come dati di prova e con i sorgenti Rev.B mancanti, che causano un arresto senza ZIP. I risultati Rev.A non costituiscono verifica della Rev.B.

## Revisione nel portale

1. In **PCB Visualizer**, controllare contorno, layer, forature, stack-up, accoppiamento differenziale USB e via sotto le piazzole termiche. Sottoporre la soluzione RF e la finitura dei via pad a DFM una volta completato il layout.
2. In **PCBA Visualizer**, caricare e associare BOM e CPL. Verificare MPN e stock, confermare faccia, polarità, rotazione e orientamento pin 1, valutare eventuale saldatura di connettori PTH e chiedere riscontro su LGA/QFN.
3. Dopo il DFM, utilizzare la revisione approvata per un lotto pilota. Il rilascio in produzione richiede gli esiti documentati del [piano di preproduzione](PREPRODUZIONE.md).

- [Portale Eurocircuits](https://be.eurocircuits.com)
- [Eurocircuits BOM e CPL](https://www.eurocircuits.com/technical-guidelines/pcb-assembly-guidelines/bom-cpl-data/)
- [Eurocircuits formati PCB](https://www.eurocircuits.com/technical-guidelines/pcb-design-guidelines/input-data-formats/)
- [Eurocircuits riempimento via](https://www.eurocircuits.com/technical-guidelines/pcb-design-guidelines/via-filling/)
