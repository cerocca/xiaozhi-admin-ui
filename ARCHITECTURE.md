# Architecture — Xiaozhi Admin UI

## Ruolo
`xiaozhi-admin-ui` è un pannello di management host-side per `xiaozhi-esp32-server`.

Il suo ruolo è amministrativo:

- osservare
- configurare
- riavviare
- leggere log
- vedere device dai log

Non partecipa al runtime audio.

---

## Principio architetturale
Separare sempre:
- runtime Xiaozhi
- tooling admin

Questo consente:
- minore rischio
- debug più semplice
- rollout prudente
- manutenzione chiara

---

## Posizionamento nel sistema

```text
Browser LAN
    ↓
xiaozhi-admin-ui (FastAPI, host-native, systemd)
    ↓
wrapper scripts / services
    ├─ docker compose (xiaozhi-esp32-server)
    ├─ systemctl / journalctl (piper-api)
    └─ file .config.yaml
```

---

## Componenti principali

## 1. Web application
Stack:
- FastAPI
- Jinja2 templates
- CSS custom minimale
- nessuna SPA
- nessun build frontend

### Router
- `dashboard`
- `config_editor`
- `logs`
- `devices`
- `actions`

---

## 2. Service layer

### `status_service.py`
Legge:
- stato Docker Compose
- stato Piper
- health check Piper
- stato config

### `config_service.py`
Gestisce:
- read `.config.yaml`
- validazione YAML
- backup
- write atomico
- rollback

### `log_service.py`
Legge:
- log Xiaozhi via Docker Compose
- log Piper via journalctl

### `device_service.py`
Parsa log Xiaozhi e ricava:
- `device_id`
- `client_id`
- `session_id`
- IP
- model
- version
- last seen
- status stimato
- ultimo evento

### `command_service.py`
Esegue wrapper scripts in modo controllato, con timeout e ritorno strutturato.

---

## 3. Template layer
Template principali:
- `dashboard.html`
- `config_editor.html`
- `backups.html`
- `logs.html`
- `devices.html`
- `action_result.html`

Scelta intenzionale:
- rendering server-side
- semplicità
- debug facile
- minima complessità

---

## 4. Script wrapper
La UI non deve eseguire shell libera.  
Usa solo wrapper scripts noti.

Script previsti:
- `admin-ui.sh`
- `xserver.sh`
- `piper.sh`

### Vantaggi
- meno rischio
- comportamento deterministico
- debug ripetibile
- coerenza tra shell e UI

---

## 5. Integrazione con Xiaozhi
`xiaozhi-esp32-server` resta separato e containerizzato.

Admin UI interagisce solo con:
- `docker compose ps`
- `docker compose restart`
- `docker compose logs`
- `.config.yaml`

Non modifica immagini né codice runtime.

---

## 6. Integrazione con Piper
`piper-api` resta un servizio host-native via systemd.

Admin UI usa:
- `systemctl status piper-api`
- `systemctl restart piper-api`
- `journalctl -u piper-api`
- health check HTTP locale

---

## 7. Gestione config
### Save
UI → validazione YAML → backup → write atomico → nessun restart automatico

### Rollback
UI → restore backup → nessun restart automatico

### Scelta voluta
Restart separato da salvataggio:
- meno sorprese
- più controllo
- meno rischio

---

## 8. Gestione log
Approccio MVP:
- lettura on-demand
- tail numerico
- refresh esplicito o periodico
- niente live stream complesso

### Fonte log
- Xiaozhi: Docker Compose
- Piper: journalctl

---

## 9. Gestione devices
Nel MVP la pagina `/devices` è log-derived, non database-driven.

### Vantaggi
- semplicità
- zero migrazioni
- nessuna persistenza nuova

### Limiti
- dipende dai log recenti
- non è uno storico completo
- non è realtime vero

---

## 10. Persistenza
Persistenza minima attuale:
- config Xiaozhi
- backup config in:
  - `/home/ciru/xiaozhi-admin-ui/data/backups/config`

Nessun DB nel MVP.

---

## 11. Sicurezza
Scelte attuali:
- LAN only
- bind su IP LAN
- nessuna auth nel MVP
- nessuna shell arbitraria
- sudoers mirato al minimo indispensabile

---

## 12. Evoluzione prevista
Livello 2:
- UI guidata provider/modelli LLM
- UI guidata ASR
- UI guidata TTS
- validazione forte campi
- config strutturata
- eventuale persistenza device in SQLite
