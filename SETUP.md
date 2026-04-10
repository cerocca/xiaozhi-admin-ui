# SETUP

Questa guida copre il percorso più semplice per installare `xiaozhi-admin-ui` su un server Linux, con configurazione esplicita e pochi passaggi manuali.

---

## 1. Prerequisiti

Serve già avere:

- Linux con accesso shell
- `git`
- Python 3 con `venv`
- backend Xiaozhi funzionante
- accesso al file config del backend
- Docker e Docker Compose (per il backend)
- Piper opzionale

Backend compatibili (esempi):

- `xiaozhi-esp32-lightserver`
- `xiaozhi-esp32-server`

Requisito fondamentale:

- endpoint `/api/health` disponibile e funzionante

---

## 2. Preflight backend (obbligatorio)

Verifica che il backend sia realmente funzionante:

```bash
ls -ld /home/xiaozhi/xiaozhi-esp32-lightserver
ls -l /home/xiaozhi/xiaozhi-esp32-lightserver/data/.config.yaml

cd /home/xiaozhi/xiaozhi-esp32-lightserver
docker compose ps

curl -s http://127.0.0.1:8003/api/health
```

Deve restituire JSON valido.

Se usi Piper:

```bash
systemctl status piper-api --no-pager
curl -s http://127.0.0.1:8091/health
```

---

## 3. Installazione

```bash
git clone https://github.com/cerocca/xiaozhi-admin-ui.git
cd xiaozhi-admin-ui

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

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

---

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

Opzionale, con default già sensati:

- `XSERVER_SCRIPT_PATH`
- `PIPER_SCRIPT_PATH`
- `XSERVER_SERVICE_NAME`
- `PIPER_HEALTH_URL`
- `LAN_CIDR`

Default già funzionanti se non li imposti:

- `XSERVER_SCRIPT_PATH` e `PIPER_SCRIPT_PATH` puntano agli script nella directory del repo corrente
- `PIPER_HEALTH_URL` usa `http://127.0.0.1:8091/health`
- `LAN_CIDR` usa `192.168.1.0/24`
- `XSERVER_SERVICE_NAME` ha default `xiaozhi-server`
- `scripts/xserver.sh` mantiene un fallback interno per `XIAOZHI_DIR`, ma per un nuovo setup è meglio impostarlo esplicitamente

Note pratiche:

- `ADMIN_UI_HOST=0.0.0.0` è il valore più semplice per esporre la UI in LAN
- `BACKEND_HOST` e `BACKEND_HEALTH_PORT` devono puntare all'endpoint `/api/health`
- `XIAOZHI_CONFIG` deve essere scrivibile dall'utente che esegue la UI

---

## 6. Avvio manuale

```bash
cd /home/xiaozhi/xiaozhi-admin-ui
source .venv/bin/activate

python -c "import app.main; print('import ok')"
uvicorn app.main:app --host 0.0.0.0 --port 8088
```

Apri nel browser:

```
http://<SERVER_IP>:8088
```

---

## 7. Verification

```bash
curl -I http://<SERVER_IP>:8088
curl -s http://127.0.0.1:8003/api/health
```

Se la UI è bindata su un IP specifico di LAN, verifica quell'indirizzo.

Controlli minimi in UI:

- `/` raggiungibile
- dashboard caricata
- `/config` legge il file YAML reale
- `/logs` mostra output backend e Piper
- `/devices` si apre

Note:

- `device = disconnected` non è errore se nessun device è connesso
- Piper può non essere attivo senza bloccare la UI

---

## 8. systemd (opzionale ma consigliato)

File:

```
/etc/systemd/system/xiaozhi-admin-ui.service
```

Contenuto:

```ini
[Unit]
Description=Xiaozhi Admin UI
After=network-online.target

[Service]
Type=simple
User=xiaozhi
WorkingDirectory=/home/xiaozhi/xiaozhi-admin-ui
EnvironmentFile=/home/xiaozhi/xiaozhi-admin-ui/.env
ExecStart=/home/xiaozhi/xiaozhi-admin-ui/.venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8088
Restart=always

[Install]
WantedBy=multi-user.target
```

Attiva:

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now xiaozhi-admin-ui
sudo systemctl status xiaozhi-admin-ui --no-pager -l
journalctl -u xiaozhi-admin-ui -f
```

---

## 9. Porte

Porte tipiche:

- Admin UI: `8088`
- backend health: `8003`
- Piper health: `8091`

```bash
ss -ltnp | grep 8088
curl -I http://<SERVER_IP>:8088
curl -s http://127.0.0.1:8003/api/health
curl -s http://127.0.0.1:8091/health
```

---

## 10. Helper CLI (opzionale)

```bash
nano ~/.bashrc
```

Aggiungi:

```bash
alias ui-start="sudo systemctl start xiaozhi-admin-ui"
alias ui-stop="sudo systemctl stop xiaozhi-admin-ui"
alias ui-restart="sudo systemctl restart xiaozhi-admin-ui"
alias ui-status="sudo systemctl status xiaozhi-admin-ui"
alias ui-logs="journalctl -u xiaozhi-admin-ui -f"
```

```bash
source ~/.bashrc
```

---

## 11. Checklist finale

Considera l'installazione riuscita se:

- la UI è raggiungibile su `http://<SERVER_IP>:<ADMIN_UI_PORT>`
- `/api/health` risponde correttamente
- la dashboard non mostra errori bloccanti
- `/config` legge il file YAML reale
- un salvataggio crea un backup
- `/logs` mostra output di backend e Piper
- `/devices` mostra la vista runtime

---

## 12. Troubleshooting base

`No module named 'app'`
- stai lanciando `uvicorn` fuori dalla root del progetto

`Permission denied` sul file config
- l'utente della UI non può scrivere `XIAOZHI_CONFIG`

Health errata:
- controlla `BACKEND_HOST`
- controlla `BACKEND_HEALTH_PORT`

Azioni non funzionano:
- controlla `XIAOZHI_DIR`
- controlla script path

Systemd non funziona:
- controlla `WorkingDirectory`
- controlla `EnvironmentFile`
- usa `journalctl`

---

## 13. Limiti attuali

- la UI è pensata per stare sullo stesso host del backend
- nessuna autenticazione applicativa
- richiede accesso locale a repo e config
