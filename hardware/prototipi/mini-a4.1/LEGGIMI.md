# Paky76 Mini A4.1 — Primo prototipo, file per preventivo JLCPCB

 
Per vedere S1, i due tasti e tutti i connettori insieme, aprire `Cablaggio/Schema-interconnessioni.svg`. Il documento `Cablaggio/Componenti-e-controlli.md` riporta la distinta di sistema e la corrispondenza dei pin.
## Documentazione PDF

- [Manuale di assemblaggio](Documentazione/Paky76-Mini-A4.1-Manuale-Assemblaggio.pdf)
- [Schemi di collegamento](Documentazione/Paky76-Mini-A4.1-Schemi-Collegamento.pdf)
- [Datasheet tecnico](Documentazione/Paky76-Mini-A4.1-Datasheet.pdf)

## Schede e interruttore

La principale A4 integra il modulo Seeed XIAO ESP32-S3 come U1 SMD (113991114, JLCPCB C20467913). Include USB-C, programmazione e caricatore LiPo 1S. La principale è a due strati, il frontale è A1. L’interruttore resta cablato nel guscio. Per l’ordine usare la cartella Principale A4, che sostituisce la precedente carrier con due file di fori. U1 è nella BOM e nel CPL. Il PCB espone BAT-SW su J2, pin 1 VBAT e pin 2 GND. J2 sono due piazzole metallizzate per il cablaggio manuale.

## Preventivo JLCPCB

| Cartella | Contorno | Strati | PCBA |
| --- | --- | ---: | --- |
| JLCPCB/Principale | 32 × 39 mm | 2 | Economic, componenti lato Top, quattro riferimenti |
| JLCPCB/Frontale | 43 × 42 mm | 2 | Economic, componenti lato Top, quattro riferimenti |

Per ciascuna scheda caricare lo ZIP Gerber del relativo gruppo, poi BOM e CPL nella pagina PCB Assembly. Specifica iniziale 1,6 mm, FR-4, rame esterno 1 oz. Selezionare la quantità minima di PCBA proposta dal configuratore per il primo prototipo. Verificare i contorni, i codici e la disponibilità per la quantità scelta, il pin 1 dei JST e il verso degli attuatori di SW1/SW2. Guardando il lato componenti, gli attuatori devono puntare verso i bordi laterali opposti. Approvare il CAM solo dopo aver confrontato la vista JLCPCB con KiCad. La consegna include due set distinti. Verificare U1 in anteprima: USB-C verso il bordo corto sul lato y=80,50 mm in KiCad. Verificare con JLCPCB la disponibilità del modulo, il servizio di assemblaggio compatibile e la saldatura delle due piazzole batteria sotto U1. Confermare il profilo di montaggio a rifusione e la corrispondenza del modulo effettivo con i pad della libreria Seeed, prima di procedere con il primo campione.

## Interruttore laterale ON/OFF

Componente previsto: **Nidec Components MFS201N-Z**, doppio deviatore a slitta non-shorting, 1 A a 30 V DC su carico resistivo. Montare sul fianco sinistro, con flangia esterna e attuatore accessibile. La flangia è lunga 23,2 mm. Il taglio riportato nel disegno del costruttore è 9,5 × 5 mm e i due fori Ø 2,5 mm hanno interasse 19 mm. Stampare prima `Meccanica/switch_gauge.stl` al 100%, nello stesso materiale del guscio. Verificare montaggio, corsa e lunghezza delle viti M2 in base al pezzo reale. Il datasheet riporta un carico minimo di riferimento di 5 V / 10 mA: verificare continuità e stabilità anche alla tensione reale della LiPo, nel carico previsto e durante l’uso dopo periodi di inattività.

Cablaggio: tagliare soltanto il positivo del cavetto intermedio, con cella e USB scollegate. Collegare il positivo proveniente dalla batteria al comune 2 di un polo e l’uscita verso J2 pin 1 VBAT a uno dei contatti esterni 1 o 3, scelto dopo aver identificato ON col multimetro. Lasciare libero l’altro contatto. Il negativo della batteria prosegue direttamente a J2 pin 2 GND. Confermare piedini e polarità sul pezzo reale poiché i terminali non sono numerati. Isolare singolarmente le saldature, bloccare il cavetto contro la trazione e tenere viti, lamiera e terminali lontani dalla cella. Applicare le indicazioni ON e OFF dopo aver verificato la posizione al banco.

