# SETUP — Xiaozhi Admin UI

## Obiettivo
Installare e configurare `xiaozhi-admin-ui` in modo ripetibile e verificabile.

Questa guida è scritta per ridurre gli errori operativi.  
Seguila in ordine.

---

## ⚠️ IMPORTANTE
Questo setup è **post-clone / post-files**.

Significa che:
- la directory del progetto deve già esistere
- il codice applicativo di `xiaozhi-admin-ui` deve già essere presente
- questa guida serve a installare, configurare e validare il progetto
- questa guida **non** sostituisce la creazione del codice sorgente

Directory attesa:

```text
/home/ciru/xiaozhi-admin-ui
```

Se il codice non è ancora stato creato o copiato nella directory progetto, fermarsi qui.

---

## 0. Assunzioni esplicite
Questa guida assume:

- utente Linux: `ciru`
- host: `Sibilla`
- IP LAN del server: `192.168.1.69`
- repo o directory di `xiaozhi-admin-ui` già presente
- repo Xiaozhi già presente in:
  - `/home/ciru/xiaozhi-esp32-server`
- config Xiaozhi già presente in:
  - `/home/ciru/xiaozhi-esp32-server/data/.config.yaml`
- Piper già disponibile come systemd service:
  - `piper-api`

Se uno di questi punti non è vero, correggerlo prima di procedere.

---

## 1. Preflight checklist
Eseguire questi controlli prima di installare.

### 1.1 Verifica Python
```bash
python3 --version
```

### 1.2 Verifica Docker e Compose
```bash
docker --version
docker compose version
```

### 1.3 Verifica server Xiaozhi
```bash
cd /home/ciru/xiaozhi-esp32-server
docker compose ps
```

Atteso:
- il container principale è `Up`

### 1.4 Verifica Piper
```bash
systemctl status piper-api --no-pager
curl -s http://127.0.0.1:8091/health ; echo
```

Atteso:
- `active (running)`
- health check HTTP valido

### 1.5 Verifica config Xiaozhi
```bash
ls -l /home/ciru/xiaozhi-esp32-server/data/.config.yaml
```

Atteso:
- il file esiste
- l'utente che eseguirà Admin UI può leggerlo e scriverlo

---

## 2. Path config Xiaozhi (VINCOLO FORTE)
La config corretta è **solo** questa:

```text
/home/ciru/xiaozhi-esp32-server/data/.config.yaml
```

Non usare:

```text
/home/ciru/xiaozhi-esp32-server/.config.yaml
```

Se il path è sbagliato:
- la UI può leggere il file sbagliato
- il salvataggio può fallire
- il rollback può essere fuorviante
- i restart possono sembrare corretti ma applicarsi a una config diversa da quella attesa

---

## 3. Struttura progetto
La directory attesa è:

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

### 3.1 Se la directory non esiste
```bash
mkdir -p /home/ciru/xiaozhi-admin-ui/{app/{routers,services,templates,static},data/backups/config,scripts}
cd /home/ciru/xiaozhi-admin-ui
```

### 3.2 Se il codice sorgente non è ancora presente
Fermarsi qui.  
Questa guida non sostituisce la creazione del codice applicativo.

---

## 4. Virtualenv
Dalla root progetto:

```bash
cd /home/ciru/xiaozhi-admin-ui
python3 -m venv .venv
source .venv/bin/activate
```

Verifica:
```bash
which python
which pip
```

Atteso:
- i path devono puntare dentro `/home/ciru/xiaozhi-admin-ui/.venv/`

---

## 5. Dipendenze Python

### 5.1 Creare `requirements.txt`
Contenuto di riferimento:

```txt
fastapi==0.115.12
uvicorn[standard]==0.34.0
jinja2==3.1.6
python-multipart==0.0.20
pydantic==2.11.3
pydantic-settings==2.8.1
httpx==0.28.1
PyYAML==6.0.2
```

### 5.2 Installare
```bash
pip install -r requirements.txt
```

