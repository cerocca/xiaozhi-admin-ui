# SETUP

Questa guida serve a installare `xiaozhi-admin-ui` da zero su un server Linux e a capire dove adattare path, IP e porte.

Obiettivo:
- installazione replicabile
- avvio manuale
- avvio con systemd
- verifica finale
- chiarimento dei limiti attuali del progetto

## 1. Placeholder usati in questa guida
Sostituisci questi valori con i tuoi:

- `<user>`: utente Linux che eseguira la UI
- `<SERVER_IP>`: IP del server che espone la UI
- `<ADMIN_UI_PORT>`: porta HTTP della UI, per esempio `8088`
- `<BACKEND_IP>`: IP del server che espone il backend Xiaozhi
- `<BACKEND_PORT>`: porta HTTP del backend, per esempio `8003`
- `<PIPER_PORT>`: porta HTTP di Piper, per esempio `8091`

Path di esempio riusabili:
- repo UI: `/home/<user>/xiaozhi-admin-ui`
- repo backend: `/home/<user>/xiaozhi-esp32-lightserver`
- alternativa installazione UI: `/opt/xiaozhi-admin-ui`
- alternativa installazione backend: `/opt/xiaozhi-esp32-lightserver`

In questa guida usero come percorso consigliato:
- `/home/<user>/xiaozhi-admin-ui`
- `/home/<user>/xiaozhi-esp32-lightserver`

Motivo:
oggi alcuni script e alcuni default del progetto sono ancora allineati a un deploy sotto `/home/<user>/...`.

## 2. Cosa serve prima di iniziare
Prerequisiti minimi:

1. Linux con accesso shell.
2. Python 3 installato.
3. `venv` disponibile.
4. `git` installato.
5. backend `xiaozhi-esp32-lightserver` gia presente.
6. file config reale del backend gia esistente.
7. Docker e Docker Compose funzionanti per il backend.
8. systemd disponibile se vuoi gestire la UI come servizio.
9. Piper gia installato se vuoi usare le funzioni operative relative a Piper.

Verifica rapida:

```bash
python3 --version
git --version
docker --version
docker compose version
systemctl --version
```

## 3. Preflight sul backend
Prima di installare la UI, conferma che il backend esista davvero e che il file config sia raggiungibile.

Esempio:

```bash
ls -l /home/<user>/xiaozhi-esp32-lightserver
ls -l /home/<user>/xiaozhi-esp32-lightserver/data/.config.yaml
cd /home/<user>/xiaozhi-esp32-lightserver
docker compose ps
```

Se Piper e sulla stessa macchina:

```bash
systemctl status piper-api --no-pager
curl -s http://127.0.0.1:<PIPER_PORT>/health
```

Devi arrivare a questo stato:
- il repo backend esiste
- `data/.config.yaml` esiste
- l'utente che eseguira la UI puo leggere e scrivere la config
- `docker compose ps` funziona nella directory backend

## 4. Clone del repository UI

```bash
git clone <REPO_URL> /home/<user>/xiaozhi-admin-ui
cd /home/<user>/xiaozhi-admin-ui
```

Se vuoi installare in `/opt/xiaozhi-admin-ui`, puoi farlo.
Pero devi poi verificare con attenzione la sezione "Adattamenti obbligatori" piu sotto, perche alcuni script del progetto non sono ancora totalmente path-agnostic.

## 5. Virtualenv e dipendenze Python

```bash
cd /home/<user>/xiaozhi-admin-ui
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -c "import fastapi, jinja2, yaml, httpx; print('deps ok')"
```

Se l'ultimo comando stampa `deps ok`, le dipendenze base sono installate.

## 6. Configurazione `.env`
Crea il file:

```text
/home/<user>/xiaozhi-admin-ui/.env
```

Esempio minimo:

```env
ADMIN_UI_HOST=0.0.0.0
ADMIN_UI_PORT=<ADMIN_UI_PORT>

XIAOZHI_DIR=/home/<user>/xiaozhi-esp32-lightserver
XIAOZHI_CONFIG=/home/<user>/xiaozhi-esp32-lightserver/data/.config.yaml

PIPER_HEALTH_URL=http://127.0.0.1:<PIPER_PORT>/health
PIPER_SYSTEMD_SERVICE=piper-api

LAN_CIDR=192.168.1.0/24
```

Come scegliere i valori:
- `ADMIN_UI_HOST`: usa `0.0.0.0` per ascoltare su tutte le interfacce, oppure `<SERVER_IP>` se vuoi bind esplicito.
- `ADMIN_UI_PORT`: porta della UI.
- `XIAOZHI_DIR`: directory del repo backend.
- `XIAOZHI_CONFIG`: path del file config reale del backend.
- `PIPER_HEALTH_URL`: health endpoint di Piper.
- `PIPER_SYSTEMD_SERVICE`: nome unita systemd di Piper.
- `LAN_CIDR`: rete LAN usata come riferimento dalla UI.

## 7. Adattamenti obbligatori prima del deploy su un altro server
Questa e la parte piu importante.

Il progetto usa sia variabili `.env` sia valori ancora hardcoded.
Se stai reinstallando su un server diverso dal tuo ambiente originario, controlla questi file:

1. `app/config.py`
   Qui ci sono default per host UI, porta, path backend, path config, Piper e LAN.

2. `app/services/health_service.py`
   Qui l'endpoint del backend `/api/health` e attualmente hardcoded.
   Se il backend gira su `http://<BACKEND_IP>:<BACKEND_PORT>`, aggiorna qui l'URL reale.