| USB-C | Cursore | Comportamento atteso |
| --- | --- | --- |
| Scollegata | OFF | XIAO spenta, batteria isolata sul positivo |
| Scollegata | ON | Funzionamento a batteria |
| Collegata | OFF | XIAO alimentabile da USB, batteria scollegata e ricarica disattivata |
| Collegata | ON | Alimentazione USB e ricarica secondo lo stato della batteria e del caricatore XIAO |

**Per caricare mettere il cursore su ON.** Per spegnere completamente, portarlo su OFF e scollegare USB-C. Questa è una commutazione sulla sola batteria. La ricarica in OFF richiederebbe una diversa architettura di alimentazione.

### Collaudo fisico del comando

1. A circuito scollegato, misurare continuità in ON e circuito aperto in OFF sul filo positivo. Verificare continuità del negativo e assenza di corto tra positivo e negativo in entrambe le posizioni.
2. Ripetere le quattro combinazioni della tabella e verificare con lo strumento l’andamento della corrente batteria. In ON verificare caduta di tensione, stabilità ai cicli di accensione e reset. In OFF con USB collegata verificare che non circoli corrente di carica.
3. Provare la corsa con guscio serrato, l’accesso USB, la tenuta della flangia e l’assenza di interferenze. Usare inizialmente la dima della cella, quindi isolare il percorso dei conduttori e verificare nuovamente con la cella reale. Verificare la temperatura in carica in scocca.

## Materiale da procurare per ogni dispositivo

- 1 antenna 2,4 GHz compatibile con la XIAO, se il modulo assemblato non è accompagnato da antenna. U1 va ordinato nella PCBA della principale.
- 1 interruttore Nidec MFS201N-Z e 2 viti M2 a lunghezza adeguata alla flangia.
- 1 LiPo protetta 1S da 350 mAh con fine carica 4,2 V. Riferimento dimensionale Adafruit 2750, 36 × 19,6 × 5,2 mm. Confermare polarità e compatibilità con il caricatore della revisione di XIAO ricevuta. Acquistare una controparte a cavo compatibile con il connettore della batteria.
- 1 OLED SH1106 128×64 a 3,3 V configurato I²C, più cablaggio. Il modulo di riferimento per l'ingombro è Waveshare 10451, 40,5 × 37,5 mm. Su quello specifico modulo verificare gli strap per I²C, l'indirizzo, lo stato di CS/D-C e la gestione del reset secondo istruzioni Waveshare. Il suo connettore a sette pin richiede un cablaggio adattato e può incidere sull'altezza. Prima dell'ordine verificare il montaggio e l'accesso a viti e cavi con il modulo previsto.
- 1 cavo JST SH a sei vie passo 1,0 mm tra le due schede. Verificare la continuità pin 1→1 fino a 6→6 con il multimetro.
- 1 cavetto JST SH a quattro vie lato frontale da adattare all'OLED, 8 viti M2 di lunghezza selezionata in base alle sedi e un anello portachiavi. Stampare prima la scocca di prova.

## Montaggio e collaudo

