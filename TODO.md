# TODO – Xiaozhi Admin UI

## 🎯 Stato attuale

La Admin UI è stabile e utilizzabile in produzione LAN.

Completato:
- Dashboard operativa (status, restart/stop/log)
- AI Stack con distinzione chiara:
  - Config (statico)
  - Runtime (/api/health)
- Configurazione LLM / ASR / TTS via UI
- Integrazione Piper TTS
- Runtime health reale backend
- Device runtime (connected/disconnected)
- Versioning UI + footer + repo link
- CHANGELOG.md iniziale

---

## 🚀 Priorità alta (prossimi step)

### 1. Migliorare runtime health UI
Obiettivo: rendere il debug ancora più immediato

- [ ] Pulsante manuale "Refresh health"
- [ ] Timestamp ultimo controllo
- [ ] Distinguere:
  - backend health non raggiungibile
  - modulo runtime in errore
- [ ] Gestione fallback visiva (es. badge "UNKNOWN")

---

### 2. Device details
Obiettivo: capire davvero cosa fa il device

- [ ] Pagina dedicata Device
- [ ] Last seen
- [ ] Stato websocket più dettagliato
- [ ] Eventuali info device (ID, IP, firmware se disponibile)

---

### 3. Logs più utili
Obiettivo: debug rapido senza SSH

- [ ] Filtro per servizio (xserver / piper)
- [ ] Selezione numero righe
- [ ] Evidenziazione errori (facoltativo, no JS complesso)

---

## ⚙️ Operatività

### Config
- [ ] Export config (download YAML)
- [ ] Import config (upload YAML)
- [ ] Diff prima del salvataggio (preview modifiche)

### Backup
- [ ] Retention policy (es. ultimi N backup)

### Device tracking
- [ ] Storico connessioni
- [ ] Persistenza base (SQLite leggera)

---

## 🔐 Sicurezza (LAN-first)

- [ ] Basic Auth per Admin UI
- [ ] Audit log azioni admin (restart/stop/config)
- [ ] Reverse proxy opzionale (nginx/caddy)
- [ ] Hardening systemd (restart policy, limits)

---

## 🎨 UX / UI polish

- [ ] Microcopy migliorata (messaggi chiari)
- [ ] Miglioramento responsive (mobile base)
- [ ] Piccoli allineamenti visivi se emergono

---

## 📚 Documentazione

- [ ] Setup completo da zero (Sibilla)
- [ ] Documentare:
  - path
  - permessi
  - servizi systemd
- [ ] Aggiornare docs insieme alle feature
- [ ] Aggiungere note per troubleshooting reale

---

## ❌ Fuori scope (per ora)

- Routing LLM avanzato
- Auto-refresh / polling continuo
- Refactor architetturali
- Firmware / device logic

---

## 🧭 Linee guida progetto

- Semplicità > feature
- Server-rendered (no SPA)
- No JS complesso
- Debug reale > UI decorativa
- Patch incrementali, no refactor massivi
