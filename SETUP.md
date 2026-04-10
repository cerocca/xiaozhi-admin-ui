# SETUP

Questa guida copre il percorso piu semplice per installare `xiaozhi-admin-ui` da zero su un server Linux standard, con configurazione esplicita e pochi passaggi manuali.

## 1. Prerequisiti
Serve gia avere:

1. Linux con accesso shell.
2. `git`.
3. Python 3 con modulo `venv`.
4. backend `xiaozhi-esp32-lightserver` gia presente sulla stessa macchina.
5. file config reale del backend gia esistente.
6. Docker e Docker Compose funzionanti per il backend.
7. Piper gia installato se vuoi usare le azioni e i log Piper.

Verifica rapida:

```bash
python3 --version
git --version
docker --version
docker compose version
```

## 2. Preflight backend
Prima di installare la UI, conferma che il backend locale sia davvero raggiungibile:

```bash
ls -ld /home/xiaozhi/xiaozhi-esp32-lightserver
ls -l /home/xiaozhi/xiaozhi-esp32-lightserver/data/.config.yaml
cd /home/xiaozhi/xiaozhi-esp32-lightserver
docker compose ps
curl -s http://127.0.0.1:8003/api/health
```

Se usi Piper sulla stessa macchina:

```bash
systemctl status piper-api --no-pager
curl -s http://127.0.0.1:8091/health
```

## 3. Installazione da zero
Clone del repository:

```bash
git clone <REPO_URL> /home/xiaozhi/xiaozhi-admin-ui
cd /home/xiaozhi/xiaozhi-admin-ui
```

Crea il virtualenv e installa le dipendenze:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -c "import fastapi, jinja2, yaml, httpx; print('deps ok')"
```

Se vedi `deps ok`, la base Python e pronta.

## 4. Configurazione `.env`
Copia il file di esempio:

```bash
cp .env.example .env
```

Apri `.env` e modifica almeno queste variabili:

```env
ADMIN_UI_HOST=0.0.0.0
ADMIN_UI_PORT=8088
BACKEND_HOST=127.0.0.1
BACKEND_HEALTH_PORT=8003
XIAOZHI_DIR=/home/xiaozhi/xiaozhi-esp32-lightserver
XIAOZHI_CONFIG=/home/xiaozhi/xiaozhi-esp32-lightserver/data/.config.yaml
PIPER_SERVICE_NAME=piper-api
```

Controlla in particolare:
- `XIAOZHI_DIR` deve puntare alla directory reale del backend sulla macchina dove gira la UI
- `XIAOZHI_CONFIG` deve puntare al file config reale del backend
- gli esempi in questa guida usano `/home/xiaozhi/...`, ma sono solo un happy path documentato
- `scripts/xserver.sh` mantiene un fallback interno per compatibilita, ma per un nuovo setup non conviene affidarsi a quel fallback

## 5. Configurazione: cosa verificare davvero
Da verificare sempre:
- `XIAOZHI_DIR`
- `XIAOZHI_CONFIG`
- devono corrispondere ai path reali del backend presente sulla macchina

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

Default gia funzionanti se non li imposti:
- `XSERVER_SCRIPT_PATH` e `PIPER_SCRIPT_PATH` puntano agli script nella directory del repo corrente
- `PIPER_HEALTH_URL` usa `http://127.0.0.1:8091/health`
- `LAN_CIDR` usa `192.168.1.0/24`
- `XSERVER_SERVICE_NAME` ha default `xiaozhi-server`
- `scripts/xserver.sh` mantiene un fallback interno per `XIAOZHI_DIR` per compatibilita, ma per un nuovo host e meglio impostare `XIAOZHI_DIR` in `.env`

Note pratiche:
- `ADMIN_UI_HOST=0.0.0.0` e il valore piu semplice per esporre la UI in LAN
- `BACKEND_HOST` e `BACKEND_HEALTH_PORT` devono puntare all'endpoint che espone `/api/health`
- `XIAOZHI_CONFIG` deve essere scrivibile dall'utente che esegue la UI

## 6. Avvio manuale

```bash
cd /home/xiaozhi/xiaozhi-admin-ui
source .venv/bin/activate
python -c "import app.main; print('import ok')"
uvicorn app.main:app --host 0.0.0.0 --port 8088
```

Apri nel browser:

```text
http://<SERVER_IP>:8088
```

Se in `.env` hai scelto una porta diversa, usa quella.