3. `scripts/xserver.sh`
   Qui la directory del backend e attualmente hardcoded.
   Se il backend non sta in `/home/<user>/xiaozhi-esp32-lightserver`, aggiorna `XIAOZHI_DIR`.

4. `app/routers/actions.py`
   Alcune azioni usano path assoluti per richiamare i wrapper `scripts/xserver.sh` e `scripts/piper.sh`.
   Se installi la UI fuori da `/home/<user>/xiaozhi-admin-ui`, devi aggiornare anche questi riferimenti.

5. `app/routers/llm.py`
   Anche qui ci sono chiamate a wrapper con path assoluto.
   Se cambi directory di deploy, aggiorna i path dei wrapper.

6. `scripts/piper.sh`
   Verifica che il nome del servizio systemd corrisponda al tuo host.

Se vuoi il percorso meno rischioso oggi, usa:
- `/home/<user>/xiaozhi-admin-ui`
- `/home/<user>/xiaozhi-esp32-lightserver`

Se invece vuoi installare in `/opt/...`, fallo pure, ma aggiorna tutti i riferimenti sopra prima di mettere la UI in produzione.

## 8. Avvio manuale

```bash
cd /home/<user>/xiaozhi-admin-ui
source .venv/bin/activate
python -c "import app.main; print('import ok')"
uvicorn app.main:app --host 0.0.0.0 --port <ADMIN_UI_PORT>
```

Apri nel browser:

```text
http://<SERVER_IP>:<ADMIN_UI_PORT>
```

## 9. Pagine da verificare dopo l'avvio
Controlli minimi:

1. `/`
2. `/ai`
3. `/llm`
4. `/asr`
5. `/tts`
6. `/config`
7. `/backups`
8. `/logs`
9. `/devices`
10. `/vad`
11. `/intent`
12. `/memory`

Verifiche pratiche:
- la dashboard si apre
- la pagina AI Stack si apre
- il config editor legge il file corretto
- i backup compaiono dopo un salvataggio
- i log sono consultabili
- il device runtime viene mostrato
- LLM, ASR e TTS mostrano i profili corretti

## 10. systemd
Esempio di file:

```ini
[Unit]
Description=Xiaozhi Admin UI
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=<user>
Group=<user>
WorkingDirectory=/home/<user>/xiaozhi-admin-ui
EnvironmentFile=/home/<user>/xiaozhi-admin-ui/.env
ExecStart=/home/<user>/xiaozhi-admin-ui/.venv/bin/uvicorn app.main:app --host 0.0.0.0 --port <ADMIN_UI_PORT>
Restart=always
RestartSec=3
StandardOutput=journal
StandardError=journal
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=full
ProtectHome=false
ReadWritePaths=/home/<user>/xiaozhi-admin-ui /home/<user>/xiaozhi-esp32-lightserver/data

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

Se installi la UI in `/opt/xiaozhi-admin-ui`, aggiorna nel file systemd:
- `WorkingDirectory`
- `EnvironmentFile`
- `ExecStart`
- `ReadWritePaths`

## 11. Porte e connettivita
Porte tipiche:
- Admin UI: `<ADMIN_UI_PORT>`
- backend health: `<BACKEND_PORT>`
- Piper health: `<PIPER_PORT>`

Esempi di verifica:

```bash
ss -ltnp | grep <ADMIN_UI_PORT>
curl -I http://127.0.0.1:<ADMIN_UI_PORT>
curl -s http://<BACKEND_IP>:<BACKEND_PORT>/api/health
curl -s http://127.0.0.1:<PIPER_PORT>/health
```

Se il backend e su un'altra macchina:
- `XIAOZHI_CONFIG` deve puntare a un file locale accessibile dalla UI, oppure la parte di editing config non funzionera
- `docker compose` e i wrapper locali non controlleranno un backend remoto a meno di adattamenti ulteriori
- la health runtime puo comunque essere letta via HTTP se imposti l'URL corretto nel file indicato sopra

In pratica:
la UI oggi e progettata soprattutto per un setup LAN-first in cui la macchina che ospita la UI ha anche accesso locale al repo backend e alla sua config.

## 12. Checklist finale
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

## 13. Troubleshooting base
`No module named 'app'`
- stai lanciando `uvicorn` fuori dalla root del progetto

`Permission denied` sul file config
- l'utente della UI non puo scrivere `XIAOZHI_CONFIG`

La dashboard si apre ma la runtime health e sbagliata
- controlla `app/services/health_service.py`
- verifica IP e porta reali del backend

Le azioni restart o log non funzionano
- controlla i path assoluti nei wrapper e nei router
- verifica `scripts/xserver.sh`
- verifica `scripts/piper.sh`

`docker compose ps` fallisce dalla UI
- la directory backend configurata non e quella reale
- il comando funziona a mano ma non col servizio systemd per problemi di permessi o ambiente

Piper risulta giu ma il servizio e attivo
- verifica `PIPER_SYSTEMD_SERVICE`
- verifica `PIPER_HEALTH_URL`

La UI funziona in shell ma non via systemd
- controlla `WorkingDirectory`
- controlla `EnvironmentFile`
- controlla i path nel servizio
- leggi `journalctl -u xiaozhi-admin-ui -n 100 --no-pager`

## 14. Limiti attuali da tenere presenti
- il progetto non e ancora completamente host-agnostic
- alcuni path sono ancora assoluti
- l'endpoint backend `/api/health` non e ancora configurato via `.env`
- la UI e pensata per operare vicino al backend, non come pannello remoto generico
- non c'e autenticazione applicativa obbligatoria
