# PROJECT_RULES

## 1. Obiettivo
Mantenere `xiaozhi-admin-ui` semplice, operativa e facile da capire anche da chi non conosce gia il progetto.

## 2. Principi guida
- semplicita prima delle feature
- patch incrementali prima dei refactor ampi
- chiarezza operativa prima dell'eleganza
- debug reale prima dell'astrazione
- comportamento prevedibile prima dell'automazione

## 3. Confine del progetto
La Admin UI:
- osserva
- modifica la config
- esegue azioni operative limitate
- legge stato runtime dal backend

La Admin UI non deve:
- assorbire responsabilita del backend
- diventare una SPA complessa
- introdurre orchestrazione non necessaria
- nascondere la differenza tra config e runtime

## 4. Regole tecniche
Preferire:
- FastAPI
- Jinja templates
- CSS semplice
- rendering server-side
- wrapper script piccoli e leggibili
- integrazioni esplicite con `docker compose`, `systemctl` e file YAML

Evitare salvo motivo forte:
- JavaScript complesso
- frontend framework pesanti
- nuove dipendenze per rifiniture marginali
- overengineering
- refactor massivi non richiesti da un problema reale

## 5. Regole di modifica
Quando si modifica il progetto:

1. fare cambi piccoli e reversibili
2. non rompere il setup gia funzionante
3. non cambiare comportamento operativo senza motivo chiaro
4. non introdurre feature non richieste dentro patch di manutenzione
5. aggiornare la documentazione quando cambia il comportamento reale

## 6. Regole operative
- backup prima delle scritture critiche
- restart separato dal salvataggio config
- niente shell arbitraria dalla UI
- azioni operative sempre esplicite
- output utile al debug reale
- LAN-first come scenario principale

## 7. Regole UI
La UI deve restare:
- leggibile
- concreta
- orientata al troubleshooting
- utile anche senza conoscere il codice

Da evitare:
- interfacce troppo astratte
- wizard inutili
- automazioni opache
- stato nascosto o ambiguo

## 8. Regole documentazione
La documentazione deve essere:
- eseguibile
- aggiornata
- indipendente dall'host personale di chi scrive
- basata su placeholder chiari
- senza salti logici

Ogni guida deve spiegare:
- dove cambiare path
- dove cambiare IP
- dove cambiare porte
- quali limiti attuali esistono davvero

## 9. Filosofia finale
- semplice batte sofisticato
- robusto batte elegante
- documentato batte implicito
- osservabile batte magico
