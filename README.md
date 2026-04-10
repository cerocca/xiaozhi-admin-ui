# Xiaozhi Admin UI

`xiaozhi-admin-ui` e una Web UI server-rendered per amministrare un'istanza esistente di `xiaozhi-esp32-lightserver`.

Stack attuale:
- FastAPI
- Jinja templates
- CSS semplice
- rendering server-side
- target LAN-first

## Cosa fa
- mostra una dashboard operativa con stato servizi e azioni rapide
- distingue tra stato config e stato runtime
- legge e modifica il file YAML reale del backend
- crea backup config prima dei salvataggi e permette restore
- mostra log backend e log Piper
- espone una vista device derivata dal runtime
- gestisce profili `LLM`, `ASR` e `TTS`
- mostra moduli read-only come `VAD`, `Intent` e `Memory`
- integra la health runtime del backend tramite `/api/health`

## Cosa non fa
- non sostituisce il backend `xiaozhi-esp32-lightserver`
- non esegue il runtime audio
- non e una SPA
- non richiede una pipeline frontend separata
- non introduce polling continuo lato UI
- non implementa autenticazione applicativa obbligatoria
- non orchestra routing o fallback LLM avanzati

## Integrazione con il backend
La UI e separata dal backend.

Interagisce con:
- il file config reale del backend
- i wrapper script locali in `scripts/`
- `docker compose` per il backend Xiaozhi
- `systemctl` e `journalctl` per Piper
- l'endpoint runtime `/api/health` esposto dal backend

La UI non modifica immagini Docker, compose file o codice del backend.

## Dipendenze
Dipendenze operative minime:
- Linux
- Python 3.11 o compatibile con il progetto
- virtualenv
- backend `xiaozhi-esp32-lightserver` gia presente
- accesso in lettura e scrittura al file config del backend
- Docker e Docker Compose per la gestione del backend
- systemd per la gestione del servizio Piper

Dipendenze Python:
- FastAPI
- Uvicorn
- Jinja2
- PyYAML
- httpx

Vedi `requirements.txt`.

## Pagine principali
- `/`: dashboard operativa
- `/ai`: indice AI Stack
- `/llm`: CRUD profili LLM
- `/asr`: CRUD profili ASR
- `/tts`: CRUD profili TTS
- `/vad`: vista read-only
- `/intent`: vista read-only
- `/memory`: vista read-only
- `/config`: editor config YAML
- `/backups`: storico backup e restore
- `/logs`: log backend e Piper
- `/devices`: vista device runtime

## Avvio rapido
Happy path su Linux server standard:

```bash
git clone <REPO_URL> /home/xiaozhi/xiaozhi-admin-ui
cd /home/xiaozhi/xiaozhi-admin-ui
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --host 0.0.0.0 --port 8088
```

Prima di avviare, modifica in `.env` almeno:
- `XIAOZHI_DIR`
- `XIAOZHI_CONFIG`

Nota:
- l'esempio usa `/home/xiaozhi/...`, ma `XIAOZHI_DIR` va sempre verificato sul server reale
- `scripts/xserver.sh` mantiene un fallback interno per compatibilita, ma non va considerato un valore universale

Apri poi la UI:

```text
http://<SERVER_IP>:8088
```

Per una guida completa, copy-paste friendly e con verifica finale vedi `SETUP.md`.

## Configurazione
Da verificare sempre:
- `XIAOZHI_DIR`
- `XIAOZHI_CONFIG`
- il path deve corrispondere al backend reale presente sulla macchina

Da modificare se il setup lo richiede:
- `ADMIN_UI_HOST`
- `ADMIN_UI_PORT`
- `BACKEND_HOST`
- `BACKEND_HEALTH_PORT`
- `PIPER_SERVICE_NAME`

Opzionale, con default gia sensati:
- `XSERVER_SCRIPT_PATH`
- `PIPER_SCRIPT_PATH`
- `XSERVER_SERVICE_NAME`
- `PIPER_HEALTH_URL`
- `LAN_CIDR`

I default gia funzionanti coprono il caso comune:
- script wrapper sotto `scripts/`
- Piper health su `http://127.0.0.1:8091/health`
- LAN `192.168.1.0/24`
- `XSERVER_SCRIPT_PATH` usa lo script del repo corrente
- `scripts/xserver.sh` mantiene anche un fallback interno di compatibilita per `XIAOZHI_DIR`, ma per un nuovo setup e meglio impostarlo esplicitamente in `.env`

## Verifica rapida
Installazione ok se:
- la UI risponde su `http://<SERVER_IP>:<ADMIN_UI_PORT>`
- `curl -s http://127.0.0.1:<BACKEND_HEALTH_PORT>/api/health` risponde dal server UI
- la dashboard si apre senza errori bloccanti
- stato `device disconnected` senza device connessi non e un errore

## Documenti del repo
- `SETUP.md`: installazione da zero, systemd, troubleshooting
- `ARCHITECTURE.md`: confini architetturali e flussi principali
- `PROJECT_RULES.md`: regole di progetto e scelte operative
- `CHANGELOG.md`: modifiche rilevanti della UI
