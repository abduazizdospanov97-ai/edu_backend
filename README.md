# EduCRM — O'quv markaz boshqaruv tizimi

## Tizim talablari
- Python 3.10+
- Node.js 18+

---

## Backend ishga tushurish

```bash
cd backend

# Virtual muhit yaratish
python -m venv venv
venv\Scripts\activate   # Windows
# source venv/bin/activate  # Linux/Mac

# Kutubxonalar o'rnatish
pip install -r requirements.txt

# Ma'lumotlar bazasini yaratish
python manage.py migrate

# Superuser yaratish
python manage.py createsuperuser

# Serverni ishga tushurish
python manage.py runserver
```

Backend `http://localhost:8000` da ishlaydi.
Admin panel: `http://localhost:8000/admin/`

---

## Frontend ishga tushurish

```bash
cd frontend

# Paketlarni o'rnatish
npm install

# Development server
npm run dev
```

Frontend `http://localhost:3000` da ishlaydi.

---

## API manzillari

| Endpoint | Tavsif |
|----------|--------|
| `POST /api/auth/login/` | Tizimga kirish |
| `GET /api/students/` | Talabalar ro'yxati |
| `GET /api/groups/` | Guruhlar |
| `GET /api/teachers/` | O'qituvchilar |
| `GET /api/payments/` | To'lovlar |
| `GET /api/attendance/` | Davomat |
| `GET /api/tests/` | Testlar |
| `GET /api/dashboard/stats/` | Statistika |
| `GET /api/debtors/` | Qarzdorlar |
