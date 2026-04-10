# ARCHITECTURE

## 1. Ruolo della Admin UI
`xiaozhi-admin-ui` e un pannello operativo separato dal backend `xiaozhi-esp32-lightserver`.

Scopo:
- osservare lo stato del sistema
- leggere e modificare la config reale
- mostrare runtime health
- eseguire azioni operative semplici
- facilitare debug e manutenzione in LAN

Non fa parte del runtime audio.
Non sostituisce il backend.

## 2. Separazione tra UI e backend
La separazione e intenzionale.

La UI:
- gira come applicazione FastAPI host-side
- renderizza HTML lato server
- usa wrapper script locali
- legge e scrive il file config del backend

Il backend:
- resta un progetto separato
- espone runtime health via `/api/health`
- continua a gestire il runtime reale

Questa separazione serve a evitare coupling forte tra interfaccia amministrativa e runtime.

## 3. Vista d'insieme

```text
Browser LAN
    ->
xiaozhi-admin-ui
    ->
service layer
    ->
wrapper scripts + file config + endpoint HTTP
    |-- docker compose per xiaozhi-esp32-lightserver
    |-- systemctl e journalctl per Piper
    |-- file YAML reale del backend
    `-- /api/health del backend
```

## 4. Stack tecnico
- FastAPI
- Jinja templates
- CSS semplice
- server-rendered
- nessuna SPA
- nessun build frontend
- nessun database applicativo

## 5. Pagine principali
- `/`: dashboard operativa
- `/ai`: vista AI Stack
- `/llm`: CRUD LLM
- `/asr`: CRUD ASR
- `/tts`: CRUD TTS
- `/vad`: modulo read-only
- `/intent`: modulo read-only
- `/memory`: modulo read-only
- `/config`: editor YAML
- `/backups`: backup e restore
- `/logs`: log backend e Piper
- `/devices`: stato device derivato dal runtime

## 6. Flussi principali
### Dashboard operativa
Mostra:
- stato backend
- stato Piper
- stato file config
- accessi rapidi a restart, stop e log

### Config editor
Flusso:
1. lettura del file YAML reale
2. modifica lato UI
3. validazione minima YAML
4. backup preventivo
5. scrittura atomica
6. verifica post-write

### Backup e restore
Flusso:
1. elenco backup disponibili
2. scelta backup
3. restore sul file config reale
4. verifica post-write

### AI Stack
La pagina `/ai` unisce:
- stato di configurazione dei moduli
- stato runtime letto dal backend
- accesso alle pagine di dettaglio `LLM`, `ASR`, `TTS`
- moduli read-only come `VAD`, `Intent`, `Memory`

### Logs
La pagina `/logs` e on-demand:
- nessuno streaming continuo complesso
- refresh esplicito
- tail numerico

### Devices
La pagina `/devices` e runtime-oriented e log-derived:
- nessun database
- nessuna persistenza dedicata
- precisione limitata alle informazioni disponibili

## 7. Config vs runtime
Questa distinzione e centrale nel progetto.

Config:
- rappresenta quello che e scritto nella configurazione del backend
- viene letto e modificato tramite file YAML
- e persistente

Runtime:
- rappresenta quello che il backend sta usando davvero in quel momento
- viene osservato tramite `/api/health`
- puo divergere dalla config se il backend non e stato riavviato o se il runtime e degradato

La UI espone entrambe le viste per aiutare il debug reale.

## 8. Integrazione `/api/health`
La UI interroga il backend Xiaozhi tramite `/api/health` per leggere almeno:
- stato `llm`
- stato `asr`
- stato `tts`
- stato `device`

Uso pratico:
- arricchisce la dashboard AI
- distingue cio che e configurato da cio che e realmente in esecuzione
- evita di assumere che config corretta significhi runtime sano

Limite attuale:
- l'URL del backend health e configurabile via `.env`, ma va comunque verificato in caso di deploy su host o porte diversi
- per un deploy su un altro server va verificato e, se necessario, aggiornato nel codice

## 9. Moduli AI
### LLM
Supporta CRUD di profili `LLM`.

Regole attuali:
- possono esistere piu profili contemporaneamente
- un solo profilo e attivo alla volta
- `runtime.llm_profile` e la source of truth principale
- `selected_module.llm` resta supportato come compatibilita legacy

### ASR
Supporta CRUD di profili `ASR` con distinzione tra profilo selezionato e profilo attivo.

### TTS
Supporta CRUD di profili `TTS`, inclusi campi operativi come endpoint, model e voice.

### Moduli read-only
`VAD`, `Intent` e `Memory` sono esposti come viste di consultazione, non come editor completi.

## 10. Limiti intenzionali
Scelte volute del progetto:
- niente SPA
- niente frontend complesso
- niente polling continuo
- niente orchestrazione automatica avanzata
- niente refactor massivi del modello YAML
- niente database applicativo

Questi limiti servono a mantenere la UI semplice, leggibile e utile per debug operativo reale.

## 11. Limiti pratici attuali
Limiti da conoscere leggendo il repo oggi:
- alcuni path sono ancora assoluti
- alcuni wrapper si aspettano un deploy locale vicino al backend
- la UI non e pensata come pannello remoto universale
- alcune compatibilita legacy restano per non rompere setup gia funzionanti
