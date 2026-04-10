# Changelog

Tutte le modifiche rilevanti della Admin UI vengono annotate qui.

## [Unreleased]

- Miglioramento UX della sezione Health (chiarezza stato LLM / ASR / TTS / device).
- Uso più esplicito dei dettagli (`details`) come contesto e non come stato primario.
- Miglioramento della semantica device (connected vs disconnected).

## [0.1.1]

- Migliorata la portabilità della Admin UI tramite configurazione centralizzata.
- Introduzione di `.env.example` per setup semplificato.
- Rimozione di path hardcoded e uso consistente di settings/env.
- Migliorata la documentazione (README e SETUP) per installazione da zero.
- Correzioni ai wrapper script (`xserver.sh`, `piper.sh`) per supportare variabili da environment.
- Migliorata la gestione dei path interni (backup, log, script) rispetto alla root del progetto.

## [0.1.0]

- Prima milestone stabile della Admin UI server-rendered.
- Dashboard iniziale con stato servizi principali e accesso rapido ai log.
- Introduzione della sezione AI Stack per organizzare i moduli AI disponibili.
- Configurazione base LLM con gestione profili principali.
- Pagine core operative per config editor, backups, logs e devices.
- Gestione iniziale di server Xiaozhi, Piper e configurazione runtime.

- Aggiunta gestione CRUD completa per profili ASR e TTS.
- Migliorata la pagina AI Stack con layout più coerente e card meglio allineate.
- Integrazione iniziale della health runtime del backend Xiaozhi.
- Aggiunta visualizzazione runtime del device nella UI.
- Rifinitura della dashboard con azioni restart/stop/log più coerenti.
- Migliorata l’esperienza configurativa TTS con supporto dropdown `voice` per provider come Piper.