### 5.3 Verifica
```bash
python -c "import fastapi, jinja2, yaml, httpx; print('deps ok')"
```

---

## 6. File `.env`

Creare:

`/home/ciru/xiaozhi-admin-ui/.env`

Contenuto di riferimento:

```env
ADMIN_UI_HOST=192.168.1.69
ADMIN_UI_PORT=8088

XIAOZHI_DIR=/home/ciru/xiaozhi-esp32-server
XIAOZHI_CONFIG=/home/ciru/xiaozhi-esp32-server/data/.config.yaml

PIPER_HEALTH_URL=http://127.0.0.1:8091/health
PIPER_SYSTEMD_SERVICE=piper-api

LAN_CIDR=192.168.1.0/24
```

### 6.1 Verifica file
```bash
cat /home/ciru/xiaozhi-admin-ui/.env
```

---

## 7. Primo test applicativo (obbligatorio)

Dalla root progetto:

```bash
cd /home/ciru/xiaozhi-admin-ui
source .venv/bin/activate
python -c "import app.main; print('import ok')"
```

Se qui fallisce, **non** procedere con systemd.  
Correggere prima il codice o i path.

---

## 8. Avvio manuale di test
Dalla root progetto:

```bash
cd /home/ciru/xiaozhi-admin-ui
source .venv/bin/activate
uvicorn app.main:app --host 192.168.1.69 --port 8088
```

Aprire da browser in LAN:

```text
http://192.168.1.69:8088
```

### Verifiche minime
Controllare che siano raggiungibili:

- `/`
- `/config`
- `/backups`
- `/logs`
- `/devices`

### Errore comune
Se si lancia `uvicorn` da una directory sbagliata:
- errore: `No module named 'app'`

Fix:
```bash
cd /home/ciru/xiaozhi-admin-ui
source .venv/bin/activate
uvicorn app.main:app --host 192.168.1.69 --port 8088
```

---

## 9. Service systemd

### 9.1 Creare il file service
Creare:

`/etc/systemd/system/xiaozhi-admin-ui.service`

Contenuto di riferimento:

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
ReadWritePaths=/home/ciru/xiaozhi-admin-ui /home/ciru/xiaozhi-esp32-server/data
ProtectHome=false

[Install]
WantedBy=multi-user.target
```

### 9.2 Abilitare
```bash
sudo systemctl daemon-reload
sudo systemctl enable --now xiaozhi-admin-ui
sudo systemctl status xiaozhi-admin-ui --no-pager -l
```

### 9.3 Log
```bash
journalctl -u xiaozhi-admin-ui -f
```

### Errore comune: `address already in use`
Causa:
- un'istanza manuale di `uvicorn` è ancora attiva

Fix:
- fermare il processo manuale
- riavviare il servizio

---

## 10. Restrizione LAN-only

### 10.1 Bind su IP LAN
Il servizio systemd avvia Admin UI direttamente su:
- `192.168.1.69:8088`

### 10.2 Firewall UFW (consigliato)
```bash
sudo ufw allow from 192.168.1.0/24 to any port 8088 proto tcp
sudo ufw deny 8088/tcp
sudo ufw reload
sudo ufw status
```

Atteso:
- la UI è raggiungibile solo dalla LAN

---

## 11. Permessi file config Xiaozhi
Verificare:

```bash
ls -l /home/ciru/xiaozhi-esp32-server/data/.config.yaml
```

Se necessario, correggere proprietario o permessi in modo coerente col proprio setup.

Esempio:

```bash
sudo chown ciru:ciru /home/ciru/xiaozhi-esp32-server/data/.config.yaml
```

### Importante
Se Admin UI non può scrivere la config:
- il salvataggio fallirà
- il rollback fallirà

---

## 12. Sudoers per Piper
Admin UI riavvia Piper con `systemctl restart piper-api`.

### 12.1 Verificare path di `systemctl`
```bash
which systemctl
```

Atteso normalmente:
```text
/usr/bin/systemctl
```

### 12.2 Creare file sudoers dedicato
```bash
sudo visudo -f /etc/sudoers.d/xiaozhi-admin-ui
```

Inserire:

```sudoers
ciru ALL=(root) NOPASSWD: /usr/bin/systemctl restart piper-api, /usr/bin/systemctl status piper-api
```

### 12.3 Test
```bash
sudo systemctl restart piper-api
sudo systemctl status piper-api --no-pager
```

Se qui fallisce, correggere subito prima di testare la WebUI.

---

## 13. Script CLI operativi

### 13.1 Directory script
```text
/home/ciru/xiaozhi-admin-ui/scripts
```

### 13.2 Requisiti minimi script
Ogni script deve:
- avere shebang valido, per esempio:
  - `#!/usr/bin/env bash`
