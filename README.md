# 📦 Network Backup Tool

A modern network configuration backup solution built with FastAPI and Vue 3. This tool allows you to back up configurations of network devices, with a sleek frontend for managing and monitoring all your devices.

---

## ⚙️ Tech Stack

### 🔙 Backend
- **Python 3**
- **FastAPI** — high-performance Python web framework for APIs
- **Netmiko** — simplifies SSH connections to network devices

### 🌐 Frontend
- **Vue 3**
- **TypeScript**
- **TailwindCSS**

---

## 🚀 Features

- 🔐 Session-based authentication
- 🔧 Add, view, edit, delete network devices
- 📤 Backup device configuration
- 🧾 Track backup history per device
- 🛡️ Secure API with session validation
- 📊 Responsive and modern UI

---

## 📂 Project Structure

```
network-backup/
├── backend/         # FastAPI backend
│   ├── main.py
│   ├── routes/
|   |   ├── auth.py
|   |   ├── device.py
|   |   ├── backup.py
|   ├── models.py
│   ├── crud.py
│   ├── database.py
│   ├── schemas.py
│   └── device.py
├── frontend/        # Vue 3 frontend
│   ├── src/
│   ├── public/
│   └── vite.config.ts
└── README.md
```

---

## 🛠️ Setup Instructions

### 📦 Backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```


### 🌐 Frontend

```bash
cd frontend
npm install
npm run dev
```
