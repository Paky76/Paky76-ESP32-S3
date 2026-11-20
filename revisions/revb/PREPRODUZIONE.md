# Rev.B · Stato e verifiche prima della produzione

**Stato: progetto di ingegneria. Produzione Rev.B bloccata.**

| Verifica | Evidenza richiesta | Stato iniziale |
|---|---|---|
| Dashboard via USB e Wi-Fi | Test Node su stato, salvataggio, cambio di trasporto, hotspot, tono e gestione IP locale | Superata in simulazione |
| Studio volumetrico | Compilazione OpenSCAD e controllo del sorgente | Superata la generazione del modello CSG |
| Build firmware | Log PlatformIO per l'ambiente ESP32-S3 Rev.B | Eseguita dal workflow Rev.B |
| Schema, PCB, ERC, DRC, parità | Sorgenti KiCad Rev.B completi e report rigenerati sulla stessa revisione | In sospeso. PCB elettrico Rev.B da progettare |
| BOM e assemblaggio | MPN e impronte verificati, disponibilità, Gerber, forature, posizionamenti e DFM del fornitore | In sospeso |
| Alimentazione | Verificare avvio, transitori LTE con audio attivo, minimi delle linee di alimentazione, temperatura, limiti della sorgente USB-C e assenza di alimentazione inversa | In sospeso |
| Porte e configurazione | USB in entrambi i versi, setup su hardware, persistenza dopo riavvio, riattivazione hotspot, errori di rete e LAN | In sospeso |
| LTE e SIM | Registrazione con SIM reale, fallback Wi-Fi → LTE, ritorno al Wi-Fi, HTTPS, perdita rete, traffico e antenna in scocca | In sospeso |
| Voce e display | Parlato italiano, volume, intelligibilità, assenza di ronzii durante trasmissione, leggibilità, animazione | In sospeso |
| Scocca, RF ed EMC | Montaggio e accesso a porte, SIM e pulsanti, cablaggi, tenuta dei fissaggi, prestazioni radio in scocca e accertamenti EMC applicabili | In sospeso |
| Lotto pilota e autorizzazione | Evidenze su unità del pilota, correzioni verificate e approvazione tecnica esplicita per lo stesso commit | In sospeso |

La CI Rev.B verifica la dashboard simulata, la generazione del modello CSG e la compilazione firmware. Il binario risultante è per il banco. I Gerber Rev.A e il controllo di produzione Rev.A appartengono a una revisione diversa.

## Sequenza di rilascio

1. Portare display, audio e modem su banco con alimentazione controllata per acquisire correnti di picco, livelli logici e misure meccaniche.
2. Chiudere schema, layout e distinta della Rev.B. Eseguire ERC e DRC con parità schema–PCB, poi la revisione RF, meccanica e DFM sul medesimo commit.
3. Commissionare il lotto pilota dopo approvazione tecnica, registrando per ogni esemplare versione hardware, firmware, esito, strumenti, condizioni di prova e misure.
4. Autorizzare la produzione dopo collaudi superati, chiusura dei difetti e approvazione esplicita della revisione fabbricabile.
