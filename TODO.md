# TODO — Xiaozhi Admin UI

## Priorità alta
- UI guidata provider LLM
- UI guidata modelli LLM
- UI guidata ASR
- UI guidata TTS
- validazione forte config strutturata

## Core backend
- persistenza device in SQLite
- storico connessioni device
- miglior parser log
- associare meglio connect/disconnect con più device
- diff config prima del salvataggio
- retention policy backup

## UX
- messaggi di successo/errore migliori
- filtro device
- filtro log
- dettagli device dedicati
- layout responsive più rifinito

## Sicurezza
- basic auth LAN
- reverse proxy opzionale
- audit azioni admin
- hardening systemd ulteriore

## Operatività
- export/import config
- profili config
- test health integrato
- endpoint health per Admin UI

## Documentazione
- mantenere setup realmente eseguibile da zero
- aggiornare docs insieme ai cambiamenti reali
- documentare sempre permessi, path e sudoers

## Filosofia
Ordine corretto:
1. stabilità
2. operatività
3. UX
4. configurazione guidata avanzata
