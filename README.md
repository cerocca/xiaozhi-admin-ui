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
Esempio generico:

```bash
git clone <REPO_URL> /home/<user>/xiaozhi-admin-ui
cd /home/<user>/xiaozhi-admin-ui
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port <ADMIN_UI_PORT>
```

Apri poi:

```text
http://<SERVER_IP>:<ADMIN_UI_PORT>
```

Per una guida completa e replicabile vedi `SETUP.md`.

## Limiti reali da conoscere
Il repository non e ancora completamente indipendente dall'host.

Valori configurabili via `.env`:
- host e porta UI
- path backend Xiaozhi
- path file config
- health URL di Piper
- nome servizio systemd di Piper

Valori ancora hardcoded nel codice o negli script:
- path di alcuni wrapper script
- directory backend usata da `scripts/xserver.sh`
- URL backend usato per `/api/health`
- alcuni default in `app/config.py`

Questo significa che un deploy su un altro server e possibile, ma oggi va fatto seguendo la sezione "Adattamenti obbligatori" in `SETUP.md`.

## Documenti del repo
- `SETUP.md`: installazione da zero, systemd, troubleshooting
- `ARCHITECTURE.md`: confini architetturali e flussi principali
- `PROJECT_RULES.md`: regole di progetto e scelte operative
- `CHANGELOG.md`: modifiche rilevanti della UI
