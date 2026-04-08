# Project Rules — Xiaozhi Admin UI

## Obiettivo
Mantenere il progetto semplice, robusto, coerente con il deploy reale e facile da manutenere senza refactor massivi.

## 1. Regola principale
Non rompere mai il setup funzionante di `xiaozhi-esp32-lightserver`.

Ogni modifica deve privilegiare:
- prudenza
- reversibilita
- isolamento
- facilita di debug

## 2. Confine architetturale
Preferire:
- FastAPI + Jinja2
- host-native + systemd
- wrapper scripts noti
- componenti minimi

Evitare salvo motivo forte:
- frontend pesanti
- nuove dipendenze non necessarie
- coupling forte col runtime Xiaozhi
- cambi invasivi al container o al modello YAML generale

## 3. Operazioni critiche
Ogni azione critica deve essere:
- esplicita
- leggibile
- tracciabile
- debuggabile

Regole concrete:
- backup prima di scrivere config
- restart separato dal save config
- niente shell arbitraria dalla UI
- compatibilita mantenuta dove il setup reale la usa ancora

## 4. Regole LLM
Stato supportato oggi:
- multi-provider Livello 1
- piu profili sotto `LLM`
- un solo profilo attivo alla volta

Source of truth:
- `runtime.llm_profile`

Compatibilita legacy ancora supportata:
- `selected_module.llm`
- endpoint legacy di salvataggio LLM

Regola importante:
- `provider_id` non e il nome del profilo
- `profile_name` e la chiave reale sotto `LLM`

Livello 2 resta fuori scope finche non serve davvero:
- routing/fallback multi-provider
- validazione strutturale completa del blocco `LLM`
- UI guidata completa per capability avanzate

## 5. Documentazione
La documentazione deve essere eseguibile e aderente al progetto reale.

Deve includere:
- path reali correnti
- prerequisiti
- comandi esatti
- verifiche attese
- limiti noti
- punti legacy ancora supportati

Documentazione vecchia ma elegante vale meno di documentazione corta ma vera.

## 6. Regole di modifica
Quando si tocca il repo:
- fare cambi piccoli
- non fare refactor ampi senza bisogno operativo
- non cambiare UX o comportamento runtime salvo bug evidenti
- non introdurre nuove dipendenze per cleanup minori
- aggiornare subito i documenti se cambia il comportamento reale

## 7. Repo hygiene
Non tenere nel repository:
- `.DS_Store`
- file AppleDouble `._*`
- `__pycache__`
- `.pyc`
- file temporanei o accidentali
- backup locali non usati dal runtime

`.gitignore` deve restare minimale e focalizzato sul rumore reale del progetto.

## 8. Filosofia finale
Semplice batte elegante.
Robusto batte sofisticato.
Controllabile batte automatico.
Documentato batte implicito.
