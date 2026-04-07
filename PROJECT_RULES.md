# Project Rules — Xiaozhi Admin UI

## Obiettivo
Mantenere il progetto semplice, robusto, manutenibile e installabile senza ambiguità.

---

## 1. Regola principale
Non rompere mai il setup funzionante di `xiaozhi-esp32-server`.

Ogni modifica deve privilegiare:
- prudenza
- reversibilità
- isolamento
- facilità di debug

---

## 2. Architettura
Preferire:
- FastAPI + Jinja2
- systemd host-native
- wrapper scripts
- componenti minimi

Evitare salvo forte motivo:
- frontend pesanti
- stack complessi
- coupling forte col runtime Xiaozhi
- modifiche invasive al container

---

## 3. Sicurezza
Regole:
- accesso solo LAN
- niente shell arbitraria dalla UI
- sudo minimo indispensabile
- restart espliciti
- backup prima di scrivere config

---

## 4. Operatività
Ogni azione critica deve essere:
- esplicita
- leggibile
- tracciabile
- debuggabile

Restart e save config devono restare separati nel MVP.

---

## 5. Qualità documentazione
La documentazione deve essere realmente eseguibile.

Deve sempre includere:
- prerequisiti
- path reali
- comandi esatti
- verifiche attese
- errori comuni
- checklist finale

Documentazione solo descrittiva non basta.

---

## 6. Ordine di sviluppo
Ordine corretto:
1. MVP stabile
2. miglioramenti operativi
3. UX più pulita
4. configurazione guidata provider/modelli

Mai sacrificare la stabilità per UX o feature premature.

---

## 7. Regole di modifica
Quando si aggiungono feature:
- fare cambi piccoli
- evitare refactor inutili
- preservare compatibilità col setup esistente
- aggiornare subito i documenti rilevanti

---

## 8. Confine con Xiaozhi server
`xiaozhi-admin-ui` è separato da `xiaozhi-esp32-server`.

Deve:
- osservare
- configurare
- controllare

Non deve:
- incorporare il server
- sostituire il runtime
- dipendere da refactor profondi del backend Xiaozhi

---

## 9. Filosofia finale
Semplice batte elegante.  
Robusto batte sofisticato.  
Controllabile batte automatico.  
Documentato batte implicito.
