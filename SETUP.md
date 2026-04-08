# SETUP — Xiaozhi Admin UI

## Obiettivo
Installare e validare `xiaozhi-admin-ui` senza ambiguita sul setup reale oggi supportato.

Questa guida assume:
- deploy Linux host-native
- backend reale `xiaozhi-esp32-lightserver`
- config reale in `data/.config.yaml`
- Admin UI servita via `uvicorn` o systemd

## 0. Assunzioni esplicite
Valori di riferimento correnti:
- utente Linux: `ciru`
- IP LAN server: `192.168.1.69`
- Admin UI: `/home/ciru/xiaozhi-admin-ui`
- backend Xiaozhi: `/home/ciru/xiaozhi-esp32-lightserver`
- config Xiaozhi: `/home/ciru/xiaozhi-esp32-lightserver/data/.config.yaml`
- Piper service: `piper-api`
- Piper health URL: `http://127.0.0.1:8091/health`

Se il tuo ambiente usa path o IP diversi, adatta `.env` e gli script wrapper prima di andare in produzione.

## 1. Preflight
Verifiche minime:

```bash
python3 --version
docker --version
docker compose version
systemctl status piper-api --no-pager
curl -s http://127.0.0.1:8091/health ; echo
ls -l /home/ciru/xiaozhi-esp32-lightserver/data/.config.yaml
cd /home/ciru/xiaozhi-esp32-lightserver
docker compose ps
```

Atteso:
- Python disponibile
- Docker Compose operativo
- `piper-api` attivo
- health Piper HTTP valido
- file config esistente e scrivibile dall'utente che esegue la UI
- backend Xiaozhi presente e avviabile via `docker compose`

## 2. Path vincolanti
La config corretta e:

```text
/home/ciru/xiaozhi-esp32-lightserver/data/.config.yaml
```

La UI legge e scrive quel file. Se il path e sbagliato:
- l'editor puo modificare il file errato
- backup e rollback diventano fuorvianti
- la pagina LLM puo mostrare dati non coerenti col runtime reale

## 3. Struttura progetto attesa

```text
/home/ciru/xiaozhi-admin-ui
├── .env
├── .venv/
├── requirements.txt
├── app/
│   ├── main.py
│   ├── config.py
│   ├── routers/
│   ├── services/
│   ├── templates/
│   └── static/
├── data/
│   └── backups/
│       └── config/
└── scripts/
```

Questa guida e post-clone: il codice deve gia essere presente.

## 4. Virtualenv e dipendenze

```bash
cd /home/ciru/xiaozhi-admin-ui
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -c "import fastapi, jinja2, yaml, httpx; print('deps ok')"
```

## 5. `.env` di riferimento

File:

```text
/home/ciru/xiaozhi-admin-ui/.env
```

Contenuto di riferimento:

```env
ADMIN_UI_HOST=192.168.1.69
ADMIN_UI_PORT=8088

XIAOZHI_DIR=/home/ciru/xiaozhi-esp32-lightserver
XIAOZHI_CONFIG=/home/ciru/xiaozhi-esp32-lightserver/data/.config.yaml

PIPER_HEALTH_URL=http://127.0.0.1:8091/health
PIPER_SYSTEMD_SERVICE=piper-api

LAN_CIDR=192.168.1.0/24
```

Note operative:
- `app/config.py` usa questi stessi default
- alcuni script wrapper puntano ancora direttamente a `/home/ciru/xiaozhi-admin-ui` e `/home/ciru/xiaozhi-esp32-lightserver`
- se cambi directory di deploy, aggiorna anche gli script in `scripts/`

## 6. Smoke test applicativo

```bash
cd /home/ciru/xiaozhi-admin-ui
source .venv/bin/activate
python -c "import app.main; print('import ok')"
uvicorn app.main:app --host 192.168.1.69 --port 8088
```

Apri poi:

```text
http://192.168.1.69:8088
```

Verifiche minime:
- `/`
- `/config`
- `/backups`
- `/logs`
- `/devices`
- `/llm`

## 7. Verifica pagina LLM
La pagina `/llm` oggi implementa il multi-provider Livello 1.

Controlli minimi:
- i profili vengono letti dalle chiavi sotto `LLM`
- il profilo attivo e coerente con `runtime.llm_profile`
- se `selected_module.llm` esiste, viene mantenuto come compatibilita legacy
- creare o modificare un profilo non deve alterare gli altri blocchi `LLM`
- attivare un profilo non deve cambiare altro oltre ai riferimenti attivi

## 8. systemd essenziale
Esempio minimale:

```ini
[Unit]
Description=Xiaozhi Admin UI
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=ciru
Group=ciru
WorkingDirectory=/home/ciru/xiaozhi-admin-ui
EnvironmentFile=/home/ciru/xiaozhi-admin-ui/.env
ExecStart=/home/ciru/xiaozhi-admin-ui/.venv/bin/uvicorn app.main:app --host 192.168.1.69 --port 8088
Restart=always
RestartSec=3
StandardOutput=journal
StandardError=journal
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=full
ProtectHome=false
ReadWritePaths=/home/ciru/xiaozhi-admin-ui /home/ciru/xiaozhi-esp32-lightserver/data

[Install]
WantedBy=multi-user.target
```

Abilitazione:

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now xiaozhi-admin-ui
sudo systemctl status xiaozhi-admin-ui --no-pager -l
journalctl -u xiaozhi-admin-ui -f
```

## 9. Post-install checklist
- import applicativo OK
- dashboard raggiungibile
- config editor legge il file reale
- save config crea backup
- rollback funziona
- restart Xiaozhi e Piper rispondono
- log viewer mostra output
- `/llm` vede il profilo attivo corretto

## 10. Errori comuni
- `No module named 'app'`: stai lanciando `uvicorn` fuori dalla root progetto
- file config non leggibile: permessi sbagliati su `/home/ciru/xiaozhi-esp32-lightserver/data/.config.yaml`
- restart Xiaozhi fallito: path o permessi errati nel wrapper `scripts/xserver.sh`
- pagina LLM incoerente: stai leggendo una config diversa da quella usata dal backend

## 11. Limiti intenzionali
Questa guida non introduce:
- nuove dipendenze
- nuovo modello YAML
- automazioni LLM di Livello 2
- refactor dei path hardcoded oltre il minimo necessario
