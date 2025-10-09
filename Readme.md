# 🧠 MindMorph

**MindMorph** is a full-stack web application for **MBTI (Myers-Briggs Type Indicator)** personality assessment using three intelligent prediction methods — Questionnaire, Text, and Twitter Analysis.

---

## 🚀 Overview

MindMorph predicts your MBTI personality type using **three distinct assessment methods**:

| Method | Description | Accuracy |
|--------|--------------|-----------|
| 📝 **Scenario Questionnaire** | 20 situational questions analyzing behavioral preferences | ~75% |
| 💬 **Text Analysis** | ML-powered prediction from user-submitted text samples | ~80% |
| 🐦 **Twitter Analysis** | Personality prediction from Twitter activity | ~80% |

Each assessment provides:
- 4-letter MBTI type (e.g., INFP, ESTJ)
- Confidence scores for each MBTI dimension (I/E, N/S, T/F, J/P)
- Personality insights, career recommendations, and compatibility matches
- Optional **PDF report generation**

---

## 🧩 Technology Stack

### 🖥️ Frontend
- **React 18** with **Vite**
- **React Router v6** for client-side navigation
- **Axios** for API calls with JWT authentication
- **Tailwind CSS** for responsive UI
- Development port: `5173` (or `3000` for production)

### ⚙️ Backend
- **Flask** (Python web framework)
- **Flask-JWT-Extended** for authentication (7-day token expiry)
- **Flask-CORS** for cross-origin support
- **PyMongo** for MongoDB integration
- **bcrypt** for password hashing
- Runs on port: `5000`

### 🧠 Database & Machine Learning
- **MongoDB** — `mindmorph` database for data persistence  
- **scikit-learn** — text classification models  
- **Dataset** — `mbti_1.csv` (training data for text-based predictions)

---

## 🏗️ Architecture
```
┌─────────────────┐       ┌──────────────────┐      ┌─────────────┐
│ React Frontend  │ ───▶  │ Flask Backend   │ ───▶ │ MongoDB     │
│ (Port 5173)     │ REST  | (Port 5000)      │ CRUD │ mindmorph   │
│ + JWT Auth      │       │ API + ML Logic   │      │ Database    │
└─────────────────┘       └──────────────────┘      └─────────────┘
```

The app follows a **three-tier architecture** separating:
- Presentation (React SPA)
- Business logic (Flask API + services)
- Data persistence (MongoDB)

---

## 📁 Project Structure
```
MindMorph/
├── backend/
│ ├── app/
│ │ ├── init.py # Flask app factory, DB setup
│ │ ├── routes/ # API routes (blueprints)
│ │ │ ├── auth.py # /api/auth endpoints
│ │ │ ├── questionnaire.py # /api/questionnaire endpoints
│ │ │ ├── text.py # /api/text endpoints
│ │ │ └── twitter.py # /api/twitter endpoints
│ │ └── services/ # Business logic
│ │ ├── auth_service.py
│ │ ├── questionnaire_service.py
│ │ └── mbti_service.py
│ └── run.py # Entry point
│
└── frontend/
└── src/
├── App.jsx # Root component
├── contexts/AuthContext.jsx # Global auth management
├── components/ # Reusable UI
└── pages/ # Main pages
```
---

## ⚙️ Setup Instructions

### 🧾 Prerequisites
- **Python 3.8+**
- **Node.js 16+**
- **MongoDB** (local or cloud)

---

### 🔧 Backend Setup

```bash
cd backend
```
 Create and activate virtual environment
```
python -m venv venv
source venv/bin/activate  # (Windows: venv\Scripts\activate)
```
 Install dependencies
```
pip install -r requirements.txt
```
 Create a .env file in backend/ with:
```
MONGO_URI=mongodb://localhost:27017/mindmorph
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret-key
```
 Run the backend:
```
python run.py
```
Backend runs on http://localhost:5000
---
### 💻 Frontend Setup
```
cd frontend
```
 Install dependencies
```
npm install
```
 Start development server
```
npm run dev
```
Frontend runs on http://localhost:5173
---



## 🔒 Authentication Flow
- User signs up / logs in → backend validates and returns JWT
- Token stored in localStorage
- AuthContext automatically attaches JWT to every Axios request
- ProtectedRoute guards private pages
- Token verified on reload via /api/auth/verify

## 🧭 Assessment Flow
- User selects an assessment type (Questionnaire, Text, Twitter)
- Completes input form → data sent to backend
- Backend predicts MBTI → stores result in MongoDB
- Frontend fetches result and displays insights
- Optionally export result as PDF

## 🌟 Features

- ✅ Multi-method personality assessment
- ✅ JWT-based secure authentication
- ✅ MBTI insights: strengths, careers, compatibility
- ✅ PDF report generation
- ✅ Prediction history tracking
- ✅ Responsive Tailwind UI
- ✅ ML-based text classification
- ✅ Twitter data caching with TTL



## 🤝 Contributors
Aishwaryaa Anand — Developer & Maintainer
📧 aishwaryaa.anand@gmail.com
