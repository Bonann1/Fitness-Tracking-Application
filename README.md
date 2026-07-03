# Fitness Tracking Application

**Studente:** Mattia Bonanni
**Tipo di progetto:** Full-Stack Web Application
**Framework:** Django 5
**Traccia:** 5 — Fitness Tracking Application (PPM Back-end 2026)

## Descrizione

Applicazione web per il tracciamento dell'attività fisica. Ogni utente standard può
registrare i propri workout (con esercizi, serie, ripetizioni, peso, distanza),
definire obiettivi (generici o "a metrica" con valore target e deadline) e
inserire progress entry collegate agli obiettivi per misurarne l'andamento nel
tempo. Il ruolo coach può consultare i dati dei propri clienti assegnati e
inviare loro feedback testuali.

## Funzionalità implementate

### Utente standard (`standard`)
- Registrazione, login, logout, modifica profilo (bio, avatar)
- CRUD completo sui propri **workout** con esercizi multipli (M2M `through` con `WorkoutExercise`)
- Catalogo di tipi di esercizio (forza, cardio, flessibilità) gestito da admin
- CRUD completo sui propri **goal** (generici o a metrica con `target_value` + `deadline`)
- CRUD completo sui propri **progress entry**, collegabili a uno specifico goal
- Dashboard con grafico settimanale dei workout (Chart.js)
- Detail del goal a metrica con grafico di progressione vs valore target
- Cronologia workout ordinata per data e pagina di riepilogo profilo con feedback ricevuti dal coach

### Coach (`coach`)
- Dashboard dedicata con lista dei clienti assegnati e ultimi feedback inviati
- Pagina "I miei clienti" e dettaglio cliente con workout, goal, progress entry, feedback
- Creazione di feedback testuali verso ciascun cliente assegnato
- Modifica dei workout dei clienti assegnati (proprietà del workout preservata)

### Admin / superuser
- Pannello Django admin completo (utenti, assegnazioni coach, esercizi, workout)

## Stack tecnico
- Django 5 con custom user model (`users.CustomUser` extends `AbstractUser`)
- 4 app: `users`, `workouts`, `goals`, `progress`
- Bootstrap 5 + Bootstrap Icons + Chart.js (via CDN)
- SQLite (`db.sqlite3`) committato pre-popolato
- WhiteNoise per file statici in produzione, Gunicorn come web server

## Setup locale

```bash
git clone <repo-url>
cd Fitness-Tracking-Application
python3 -m venv venv
source venv/bin/activate          # su Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Apri `http://127.0.0.1:8000/`. Il file `db.sqlite3` è incluso nel repository e
**contiene già i dati demo** (esercizi, workout, goal, progress entry, feedback).
Per rigenerarli da zero:

```bash
python manage.py seed_db
```

## Database demo

File: `db.sqlite3` (incluso nel repository).
Contiene utenti, assegnazioni coach, 10 tipi di esercizio, 5 workout completi
con esercizi associati, goal generico + goal a metrica con 5 progress entry, e
2 feedback del coach.

## Account demo

| Username | Password | Ruolo |
|---|---|---|
| `admin_demo` | `admin12345` | superuser (admin) |
| `coach_demo` | `coach12345` | coach |
| `user_demo`  | `user12345`  | standard user (assegnato a `coach_demo`) |
| `user_demo2` | `user12345`  | standard user (assegnato a `coach_demo`) |

## Deployment

URL online: **`<inserire qui l'URL Render dopo il deploy>`**


Il progetto è pronto per il deploy su Render (free tier):

1. Fork / push del repo su GitHub.
2. Su [Render](https://render.com) crea un **Web Service** collegato al repo.
3. Configura:
   - **Build Command:** `./build.sh`
   - **Start Command:** `gunicorn fitness_tracker.wsgi:application`
   - **Environment:** Python 3.11+
   - Variabili d'ambiente:
     - `DJANGO_SECRET_KEY` = una stringa random sicura
     - `DJANGO_DEBUG` = `False`
     - `DJANGO_ALLOWED_HOSTS` = `.onrender.com,localhost,127.0.0.1`
     - `DJANGO_CSRF_TRUSTED_ORIGINS` = `https://<nome-app>.onrender.com`
4. Deploy. Il `db.sqlite3` pre-popolato viene incluso nello slug, quindi i demo
   account funzioneranno subito anche online.

> Nota: il filesystem di Render free è effimero. Eventuali dati inseriti online
> non sopravvivono ai redeploy. Per la valutazione è sufficiente perché tutti i
> dati demo sono già nel `db.sqlite3` committato.

## Scenario di test (browser)

1. Vai sull'URL del deploy (o `http://127.0.0.1:8000/` in locale).
2. **Login come `user_demo / user12345`** → la dashboard mostra il grafico
   settimanale dei workout, i goal attivi e gli ultimi progress.
3. Menu **Workout**:
   - Crea un nuovo workout (titolo, data, durata).
   - Apri il detail, aggiungi un esercizio con serie/ripetizioni o distanza
     (la validazione richiede almeno uno dei due).
   - Modifica e poi elimina il workout.
4. Menu **Obiettivi**: crea un goal "a metrica" con `target_value` e `deadline`.
   Apri il detail per vedere il grafico (inizialmente vuoto).
5. Menu **Progresso**: aggiungi una entry collegata al goal appena creato.
   Torna al detail del goal e verifica che il grafico si aggiorni.
6. **Logout**. **Login come `coach_demo / coach12345`** → dashboard coach con
   lista clienti.
7. "I miei clienti" → apri `user_demo` → "Lascia un feedback".
8. **Test di permessi negati**: come `user_demo2`, tenta di aprire un URL come
   `/workouts/<id-di-user_demo>/edit/`. L'app reindirizza alla dashboard con
   un messaggio di errore.

## Requisiti tecnici soddisfatti

| Requisito | Implementazione |
|---|---|
| ≥ 2 Django app | 4 app: `users`, `workouts`, `goals`, `progress` |
| ≥ 2 relazioni | ForeignKey multiple + Many-to-Many `Workout↔ExerciseType` con through `WorkoutExercise` |
| Custom user model | `users.CustomUser(AbstractUser)` con `role`, `bio`, `avatar` |
| ≥ 2 ruoli | `standard` e `coach` con permessi enforced in CBV |
| Class-based view | `ListView`, `DetailView`, `CreateView`, `UpdateView`, `DeleteView` ovunque |
| Validazione input | `ModelForm` con metodi `clean()` custom |
| CRUD completa | Workout, Goal, ProgressEntry |
| DB SQLite popolato | `db.sqlite3` committato + comando `seed_db` |
| Migrazioni | Presenti per tutte le app |
| Deployment | Render (vedi sezione Deployment) |
