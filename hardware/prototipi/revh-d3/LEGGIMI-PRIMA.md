# Paky76 Rev.H / D3 — Ordine prototipo

La scheda principale ha contorno rettangolare finito di 83,25 × 70,00 mm ed è a quattro strati. L'estensione di 28 mm è sul lato USB, così l'antenna sporge ancora di 6 mm dal bordo opposto. J1 è sul nuovo bordo; J9 microSD, portapila e gli altri componenti conservano la loro posizione rispetto al retro. Il pannello 34 × 34 mm è quello Rev.G, con cinque ALPS C115351.

| Scheda | Quota finita | Lato di assemblaggio | File |
| --- | --- | --- | --- |
| Principale Rev.H | 83,25 × 70 mm | Top + Bottom | Gerber Rev.H + BOM/CPL Rev.H |
| Pannello comandi | 34 × 34 mm | Top | Gerber e CPL pannello Rev.G, BOM ALPS |

JLCPCB: Standard PCBA sulla principale, quattro strati, Top + Bottom. Per BT1 montato dal fornitore usa la coppia in Completa. Se il montaggio di BT1 sul fondo viene rifiutato, usa BT1-Manuale. Entrambe le varianti includono J9. PCBWay: Turnkey Both sides sulla principale e Top side sul pannello. I Gerber della singola scheda vanno caricati con i relativi CSV.

La misura 83,25 × 70 mm è quella del PCB finito e supera o eguaglia il minimo dimensionale Standard pubblicato. Il produttore può aggiungere guide di lavorazione o fiduciali oltre il contorno. Verificare la quota finale nel CAM e chiedere la consegna senza guide. Testo per il produttore:

> Please confirm the finished individual main PCB measures 83.25 × 70.00 mm per the supplied Rev.H Gerber. If tooling rails are needed for assembly, please remove them before shipping. Please confirm bottom-side assembly of J9 and BT1, component availability, and any fees before production.

La scocca D3 è lunga 85,1 mm in profondità, 101 mm in larghezza e 104 mm in altezza. Il frontale, i tasti, il display e la disposizione della griglia derivano dalla D2.1. I binari di supporto e l'accesso laterale alla microSD sono stati spostati o allungati per il nuovo PCB. Vedi Scocca-D3/MONTAGGIO-D3.md.

DRC, ERC e parità schema/PCB superati. Il passaggio USB-C e le aperture sono stati verificati sul modello CAD. Entrambe le piste dati USB sono state allungate di 28 mm; il primo campione deve verificare enumerazione, trasferimento dati, caduta su VBUS sotto carico e tenuta meccanica dei connettori. Restano da confermare CAM, disponibilità, collaudo fisico e funzionalità applicative.
