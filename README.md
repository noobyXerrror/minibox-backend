# MiniBox Backend 🧾

A lightweight **payroll and attendance** system inspired by SalaryBox — built with Django and PostgreSQL.

> ⚡ Built in 48 hours to demonstrate backend skills for SalaryBox (YC S21)

---

## 🚀 Features (In Progress)

- ✅ Django setup with PostgreSQL
- ✅ Environment variable support
- ✅ Admin dashboard via Django Admin
- ✅ Employee model with user linking
- ✅ API to create employees (only non-employee users appear in dropdown)
- ✅ HR can manually type email to create employee
- 🚧 Attendance model (in progress)
- 🚧 Payroll generation logic (**coming soon**)
- 🚧 REST API for salaries

---

## 🛠 Tech Stack

- **Backend**: Django (Python)
- **Database**: PostgreSQL
- **Admin Panel**: Django Admin
- **Environment Management**: `python-dotenv`
- **Version Control**: Git + GitHub

---

## 🧪 Setup Locally

```bash
git clone https://github.com/YOUR_USERNAME/minibox-backend.git
cd minibox-backend

python -m venv env
source env/bin/activate   # On Windows: env\Scripts\activate

pip install -r requirements.txt
