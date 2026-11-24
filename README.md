# Hospital Management Backend 

## Features
1. Doctor management: create, list, retrieve, update and delete doctors.
2. Appointment management: create, list, retrieve, update and delete appointments.

Business rules: a doctor cannot have two appointments in the same date/time slot (409 Conflict). A doctor with existing appointments cannot be deleted (409 Conflict).

## Architecture
Request -> middleware -> route/controller -> service -> domain/repository -> SQLite.
- `routes/`: thin HTTP handlers; no SQL or business rules.
- `services/`: use cases, validation and business rules.
- `domain/`: framework-independent entities.
- `repositories/`: all SQLite access.
- `config.py`: environment configuration.
- `errors.py`: centralized RFC 9457-style problem response.
- `tests/`: automated integration tests using Flask's test client.

Dependencies are passed into services and wired once in `create_app()`.

## Run on Windows CMD / VS Code
```bat
cd hospital_backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python run.py
```
Server: `http://127.0.0.1:5000`

## Run tests (Postman automation replacement)
In another terminal with `.venv` activated:
```bat
pytest -v
```
The Flask test client automatically sends requests through the app. Tests cover CRUD lifecycles and failure cases. No manual Postman clicking is needed; tests run repeatedly with one command.

## Endpoints
| Method | Endpoint | Action |
|---|---|---|
| POST | `/api/doctors` | Create doctor |
| GET | `/api/doctors` | List doctors |
| GET | `/api/doctors/{id}` | Read doctor |
| PUT | `/api/doctors/{id}` | Update doctor |
| DELETE | `/api/doctors/{id}` | Delete doctor |
| POST | `/api/appointments` | Create appointment |
| GET | `/api/appointments` | List appointments |
| GET | `/api/appointments/{id}` | Read appointment |
| PUT | `/api/appointments/{id}` | Update appointment |
| DELETE | `/api/appointments/{id}` | Delete appointment |
| GET | `/health` | Health check |

## Example JSON
Doctor:
```json
{"name":"Dr. Ayesha Rahman","specialty":"Cardiology","phone":"01700000000"}
```
Appointment:
```json
{"doctor_id":1,"patient_name":"Mahi","appointment_date":"2026-12-02","appointment_time":"11:00","reason":"Regular checkup"}
```

## Status codes and error handling
201 create (with `Location`), 200 read/list/update, 204 delete, 404 missing resource, 409 business-rule conflict, 422 field validation. Every response includes `X-Request-ID`; errors use `application/problem+json`. Unexpected exception details go to logs, not the client.

## Test cases
- Doctor full CRUD, missing doctor, invalid doctor fields, deletion blocked by existing appointments.
- Appointment full CRUD, duplicate doctor slot, invalid date/time, unknown doctor, unknown appointment.

`.env.example` is committed; `.env` and database files are ignored by Git. This is an educational backend, not production-ready for real patient data; authentication, role-based authorization, audit retention and privacy controls are still required.

AI-use disclosure: AI assistance was used to scaffold the project. Run the tests, inspect the code and make sure you can explain every module and the request lifecycle before submission.