1. Stampare il guscio e la cornice al 100% in Cura e usare le dime. Ingombro di prova 48 × 47 × 30 mm, escluso l'occhiello. Verificare apertura USB con il cavo reale, allineamento dei tasti, altezza OLED, antenna, cablaggi, spazio per il modulo e sede della cella. Il modello è una prova di ingombro. Attuatori, fissaggio display e ritenzione cella richiedono verifica meccanica. Tenere la cella separata da componenti, saldature, viti e spigoli. Per la prova di montaggio usare la dima, senza installare la cella.
2. Preparare il cablaggio ON/OFF a batterie e USB scollegate. Saldare il positivo dopo interruttore su J2 pin 1 e il negativo su J2 pin 2 della principale. Verificare la polarità prima del collegamento e bloccare meccanicamente il cavetto. Sul primo campione misurare tensione su VBAT e continuità di GND prima della prova di carica, poi verificare l’antenna e l’allineamento USB con il guscio.
3. Accendere inizialmente con USB e senza batteria. Verificare enumerazione, tensione sui pin J1 del frontale e assorbimento anomalo. Collegare il frontale e successivamente l'OLED. J1 pin 1–6: GND, 3V3, SDA GPIO5, SCL GPIO6, LEFT_N GPIO2, RIGHT_N GPIO1. J2 frontale pin 1–4: GND, 3V3, SDA, SCL. Un pulsante premuto deve portare a massa la relativa linea. I pull-up I²C sono 4,7 kΩ sulla principale, misurare la resistenza effettiva se presenti anche sul display.
4. Caricare lo sketch con target Seeed Studio XIAO ESP32S3. Lo sketch di collaudo prova il display SH1106, i due comandi, il lampeggio degli occhi e lo spegnimento del display dopo inattività. Verifica di sintassi C++ eseguita con interfacce simulate. Compilazione nel core Arduino ESP32 e prova su scheda restano da fare. Il firmware non abilita il Wi-Fi e il timer spegne solo il display. Il cursore interrompe l’alimentazione a batteria come descritto sotto.
5. Collegare la cella dopo le misure USB e applicare la matrice di collaudo dell’interruttore. Verificare corrente di carica reale e tensione finale con strumentazione, comportamento a batteria e con USB inserita o rimossa, temperatura e autonomia. Ripetere a batteria parzialmente scarica. Controllare l'assenza di riavvii e che la corrente rimanga entro i limiti della cella. La 350 mAh di riferimento documenta 525 mA continui. Conservare Wi-Fi disabilitato per il primo collaudo e qualificare eventuali picchi radio sulla batteria prima di abilitarlo. La ricarica della XIAO è integrata, priva di sensore di temperatura esterno su questa carrier. Usare solo il pacco qualificato, entro le temperature definite dal suo produttore, e validare la carica in scocca prima dell'uso regolare.
6. Solo dopo aver verificato il prototipo, consolidare la scocca e il cablaggio e autorizzare un lotto.

## Verifiche eseguite

- Sorgenti KiCad 9, ERC e DRC con parità schema/PCB per entrambe le schede. Zero violazioni e zero connessioni mancanti.
- Verifiche locali dei contorni Gerber, numero dei fori PTH/NPTH, riferimenti e montaggio su un lato. STL verificati come mesh chiuse. U1 usa le castellazioni e i due pad batteria inferiori. Le aperture paste si verificano nell’anteprima di assemblaggio.
- Il CAM del configuratore JLCPCB, lo stock del preventivo, le prove elettriche, di ricarica e di montaggio richiedono verifica. Nessun invio di ordine o pagamento.

## Riferimenti

- Nidec MFS201N-Z: https://www.nidec-components.com/e/catalog/switch/mfs.pdf
- Footprint Seeed di riferimento: https://github.com/Seeed-Studio/OPL_Kicad_Library/blob/master/Seeed%20Studio%20XIAO%20Series%20Library/XIAO-ESP32-S3-SMD.kicad_mod
- Catalogo JLCPCB U1: https://jlcpcb.com/partdetail/SEEED_TECHNOLOGY_CO_LTD-113991114/C20467913
- Seeed XIAO ESP32-S3: https://wiki.seeedstudio.com/xiao_esp32s3_getting_started/
- Schema Seeed revisione 1.3: https://files.seeedstudio.com/wiki/SeeedStudio-XIAO-ESP32S3/res/XIAO_ESP32S3_V1.3_SCH_260115.pdf
- Batteria: https://www.adafruit.com/product/2750
- Display: https://www.waveshare.com/wiki/1.3inch_OLED_(B)
- JLCPCB PCBA: https://jlcpcb.com/capabilities/pcb-assembly-capabilities
- Simboli e footprint KiCad: https://www.kicad.org/libraries/license/