## 7. Verification
Controllo rapido post-installazione:

```bash
curl -I http://<SERVER_IP>:8088
curl -s http://127.0.0.1:8003/api/health
```

Se la UI e bindata su un IP specifico di LAN, verifica quell'indirizzo. Non assumere `127.0.0.1:8088` come controllo universale.

Controlli minimi in UI:
- `/` raggiungibile
- dashboard caricata
- `/config` legge il file YAML reale
- `/logs` mostra output backend e Piper
- `/devices` si apre

Note di lettura corrette:
- se il backend health risponde ma `device` appare `disconnected`, non e un errore quando nessun device e collegato
- se Piper non gira, la UI puo comunque avviarsi; semplicemente la dashboard lo mostrera come non healthy

## 8. systemd opzionale
Esempio di file:

```ini
[Unit]
Description=Xiaozhi Admin UI
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=xiaozhi
Group=xiaozhi
WorkingDirectory=/home/xiaozhi/xiaozhi-admin-ui
EnvironmentFile=/home/xiaozhi/xiaozhi-admin-ui/.env
ExecStart=/home/xiaozhi/xiaozhi-admin-ui/.venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8088
Restart=always
RestartSec=3
StandardOutput=journal
StandardError=journal
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=full
ProtectHome=false
ReadWritePaths=/home/xiaozhi/xiaozhi-admin-ui /home/xiaozhi/xiaozhi-esp32-lightserver/data

[Install]
WantedBy=multi-user.target
```

Salvalo, per esempio, come:

```text
/etc/systemd/system/xiaozhi-admin-ui.service
```

Poi abilitalo:

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now xiaozhi-admin-ui
sudo systemctl status xiaozhi-admin-ui --no-pager -l
journalctl -u xiaozhi-admin-ui -f
```

Se cambi porta nella `.env`, aggiorna anche `ExecStart` oppure lancia `uvicorn` leggendo host e porta dal tuo supervisor esterno.

## 9. Porte e connettivita
Porte tipiche:
- Admin UI: `8088`
- backend health: `8003`
- Piper health: `8091`

Esempi di verifica:

```bash
ss -ltnp | grep 8088
curl -I http://<SERVER_IP>:8088
curl -s http://127.0.0.1:8003/api/health
curl -s http://127.0.0.1:8091/health
```

## 10. Checklist finale
Considera l'installazione riuscita se:

1. `import app.main` funziona.
2. la UI risponde su `http://<SERVER_IP>:<ADMIN_UI_PORT>`.
3. la dashboard mostra stato servizi senza errori bloccanti.
4. `/config` legge il file YAML reale del backend.
5. un salvataggio crea un backup.
6. `/logs` mostra output di backend e Piper.
7. `/devices` mostra la vista runtime.
8. `/llm`, `/asr` e `/tts` mostrano i profili attesi.
9. `systemctl status xiaozhi-admin-ui` e attivo, se usi systemd.

## 11. Troubleshooting base
`No module named 'app'`
- stai lanciando `uvicorn` fuori dalla root del progetto

`Permission denied` sul file config
- l'utente della UI non puo scrivere `XIAOZHI_CONFIG`

La dashboard si apre ma la runtime health e sbagliata
- controlla `BACKEND_HOST`
- controlla `BACKEND_HEALTH_PORT`

Le azioni restart o log non funzionano
- controlla `XSERVER_SCRIPT_PATH`
- controlla `PIPER_SCRIPT_PATH`
- controlla `XIAOZHI_DIR`
- controlla `PIPER_SERVICE_NAME`

`docker compose ps` fallisce dalla UI
- la directory backend configurata non e quella reale
- il comando funziona a mano ma non col servizio systemd per problemi di permessi o ambiente

Piper risulta giu ma il servizio e attivo
- verifica `PIPER_SERVICE_NAME`
- verifica `PIPER_HEALTH_URL`

La UI funziona in shell ma non via systemd
- controlla `WorkingDirectory`
- controlla `EnvironmentFile`
- controlla i path nel servizio
- leggi `journalctl -u xiaozhi-admin-ui -n 100 --no-pager`

## 12. Limiti attuali
- la UI resta pensata per stare vicino al backend, non come pannello remoto generico
- il backend repo e il file config devono restare accessibili localmente alla UI
- Docker, systemd e Piper non vengono installati da questa guida: devono gia esistere
- non c'e autenticazione applicativa obbligatoria
