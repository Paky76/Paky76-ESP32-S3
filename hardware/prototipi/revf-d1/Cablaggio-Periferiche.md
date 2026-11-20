# Paky76 Rev.F — una videocamera e microSD

La Rev.F assegna il secondo chip select di J7 alla microSD. J7 collega una sola camera SPI e un lettore microSD SPI rimovibile, entrambi fissati nella scocca e collegati con un cablaggio. Il lettore è un modulo esterno alla scheda principale. Microfono J6, display, speaker e LTE restano disponibili. U1 è N16R8 con 16 MB di flash e 8 MB di PSRAM.

## J7 — cablaggio a due rami

| Pin | GPIO | Camera SPI | microSD SPI |
| --- | --- | --- | --- |
| 1 | — | GND | VSS |
| 2 | 38 | SCK | CLK |
| 3 | 39 | MOSI | CMD / DI |
| 4 | 40 | MISO | DAT0 / DO |
| 5 | 41 | CS | — |
| 6 | 42 | — | DAT3 / CS |

Camera candidata: Arducam Mega SPI, con segnali a 3,3 V e uscita MISO in alta impedenza a CS alto da verificare sul modulo reale. Lettore candidato: SparkFun BOB-00544, socket nativo a 3,3 V; integrare nel cablaggio i pull-up da 10 kΩ verso 3,3 V per CMD e DAT0–DAT3 dove assenti, compresi DAT1/DAT2. Tenere CS camera alto a riposo/avvio con pull-up se assente sul modulo. Usare cavi corti e massa comune. J7 non porta VCC. Alimentare camera e microSD con un ramo 3,3 V regolato separato dal 3,3 V della Rev.F, comune ai due moduli, con disaccoppiamento vicino ai carichi e sufficiente per i loro picchi; non alimentare il lettore a 5 V. Il lettore e la camera devono essere alimentati prima di pilotare il bus. J7 non è un connettore MIPI o DVP.

Microfono J6: 1 = 3,3 V, 2 = GND, 3 = BCLK GPIO4, 4 = LRCLK GPIO5, 5 = DOUT del microfono verso GPIO14. Esempio: breakout I²S SPH0645 con SEL a GND. L'amplificatore condivide BCLK/LRCLK e riceve i dati da GPIO6.

## Firmware e file

Avviare il bus SPI e mantenere CS camera alto. Montare la microSD in modalità SDSPI prima della prima transazione con la camera. Se il montaggio fallisce con la scheda inserita, non avviare la camera sullo stesso bus finché la condizione non è risolta. Usare i due dispositivi in transazioni serializzate, e avviare il collaudo a velocità ridotta. Per il primo prototipo usare una microSD da 16–32 GB formattata FAT32. Percorsi suggeriti: /sdcard/models/, /sdcard/audio/ e /sdcard/capture/. Collaudare la camera e la lettura SD prima singolarmente e poi assieme.

La microSD conserva pesi, vocabolari, audio e dati. Il firmware può leggerli a blocchi se il runtime del modello lo supporta. La microSD non aumenta la PSRAM o la potenza di calcolo dell’ESP32. Un LLM conversazionale utilizzabile sulla scheda non è incluso o validato. Il primo obiettivo offline resta un modello compatto per comandi vocali o classificazione visiva.

