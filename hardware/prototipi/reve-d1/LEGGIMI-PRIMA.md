# Paky76 Rev.E / D1 — RTC con batteria tampone

La Rev.E integra U5 (Micro Crystal RV-3028-C7) e BT1 (Keystone 500, portapila passante sul lato inferiore). Alloggia una sola CR1220 da 3 V, da inserire a mano a scheda assemblata. SDA GPIO21, SCL GPIO47, pull-up 4,7 kΩ a 3,3 V. Il condensatore C7 da 10 nF disaccoppia VDD e VBACKUP riceve esclusivamente la tensione della pila. La CR1220 è una pila primaria. La ricarica del RTC deve restare disattivata.

Al primo avvio con alimentazione principale configurare nel RTC la commutazione di backup, disattiva di fabbrica. Verificare rileggendo i registri e provare la ritenzione dell'ora al ritorno del 5 V senza rete. Il collaudo è fisico e rimane da eseguire. Il portapila è sotto la scheda; rimuovere il frontale ed estrarre la PCB per accedere alla pila. Confermare sul campione ingombro, isolamento e accesso prima di chiudere la scocca D1.

## File JLCPCB

- Gerber-RevE-DFM.zip, BOM-JLCPCB-RevE.csv, CPL-JLCPCB-RevE.csv. Sorgenti e report in questo pacchetto.
- Richiedere Standard PCBA e pannellizzazione per la scheda da 66 × 42 mm. BT1 è l'unico componente sul lato inferiore ed è passante. Il CPL indica per BT1 il centro della sede circolare e la rotazione nominale KiCad. Il gestore CAM deve confermare posizione, lato, polarità e fattibilità di assemblaggio passante lato inferiore. Se il fornitore omette BT1, installarlo a mano dopo l'assemblaggio.
- Verificare disponibilità U5 C2829066 e BT1 C238121: risultavano a stock pubblico zero nelle pagine JLCPCB consultate. Richiedere approvvigionamento o accettazione di componenti a consignment. La pila si acquista a parte.
- Confermare anche il piazzamento del modulo U1 e il trattamento del pad termico. ERC, DRC e confronto schema/PCB sono verifiche dei file. L'accettazione CAM e il collaudo del campione sono da completare.

La Rev.E copre il circuito RTC. La microSD resta un modulo cablato. Pannello a cinque tasti, LED RGB e interruttore generale restano nelle specifiche D1 da integrare. Gli STL D1 sono inclusi per la prova meccanica.
