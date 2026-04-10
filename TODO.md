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
- Tab Devices già presente
- Versioning UI + footer + repo link
- CHANGELOG.md iniziale

---

## 🚀 Priorità alta (v0.2.0)

### UI Health UX (focus principale)
Obiettivo: rendere lo stato runtime immediato, chiaro e non ambiguo

- [ ] Rendere esplicito lo stato:
  - LLM / ASR / TTS / DEVICE
- [ ] Distinguere chiaramente:
  - backend non raggiungibile
  - modulo in errore
- [ ] Device:
  - connected → positivo
  - disconnected → neutro (non errore)
- [ ] Usare `details` solo come contesto (endpoint, http_status, reason)
- [ ] Fallback visivo (es. UNKNOWN) se health non disponibile

---

## 🟡 Priorità media

### Device details (miglioramento tab esistente)
Obiettivo: maggiore visibilità runtime

- [ ] Mostrare Last seen
- [ ] Stato websocket più dettagliato
- [ ] Info device (ID, IP, firmware se disponibile)
- [ ] Migliorare leggibilità stato device nella tab esistente

---

### Logs più utili
Obiettivo: debug rapido senza SSH

- [ ] Filtro per servizio (xserver / piper)
- [ ] Selezione numero righe
- [ ] Evidenziazione errori (senza JS complesso)

---

### Operatività

#### Config
- [ ] Export config (download YAML)
- [ ] Import config (upload YAML)
- [ ] Diff prima del salvataggio (preview modifiche)

#### Backup
- [ ] Retention policy (es. ultimi N backup)

---

## 🟢 Priorità bassa / futura

### Device tracking
- [ ] Storico connessioni
- [ ] Persistenza base (SQLite leggera)

---

### Sicurezza (LAN-first)
- [ ] Basic Auth per Admin UI
- [ ] Audit log azioni admin (restart/stop/config)
- [ ] Reverse proxy opzionale (nginx/caddy)
- [ ] Hardening systemd

---

### UX / UI polish
- [ ] Microcopy migliorata
- [ ] Responsive base (mobile)
- [ ] Allineamenti visivi minori

---

### Documentazione
- [ ] Setup completo da zero (Sibilla)
- [ ] Documentare:
  - path
  - permessi
  - servizi systemd
- [ ] Aggiornare docs insieme alle feature
- [ ] Troubleshooting reale

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