- essere eseguibile
- trovarsi nella cartella `scripts/`

Rendere eseguibili:

```bash
cd /home/ciru/xiaozhi-admin-ui
chmod +x scripts/*.sh
```

### 13.3 Symlink globali consigliati
```bash
sudo ln -s /home/ciru/xiaozhi-admin-ui/scripts/admin-ui.sh /usr/local/bin/xui
sudo ln -s /home/ciru/xiaozhi-admin-ui/scripts/xserver.sh /usr/local/bin/xserver
sudo ln -s /home/ciru/xiaozhi-admin-ui/scripts/piper.sh /usr/local/bin/piper
```

### 13.4 Verifica symlink / comandi
```bash
which xui
which xserver
which piper
```

Se uno dei tre comandi non esiste, correggere prima di continuare.

### 13.5 Comandi attesi
```bash
xui restart
xui logs
xui rlogs

xserver status
xserver restart
xserver logs
xserver tail 100
xserver rlogs

piper status
piper restart
piper logs
piper tail 100
piper rlogs
```

---

## 14. Verifiche finali da browser

### 14.1 Dashboard
Aprire `/` e verificare:
- Xiaozhi healthy
- Piper healthy
- config path corretto

### 14.2 Config editor
Aprire `/config` e verificare:
- contenuto caricato
- salvataggio YAML valido
- errore con YAML invalido
- backup automatico prima del save

### 14.3 Backups
Aprire `/backups` e verificare:
- presenza backup
- restore disponibile

### 14.4 Logs
Aprire:
- `/logs?source=xserver&lines=200`
- `/logs?source=piper&lines=200`

### 14.5 Devices
Con un device acceso e connesso:
- aprire `/devices?lines=1000`

### 14.6 Restart UI
Verificare:
- Restart Xiaozhi funziona
- Restart Piper funziona

---

## 15. Troubleshooting rapido

### `No module named 'app'`
Sei nella directory sbagliata. Tornare nella root progetto.

### `address already in use`
C'è già una istanza di `uvicorn` attiva.

### `/devices` vuoto
Cause comuni:
- device spento
- log recenti insufficienti
- `lines` troppo basso

Fix:
- accendere il device
- controllare prima `/logs?source=xserver&lines=1000`
- poi `/devices?lines=1000`

### Restart Piper fallisce
Controllare:
- file sudoers
- path di `systemctl`
- stato del servizio `piper-api`

### Restart Xiaozhi fallisce
Controllare:
- `docker compose ps`
- permessi utente Docker
- path `XIAOZHI_DIR`

---

## 16. Checklist finale “a prova di errore”
Non considerare finito il setup finché non sono veri tutti questi punti:

- [ ] `python -c "import app.main"` funziona
- [ ] avvio manuale `uvicorn` funziona
- [ ] `xiaozhi-admin-ui.service` è `active (running)`
- [ ] browser LAN apre `http://192.168.1.69:8088`
- [ ] `/config` salva correttamente
- [ ] `/backups` mostra i backup
- [ ] restart Xiaozhi funziona
- [ ] restart Piper funziona
- [ ] `/logs` funziona per Xiaozhi e Piper
- [ ] `/devices` mostra almeno un device connesso quando il device è attivo
