# Xiaozhi Admin UI

## Scopo
Xiaozhi Admin UI è una WebUI leggera per amministrare un server `xiaozhi-esp32-server` già funzionante, senza modificare in modo invasivo il runtime audio.

Serve a:
- vedere lo stato del server Xiaozhi e di Piper
- leggere e modificare `.config.yaml`
- creare backup automatici prima dei salvataggi
- fare rollback della config
- riavviare Xiaozhi e Piper
- leggere i log principali
- vedere i device ricavati dai log recenti

## Filosofia
Questo progetto segue regole semplici:

- **solo LAN**
- **approccio prudente**
- **zero stack pesanti**
- **prima stabilità, poi UX**
- **nessun accoppiamento forte con il runtime Xiaozhi**

## Stato attuale
MVP implementato e operativo.

Funzionalità presenti:
- dashboard stato servizi
- config editor con validazione YAML minima
- backup automatico + rollback
- restart Xiaozhi
- restart Piper
- log viewer Xiaozhi / Piper
- device list ricavata dai log
- servizio systemd dedicato
- accesso LAN-only

## Cosa non fa ancora
- nessuna UI guidata per provider/modelli LLM/ASR/TTS
- nessun database persistente per i device
- nessuna autenticazione applicativa nel MVP
- nessun reverse proxy obbligatorio

## Architettura in una riga
Browser LAN → FastAPI Admin UI → wrapper scripts → Docker Compose / systemd / file config

## Requisiti operativi
Questa documentazione presume:

- host Linux
- `xiaozhi-esp32-server` già presente e funzionante
- Piper API già presente e funzionante
- Python 3 installato
- Docker + Docker Compose funzionanti
- permessi coerenti per leggere/scrivere la config Xiaozhi

## Percorsi usati nel setup di riferimento
- Admin UI: `/home/ciru/xiaozhi-admin-ui`
- Xiaozhi server: `/home/ciru/xiaozhi-esp32-server`
- Config Xiaozhi: `/home/ciru/xiaozhi-esp32-server/data/.config.yaml`
- Piper systemd service: `piper-api`
- URL UI: `http://192.168.1.69:8088`

## Importante
Questi documenti sono pensati per essere **installabili da zero sul progetto Admin UI**, ma **presuppongono che il codice sorgente di `xiaozhi-admin-ui` esista già nel repository o nella directory di lavoro**.

Se il codice non è ancora stato salvato nel repo, bisogna prima creare i file applicativi del progetto e solo dopo usare questa guida per installazione e configurazione.
