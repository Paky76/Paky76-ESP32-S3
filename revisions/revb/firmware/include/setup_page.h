#pragma once
static const char SETUP_PAGE[] PROGMEM = R"PAKYHTML(<!doctype html>
<html lang="it">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Configura Paky76</title>
<style>
:root{color-scheme:light;font:16px system-ui;color:#162c30;background:#f4f1e9}*{box-sizing:border-box}body{margin:0}
main{max-width:740px;margin:auto;padding:24px}header{display:flex;align-items:center;gap:16px;margin:10px 0 24px}
.mark{width:54px;height:50px;display:grid;place-items:center;color:#96eee1;background:#173b3b;border-radius:16px;font-size:25px}
h1,h2,p{margin:0}h1{font-size:1.8rem}h2{font-size:1.15rem;margin-bottom:12px}header p,small{color:#486367}
section{background:#fffdf8;border:1px solid #dedfd2;border-radius:18px;padding:20px;margin-bottom:14px}
label{display:block;font-weight:650;margin:10px 0 6px}input,select,button{font:inherit}input:not([type=checkbox]),select{width:100%;padding:10px;border:1px solid #a8b8b2;border-radius:9px;background:#fff}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:12px}button,.link{border:0;border-radius:9px;color:white;background:#175954;padding:10px 14px;display:inline-block;text-decoration:none;font-weight:650;cursor:pointer}
button:disabled{opacity:.46;cursor:default}.secondary{background:#47605e}.actions{display:flex;flex-wrap:wrap;gap:8px;margin:12px 0}#notice{min-height:1.5em;color:#335a54}#notice.error{color:#943626}
dl{display:grid;grid-template-columns:120px 1fr;gap:7px;margin:10px 0 0}dd{margin:0;overflow-wrap:anywhere}dt{color:#486367}
@media(max-width:520px){main{padding:14px}.grid{grid-template-columns:1fr}}
</style>
</head>
<body>
<main>
<header><div class="mark" aria-hidden="true">••</div><div><h1>Configura Paky76</h1><p>Prima accensione e connessione locale</p></div></header>
<section>
<h2>Collegamento al dispositivo</h2>
<div class="actions"><button type="button" id="usb">Collega USB</button><button type="button" id="reopen" class="secondary" hidden>Riattiva Wi‑Fi iniziale</button><button type="button" id="refresh" class="secondary">Aggiorna stato</button></div>
<form id="openip" class="actions"><input id="ip" aria-label="Indirizzo IP locale" placeholder="IP locale di Paky76" inputmode="decimal" style="max-width:210px"><button class="secondary">Apri via Wi‑Fi</button></form>
<dl><dt>Dispositivo</dt><dd id="device">In attesa</dd><dt>Collegamento</dt><dd id="transport">Nessuno</dd><dt>IP Wi‑Fi</dt><dd id="address">—</dd><dt>Wi‑Fi iniziale</dt><dd id="ap">—</dd><dt>Cellulare</dt><dd id="lte">—</dd></dl>
</section>
<form id="settings">
<section><h2>Wi‑Fi</h2>
<div class="grid"><div><label for="ssid">Nome rete (SSID)</label><input id="ssid" maxlength="32" placeholder="Facoltativo" autocomplete="off"></div>
<div><label for="password">Password Wi‑Fi</label><input id="password" type="password" maxlength="63" autocomplete="new-password"><small>Vuota per mantenere la password della rete già configurata.</small></div></div>
<label><input id="open" type="checkbox"> La rete Wi‑Fi è aperta</label>
</section>
<section><h2>SIM e voce</h2><div class="grid">
<div><label for="apn">APN operatore</label><input id="apn" maxlength="63" autocomplete="off" placeholder="Facoltativo"><small>Salvato per il modem LTE della Rev.B.</small></div>
<div><label for="volume">Volume preferito</label><input id="volume" type="range" min="0" max="100" value="45"><output id="volumeout" for="volume">45%</output><br><small>Usato per il tono di prova e salvato per il motore vocale.</small></div>
</div><div class="actions"><button type="button" id="tone" class="secondary" disabled>Prova altoparlante</button></div></section>
<button id="save" disabled>Salva impostazioni</button>
<p id="notice" role="status" aria-live="polite"></p>
</form>
<section>
<h2>Parla con Paky76</h2>
<form id="basic"><label for="aimode">Modalità</label><select id="aimode"><option value="basic">Comandi offline</option><option id="onlinechoice" value="gateway" disabled>Modello via gateway HTTPS</option></select>
<label for="prompt">Messaggio</label><input id="prompt" maxlength="160" required placeholder="Per esempio: chi sei?">
<div class="actions"><button id="ask" disabled>Chiedi a Paky76</button></div></form>
<p id="answer" aria-live="polite"></p>
</section>
<section>
<h2>Aggiornamento firmware</h2>
<p id="firmwareVersion">Versione in attesa</p>
<form id="otaupload">
<label for="otafile">Pacchetto firmware firmato</label>
<input type="file" id="otafile" accept=".pakyota" required disabled>
<div class="actions"><button id="otainstall" disabled>Installa dalla dashboard</button></div>
</form>
<label><input id="otaauto" type="checkbox" disabled> Installa automaticamente gli aggiornamenti online</label>
<p id="otanote" aria-live="polite"></p>
</section>
</main>
<script>
"use strict";
const el=id=>document.getElementById(id);
const onDevice=location.pathname==="/setup";
let port, reader, writer, pending, mode=onDevice?"wifi":null;
const enc=new TextEncoder(), dec=new TextDecoder();
function notice(message,error=false){el("notice").textContent=message;el("notice").classList.toggle("error",error);}
function request(cmd,fields={}){
 if(mode==="wifi")return fetch("/api/config",{method:"POST",headers:{"Content-Type":"application/json","X-Paky-Setup":"1"},cache:"no-store",body:JSON.stringify({cmd,...fields})}).then(async res=>{
  if(!res.ok)throw Error("Dashboard irraggiungibile o credenziali errate");
  return res.json();
 });
 if(!writer||mode!=="usb")return Promise.reject(Error("Collega prima un dispositivo."));
 if(pending)return Promise.reject(Error("Attendi la risposta del dispositivo."));
 return new Promise((resolve,reject)=>{
  const timer=setTimeout(()=>{pending=null;reject(Error("Nessuna risposta via USB."));},4500);
  pending={resolve:value=>{clearTimeout(timer);resolve(value);},reject:error=>{clearTimeout(timer);reject(error);}};
  writer.write(enc.encode(JSON.stringify({cmd,...fields})+"\n")).catch(error=>{
   if(pending){pending.reject(error);pending=null;}
  });
 });
}
async function readSerial(){
 let line="";
 try{
  for(;;){
   const {value,done}=await reader.read();if(done)break;
   line+=dec.decode(value,{stream:true});
   if(line.length>8192)line="";
   for(let i=line.indexOf("\n");i>=0;i=line.indexOf("\n")){
    const frame=line.slice(0,i);line=line.slice(i+1);
    try{const result=JSON.parse(frame);if(pending&&result.paky===1){const p=pending;pending=null;p.resolve(result);}}catch{}
   }
  }
 }finally{
  if(pending){pending.reject(Error("USB scollegata."));pending=null;}
  reader.releaseLock();writer.releaseLock();await port.close().catch(()=>{});
  reader=writer=port=null;mode=onDevice?"wifi":null;
  el("usb").textContent="Collega USB";el("save").disabled=!onDevice;el("tone").disabled=!onDevice;el("ask").disabled=!onDevice;el("reopen").hidden=true;
 }
}
function show(s){
 if(!s.ok)throw Error(s.error||"Errore del dispositivo");
 el("device").textContent=s.name||"Paky76";el("transport").textContent=mode==="usb"?"USB":"Wi‑Fi";
 el("address").textContent=s.ip||"Non connesso";el("ssid").value=s.ssid||"";
 el("ap").textContent=(s.ap ? s.ap+(s.apIp?" · "+s.apIp:""):"Disattivo")+(s.setupKey?" · codice "+s.setupKey:"");
 el("lte").textContent=s.lte||"Non disponibile";el("apn").value=s.apn||"";
 el("open").checked=!!s.open;if(s.ip)el("ip").value=s.ip;
 el("volume").value=s.volume??45;el("volumeout").textContent=el("volume").value+"%";
 el("save").disabled=false;el("tone").disabled=false;el("ask").disabled=false;el("reopen").hidden=mode!=="usb";el("onlinechoice").disabled=!s.aiReady;
 el("firmwareVersion").textContent=s.fwVersion ? "Versione "+s.fwVersion : "Versione in attesa";
 el("otafile").disabled=el("otainstall").disabled=!(onDevice&&s.otaLocal);
 el("otaauto").disabled=!s.otaOnline;el("otaauto").checked=!!s.otaAuto;
}
async function refresh(){show(await request("status"));}
el("usb").onclick=async()=>{
 try{
  if(port){await reader.cancel();return;}
  if(!navigator.serial)throw Error("Per USB apri questa pagina su localhost con un browser desktop compatibile con Web Serial.");
  const selected=await navigator.serial.requestPort();await selected.open({baudRate:115200});port=selected;
  reader=port.readable.getReader();writer=port.writable.getWriter();mode="usb";
  readSerial().catch(e=>notice(e.message,true));el("usb").textContent="Scollega USB";
  await refresh();notice("Dispositivo collegato.");
 }catch(e){notice(e.message,true);}
};
el("refresh").onclick=()=>refresh().then(()=>notice("Stato aggiornato.")).catch(e=>notice(e.message,true));
el("reopen").onclick=()=>request("ap").then(show).then(()=>notice("Wi-Fi iniziale attivo.")).catch(e=>notice(e.message,true));
el("tone").onclick=()=>request("tone",{volume:Number(el("volume").value)}).then(s=>{
 if(!s.ok)throw Error(s.error);notice("Tono di prova inviato allo speaker.");
}).catch(e=>notice(e.message,true));
el("openip").onsubmit=e=>{
 e.preventDefault();
 const ip=el("ip").value.trim(), a=ip.split(".");
 if(a.length!==4||a.some(v=>!/^\d{1,3}$/.test(v)||Number(v)>255)||
    !(Number(a[0])===10||(Number(a[0])===192&&Number(a[1])===168)||(Number(a[0])===172&&Number(a[1])>=16&&Number(a[1])<=31))){
  notice("Inserisci un indirizzo IPv4 privato, per esempio 192.168.1.24.",true);return;
 }
 location.href="http://"+a.map(Number).join(".")+"/setup";
};
el("volume").oninput=()=>el("volumeout").textContent=el("volume").value+"%";
el("settings").onsubmit=async e=>{
 e.preventDefault();el("save").disabled=true;
 try{show(await request("save",{ssid:el("ssid").value,password:el("password").value,open:el("open").checked,apn:el("apn").value.trim(),volume:Number(el("volume").value)}));
 el("password").value="";notice("Impostazioni salvate. Attendi la connessione, poi aggiorna lo stato per leggere il nuovo IP.");
 }catch(e){notice(e.message,true);}finally{el("save").disabled=false;}
};
el("aimode").onchange=()=>{el("prompt").maxLength=el("aimode").value==="gateway"?300:160;};
el("basic").onsubmit=async e=>{
 e.preventDefault();
 try{
  el("ask").disabled=true;
  const online=el("aimode").value==="gateway";
  let s=await request(online?"ask_ai":"ask_basic",{prompt:el("prompt").value});
  if(!s.ok)throw Error(s.error);
  if(online){
   const id=s.id;
   el("answer").textContent="Richiesta al modello in corso…";
   for(let j=0;s.pending&&j<95;j++){
    await new Promise(resolve=>setTimeout(resolve,500));
    s=await request("ai_result",{id});
    if(!s.ok)throw Error(s.error);
   }
   if(s.pending)throw Error("Tempo di attesa superato.");
   if(s.aiError)throw Error(s.aiError);
  }
  el("answer").textContent=s.text;
 }catch(error){el("answer").textContent=error.message;}finally{el("ask").disabled=!(mode==="wifi"||mode==="usb");}
};
el("otaupload").onsubmit=async e=>{
 e.preventDefault();
 const file=el("otafile").files[0];
 if(!onDevice||!file)return;
 el("otainstall").disabled=true;
 el("otanote").textContent="Caricamento in corso. Mantieni collegata l'alimentazione.";
 try{
  const form=new FormData();form.append("firmware",file);
  const r=await fetch("/api/ota",{method:"POST",headers:{"X-Paky-Setup":"1"},body:form});
  const message=await r.text();
  if(!r.ok)throw Error(message||"Aggiornamento rifiutato.");
  el("otanote").textContent=message;
 }catch(error){el("otanote").textContent=error.message;el("otainstall").disabled=false;}
};
el("otaauto").onchange=async()=>{
 const setting=el("otaauto"), enabled=setting.checked;
 setting.disabled=true;
 try{
  const s=await request("ota_auto",{enabled});
  if(!s.ok)throw Error(s.error);
  setting.checked=s.otaAuto;
  el("otanote").textContent=enabled?"Aggiornamenti online attivati.":"Aggiornamenti online disattivati.";
 }catch(error){setting.checked=!enabled;el("otanote").textContent=error.message;}
 finally{setting.disabled=false;}
};
if(onDevice)refresh().catch(e=>notice(e.message,true));
else notice("Collega Paky76 via USB oppure apri l’indirizzo IP che compare sul display.");
</script>
</body>
</html>
)PAKYHTML";
