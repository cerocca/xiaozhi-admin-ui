# Xiaozhi Admin UI

Admin UI minimale per gestire e osservare un server Xiaozhi ESP32 — vedi [Requisiti](#requisiti) — in ambiente LAN.  
Per installazione completa e guida passo-passo vedi [`SETUP.md`](SETUP.md).

---

## Cosa fa

- Dashboard con stato servizi:
  - LLM
  - ASR
  - TTS
  - device (connected / disconnected)

- Integrazione health runtime reale del backend tramite `/api/health`

- Configurazione:
  - LLM
  - ASR
  - TTS

- Visualizzazione moduli read-only:
  - VAD
  - Intent
  - Memory

- Accesso ai log (backend e Piper)

- Azioni operative:
  - restart
  - logs

Obiettivo:
- debug reale
- semplicità
- zero overengineering

---

## Quick start

```bash
git clone https://github.com/cerocca/xiaozhi-admin-ui.git
cd xiaozhi-admin-ui

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
```

Modifica almeno:

```env
XIAOZHI_DIR=...
XIAOZHI_CONFIG=...
```

Avvia:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8088
```

Apri:

```text
http://<SERVER_IP>:8088
```

---

## Requisiti

- backend Xiaozhi compatibile già funzionante  
  (es. [xiaozhi-esp32-lightserver](https://github.com/cerocca/xiaozhi-esp32-lightserver) oppure [xiaozhi-esp32-server](https://github.com/xinnan-tech/xiaozhi-esp32-server))

- accesso locale a:
  - repository backend
  - file di configurazione

- Docker (per backend)
- Piper opzionale

**Nota:**  
la UI è stata sviluppata e testata principalmente con `xiaozhi-esp32-lightserver`.  
Altri backend compatibili con `/api/health` dovrebbero funzionare, ma non sono garantiti.

---

## Documenti del repo

- `SETUP.md` → installazione completa da zero (consigliato)
- `ARCHITECTURE.md` → struttura del progetto e componenti
- `PROJECT_RULES.md` → linee guida e vincoli
- `CHANGELOG.md` → versioni e modifiche

---

## Stato progetto

- `v0.1.x` → stabile e utilizzabile
- `v0.2.0` → in sviluppo (focus su UX e health clarity)

---

## Filosofia

- Server-rendered (no SPA)
- No JavaScript complesso
- Debug reale > UI decorativa
- Patch incrementali, no refactor massivi
