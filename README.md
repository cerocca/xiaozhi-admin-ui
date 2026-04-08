# Xiaozhi Admin UI

## Scopo
`xiaozhi-admin-ui` e una Web UI FastAPI/Jinja2 per amministrare in LAN un'istanza gia funzionante di `xiaozhi-esp32-lightserver`, senza introdurre coupling forte con il runtime audio.

Serve oggi a:
- vedere lo stato del backend Xiaozhi, di Piper e del file config
- leggere e modificare `data/.config.yaml`
- creare backup automatici prima dei salvataggi e fare rollback
- riavviare Xiaozhi e Piper in modo esplicito
- leggere log Xiaozhi e Piper
- ricavare una vista device dai log recenti
- gestire il multi-provider LLM di Livello 1 tramite profili sotto `LLM`

## Stato reale del progetto
Lo stato funzionale non e piu il solo MVP iniziale.

Gia presenti:
- dashboard operativa
- config editor con validazione YAML minima
- backup config + restore
- pagine log e device
- pagina LLM multi-provider Livello 1
- compatibilita con setup LAN reale via systemd + wrapper scripts

Non ancora in scope:
- refactor massivi del modello YAML
- orchestrazione LLM avanzata, fallback o routing automatico
- UI guidata completa per ASR e TTS
- persistenza device in database
- autenticazione applicativa obbligatoria

## LLM multi-provider: regola attuale
La UI supporta piu profili LLM contemporaneamente dentro `LLM`.

- `runtime.llm_profile` e la source of truth del profilo attivo
- `selected_module.llm` resta supportato come compatibilita legacy
- `profile_name` = nome della chiave sotto `LLM`
- `provider_id` = preset UI usato per proporre `type`, `base_url`, `model` e validazioni minime

Esempio concettuale:
- `provider_id`: `openai`
- `profile_name`: `openai_fast`

Questo e Livello 1: piu profili coexistono, uno e attivo alla volta.

## Architettura in una riga
Browser LAN -> FastAPI Admin UI -> service layer -> wrapper scripts -> Docker Compose / systemd / file YAML

## Requisiti operativi
- host Linux
- backend `xiaozhi-esp32-lightserver` gia presente e funzionante
- Piper API gia presente e funzionante
- Python 3 installato
- Docker + Docker Compose funzionanti
- permessi coerenti per leggere/scrivere la config Xiaozhi

## Path di riferimento correnti
Path di deploy previsti dal codice attuale:
- Admin UI: `/home/ciru/xiaozhi-admin-ui`
- Backend Xiaozhi: `/home/ciru/xiaozhi-esp32-lightserver`
- Config Xiaozhi: `/home/ciru/xiaozhi-esp32-lightserver/data/.config.yaml`
- Backup Admin UI: `/home/ciru/xiaozhi-admin-ui/data/backups/config`
- Piper systemd service: `piper-api`
- URL UI: `http://192.168.1.69:8088`

Nota:
- in sviluppo il repository puo stare altrove
- in runtime gli script e alcuni path applicativi sono ancora allineati al deploy `/home/ciru/...`

## Documenti utili
- `SETUP.md`: installazione e validazione operativa
- `ARCHITECTURE.md`: confini architetturali, LLM Livello 1 e punti legacy
- `PROJECT_RULES.md`: regole di modifica del progetto
