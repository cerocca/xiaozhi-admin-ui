# Architecture — Xiaozhi Admin UI

## Ruolo
`xiaozhi-admin-ui` e un pannello di management host-side per `xiaozhi-esp32-lightserver`.

Responsabilita attuali:
- osservare stato servizi e config
- modificare il file YAML reale
- creare backup e rollback
- lanciare restart espliciti
- leggere log
- offrire una gestione LLM multi-provider di Livello 1

Non partecipa al runtime audio e non sostituisce il backend Xiaozhi.

## Principio architetturale
Separare sempre:
- runtime Xiaozhi
- tooling admin

Questo mantiene basso il rischio operativo e rende il debug piu leggibile.

## Posizionamento nel sistema

```text
Browser LAN
    ->
xiaozhi-admin-ui (FastAPI, host-native, systemd)
    ->
service layer
    ->
wrapper scripts / file access
    |-- docker compose (xiaozhi-esp32-lightserver)
    |-- systemctl / journalctl (piper-api)
    `-- /home/ciru/xiaozhi-esp32-lightserver/data/.config.yaml
```

## Componenti principali

### Web application
Stack:
- FastAPI
- Jinja2
- CSS custom minimale
- nessuna SPA
- nessun build frontend

Router reali:
- `/`
- `/config`
- `/backups`
- `/logs`
- `/devices`
- `/llm`
- `/actions/*`

### Service layer
`app/services/status_service.py`
- stato backend Xiaozhi via `docker compose ps`
- stato Piper via `systemctl` + health HTTP
- stato file config

`app/services/config_service.py`
- read config
- validazione YAML minima
- backup
- scrittura atomica
- verifica post-write
- rollback

`app/services/log_service.py`
- log Xiaozhi via wrapper `xserver.sh`
- log Piper via wrapper `piper.sh`

`app/services/device_service.py`
- ricostruzione device log-derived

`app/services/llm_service.py`
- lettura profili sotto `LLM`
- risoluzione profilo attivo
- CRUD minimo dei profili
- aggiornamento riferimento attivo
- compatibilita con entry legacy

`app/services/command_service.py`
- esecuzione wrapper scripts con timeout e risultato strutturato

### Template layer
Template principali:
- `dashboard.html`
- `config_editor.html`
- `backups.html`
- `logs.html`
- `devices.html`
- `llm.html`
- `action_result.html`

Scelta intenzionale:
- rendering server-side
- comportamento semplice
- nessuna pipeline frontend separata

## Integrazione con backend e host

### Backend Xiaozhi
Il backend resta separato e containerizzato.

La UI interagisce con:
- `docker compose ps`
- `docker compose restart`
- `docker compose logs`
- `data/.config.yaml`

Non modifica immagini, compose file o codice runtime del backend.

### Piper
`piper-api` resta un servizio host-native.

La UI usa:
- `systemctl`
- `journalctl`
- health check HTTP locale

### Wrapper scripts
La UI non esegue shell arbitraria.
Usa soltanto:
- `scripts/admin-ui.sh`
- `scripts/xserver.sh`
- `scripts/piper.sh`

## Gestione configurazione

### Save config
UI -> validazione YAML -> backup -> write atomico -> verifica post-write

### Rollback
UI -> scelta backup -> restore -> verifica post-write

Scelta voluta:
- restart separato dal save
- operazioni esplicite
- minor rischio di side-effect

## LLM multi-provider

### Livello 1: gia implementato
La sezione `LLM` puo contenere piu profili.
Ogni profilo e una chiave YAML indipendente.

Concetti da tenere distinti:
- `profile_name`: nome del profilo, cioe la chiave sotto `LLM`
- `provider_id`: preset UI usato per dedurre/validare campi noti del provider

Esempio:
- `profile_name = openai_fast`
- `provider_id = openai`

Regola attuale del profilo attivo:
1. `runtime.llm_profile` e la source of truth
2. `selected_module.llm` resta letto e aggiornato come compatibilita legacy
3. se mancano entrambi, il service prova a risolvere un profilo esistente in `LLM`

Compatibilita legacy ancora supportata:
- endpoint legacy `/llm/save`
- endpoint legacy `/llm/save-and-restart`
- campo YAML `selected_module.llm`

Questi punti legacy esistono per non rompere setup gia in uso, non per guidare l'evoluzione futura.

### Livello 2: volutamente rimandato
Fuori scope per ora:
- routing automatico tra provider
- fallback intelligente
- UI guidata completa per capability/provider/model
- validazione forte dell'intero modello YAML
- normalizzazione strutturale del blocco `LLM`

## Devices e log
La pagina `/devices` resta log-derived:
- nessun DB
- nessuna migrazione
- accuratezza limitata ai log recenti

La pagina `/logs` resta on-demand:
- tail numerico
- refresh esplicito
- niente stream realtime complesso

## Persistenza
Persistenza minima attuale:
- config Xiaozhi reale
- backup config in `/home/ciru/xiaozhi-admin-ui/data/backups/config`

Nessun database applicativo.

## Sicurezza
Scelte attuali:
- LAN only
- bind su IP LAN
- nessuna auth applicativa obbligatoria
- niente shell libera dalla UI
- permessi minimi per leggere/scrivere config e usare i wrapper
