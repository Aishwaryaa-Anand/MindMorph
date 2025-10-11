# MindMorph - AI-Powered Personality Analysis Platform

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![React](https://img.shields.io/badge/React-18.0+-61DAFB.svg)
![Flask](https://img.shields.io/badge/Flask-3.0+-000000.svg)
![MongoDB](https://img.shields.io/badge/MongoDB-Latest-47A248.svg)
![ML Accuracy](https://img.shields.io/badge/ML%20Accuracy-80.36%25-success.svg)

A comprehensive web application that predicts MBTI personality types using advanced machine learning techniques. Analyzes personality through questionnaires, text analysis, and social media profiles.

---

## 🎯 Key Features

### Three Analysis Modules

#### 1. Scenario-Based Questionnaire
- 20 carefully crafted real-life scenarios
- ML-enhanced scoring with Random Forest classifier
- Interactive UI with progress tracking
- **Accuracy: 75%+**

#### 2. Text Analysis
- Analyze any written text (journals, essays, blogs)
- Minimum 100 characters, 500+ recommended
- BERT + CountVectorizer + Linguistic feature extraction
- **Accuracy: 80.36%** ⭐

#### 3. Twitter/Social Media Analysis
- Analyze personality from tweets
- Hybrid system: Real Twitter API + Professional Mock API
- Stores analyzed tweets in database
- Same 80.36% ML model
- **Accuracy: 80.36%**

### Additional Features
- 📊 **History Tracking** - View all past analyses
- 📄 **PDF Export** - Download detailed reports
- 🔐 **Authentication** - Secure JWT-based login
- 🎨 **Modern UI** - Beautiful gradient design
- 🔄 **Real-time Analysis** - Instant results
- 💾 **Data Persistence** - MongoDB storage
- 🎭 **16 MBTI Types** - Complete personality profiles

---

<!-- ## 🧠 Machine Learning Architecture

### Model Overview

Our system uses **4 binary ensemble classifiers** instead of a single 16-class classifier, significantly improving accuracy.

#### Architecture Diagram
Input Text
↓
Feature Extraction (5,788 total features)
├─→ BERT Embeddings (768 features)
├─→ CountVectorizer (5,000 features)
└─→ Linguistic Patterns (20 features)
↓
4 Binary Classifiers
├─→ Introversion/Extraversion (I/E)
├─→ Intuition/Sensing (N/S)
├─→ Thinking/Feeling (T/F)
└─→ Judging/Perceiving (J/P)
↓
Ensemble Voting (per dimension)
├─→ Logistic Regression
├─→ XGBoost
└─→ Random Forest
↓
Final MBTI Type (e.g., INTJ)

### Technical Details

**Feature Engineering:**
1. **BERT Embeddings (768 dimensions)**
   - Model: `all-MiniLM-L6-v2` (sentence-transformers)
   - Captures semantic meaning and context
   - Pre-trained on large text corpus

2. **CountVectorizer (5,000 dimensions)**
   - Unigrams and bigrams (n-gram range: 1-2)
   - Frequency-based word importance
   - Better than TF-IDF for personality text

3. **Linguistic Features (20 dimensions)**
   - Average word/sentence length
   - Punctuation patterns (!, ?, ..., ,)
   - Personal pronoun usage (I, we, you)
   - Emotional word ratios
   - Abstract vs concrete language

**Classification:**
- 4 separate binary classifiers (one per dimension)
- Each uses soft voting ensemble
- Algorithms: Logistic Regression + XGBoost + Random Forest
- Training: 5 epochs with early stopping

### Training Data

**Dataset Specifications:**
- **Source:** MBTI Personality Types Dataset (Kaggle)
- **Total Profiles:** 2,574 individuals
- **Data Type:** Aggregated Twitter posts per person
- **Average Text Length:** 7,989 characters per profile
- **Distribution:** Balanced across 16 MBTI types (~150-200 per type)

**Data Preprocessing:**
1. Collected 8,675 user profiles from Kaggle
2. Aggregated multiple posts per person (20-50 posts each)
3. Filtered short posts (<100 characters)
4. Balanced classes via undersampling
5. Split: 70% train, 15% validation, 15% test

**Training Environment:**
- Platform: Google Colab (Free GPU - T4)
- Training Time: 30-45 minutes
- Framework: scikit-learn, XGBoost, Transformers

### Accuracy Results

| Dimension | Accuracy | Precision | Recall | F1-Score |
|-----------|----------|-----------|--------|----------|
| I/E | **80.88%** | 0.81 | 0.81 | 0.81 |
| N/S | **83.98%** | 0.84 | 0.84 | 0.84 |
| T/F | **81.91%** | 0.82 | 0.82 | 0.82 |
| J/P | **74.68%** | 0.75 | 0.75 | 0.75 |
| **Overall** | **80.36%** | 0.81 | 0.80 | 0.80 |

**Performance Comparison:**
- Previous systems: 55-65% accuracy (16-class)
- Our approach: 80.36% accuracy (4 binary classifiers)
- Improvement: +15-25 percentage points

--- -->

## 🛠️ Tech Stack

### Frontend
- **React** 18.2.0 - UI framework
- **React Router** v6 - Navigation
- **Axios** - HTTP client
- **Tailwind CSS** - Styling
- **jsPDF** - PDF generation
- **React Hot Toast** - Notifications

### Backend
- **Flask** 3.0 - Web framework
- **Python** 3.10+ - Programming language
- **Flask-JWT-Extended** - Authentication
- **Flask-CORS** - Cross-origin support
- **PyMongo** - MongoDB driver
- **Werkzeug** - Security utilities

### Machine Learning
- **scikit-learn** 1.3+ - ML algorithms
- **XGBoost** 2.0+ - Gradient boosting
- **Transformers** 4.30+ - BERT models
- **sentence-transformers** 2.2+ - Embeddings
- **pandas** - Data manipulation
- **numpy** - Numerical computing

### Database
- **MongoDB** 6.0+ - NoSQL database
- Collections: users, questionnaire_predictions, text_predictions, twitter_predictions

### APIs
- **Twitter API v2** (Optional) - Real tweet fetching
- **Mock API** (Built-in) - Demo profiles

---

## 📦 Installation & Setup

### Prerequisites
```bash
# Required Software
- Python 3.10 or higher
- Node.js 16 or higher
- MongoDB 6.0 or higher
- Git

# Check versions
python --version
node --version
mongod --version
Step 1: Clone Repository
bashgit clone https://github.com/yourusername/mindmorph.git
cd mindmorph
Step 2: Backend Setup
bash# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
Create: backend/.env
env# MongoDB Configuration
MONGODB_URI=mongodb://localhost:27017/mindmorph

# JWT Secret (Generate a secure random string)
JWT_SECRET_KEY=your_super_secret_jwt_key_change_this

# Twitter API (Optional)
TWITTER_BEARER_TOKEN=your_twitter_bearer_token_here
USE_REAL_TWITTER_API=false

# Flask Configuration
FLASK_ENV=development
bash# Start MongoDB (if not running)
# Windows:
mongod --dbpath C:\data\db
# Mac/Linux:
sudo systemctl start mongodb

# Run backend server
python run.py

# Backend should start on http://localhost:5000
Step 3: Frontend Setup
bash# Open new terminal
cd frontend

# Install dependencies
npm install

# Start development server
npm start

# Frontend opens at http://localhost:3000
Step 4: Verify Installation

Open browser: http://localhost:3000
Create an account (Sign Up)
Login with credentials
You should see the home page with 3 modules


🚀 Usage Guide
1. Authentication
Sign Up:

Click "Sign Up" on login page
Enter name, email, password
Click "Create Account"

Login:

Enter email and password
Click "Login"
Redirects to home page

2. Questionnaire Module
Steps:

Click "Scenario Questionnaire" on home
Read each scenario carefully
Choose A or B for each question
Use "Next" and "Back" to navigate
Click "Get Results" after answering all 20
View detailed results with insights
Download PDF report (optional)

3. Text Analysis Module
Steps:

Click "Text Analysis" on home
Paste your text (minimum 100 characters)
Character counter shows progress
Click "Analyze Text"
View results with confidence scores
See keywords that influenced prediction
Download PDF report

Tips:

More text = better accuracy
Use authentic, personal writing
Recommended: 500+ characters

4. Twitter Analysis Module
Steps:

Click "Twitter Analysis" on home
Enter Twitter username (without @)

Available: elonmusk, billgates, naval, sundarpichai, barackobama


Click "Analyze"
View results with profile information
See analyzed tweets stored in database
Download PDF report

5. View History
Steps:

From home page, click any history card
See all past analyses for that module
Click any result to view full details


📊 API Documentation
Authentication Endpoints
POST /api/auth/signup
Register new user.
Request:
json{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "securepassword123"
}
Response:
json{
  "message": "User created successfully",
  "userId": "507f1f77bcf86cd799439011"
}
POST /api/auth/login
Login user and get JWT token.
Request:
json{
  "email": "john@example.com",
  "password": "securepassword123"
}
Response:
json{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": "507f1f77bcf86cd799439011",
    "name": "John Doe",
    "email": "john@example.com"
  }
}
Text Analysis Endpoints
POST /api/text/predict
Analyze text and predict MBTI.
Headers: Authorization: Bearer <token>
Request:
json{
  "text": "Your text here (minimum 100 characters)..."
}
Response:
json{
  "predictionId": "507f1f77bcf86cd799439013",
  "mbtiType": "ENFP",
  "confidence": {
    "IE": 0.82,
    "NS": 0.88,
    "TF": 0.75,
    "JP": 0.79
  },
  "keywords": ["creative", "people", "ideas"],
  "textLength": 1523,
  "insights": {...}
}
Twitter Analysis Endpoints
POST /api/twitter/analyze
Analyze Twitter profile.
Headers: Authorization: Bearer <token>
Request:
json{
  "username": "elonmusk"
}
Response:
json{
  "predictionId": "507f1f77bcf86cd799439014",
  "username": "elonmusk",
  "mbtiType": "ENTJ",
  "confidence": {...},
  "tweetCount": 20,
  "source": "mock_api",
  "insights": {...}
}

📁 Project Structure
MindMorph/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── ml_models/
│   │   │   ├── text_classifier.py
│   │   │   ├── questionnaire/
│   │   │   │   └── random_forest_model.pkl
│   │   │   └── text/
│   │   │       ├── IE_aggregated_ensemble.pkl
│   │   │       ├── IE_aggregated_vectorizer.pkl
│   │   │       ├── NS_aggregated_ensemble.pkl
│   │   │       ├── NS_aggregated_vectorizer.pkl
│   │   │       ├── TF_aggregated_ensemble.pkl
│   │   │       ├── TF_aggregated_vectorizer.pkl
│   │   │       ├── JP_aggregated_ensemble.pkl
│   │   │       └── JP_aggregated_vectorizer.pkl
│   │   ├── routes/
│   │   │   ├── auth.py
│   │   │   ├── questionnaire.py
│   │   │   ├── text.py
│   │   │   ├── twitter.py
│   │   │   └── twitter_mock_api.py
│   │   ├── services/
│   │   │   ├── mbti_service.py
│   │   │   ├── twitter_hybrid_service.py
│   │   │   ├── twitter_real_api_client.py
│   │   │   └── twitter_mock_api_client.py
│   │   └── models/
│   │       └── user.py
│   ├── data/
│   │   ├── mbti_insights.json
│   │   ├── mock_twitter_data.json
│   │   └── training/
│   │       ├── aggregated_binary/
│   │       └── analysis_plots/
│   ├── .env
│   ├── requirements.txt
│   └── run.py
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   │   ├── auth/
│   │   │   ├── questionnaire/
│   │   │   └── shared/
│   │   ├── pages/
│   │   │   ├── Home.jsx
│   │   │   ├── questionnaire/
│   │   │   │   ├── Test.jsx
│   │   │   │   ├── Result.jsx
│   │   │   │   └── History.jsx
│   │   │   ├── text/
│   │   │   │   ├── Analyze.jsx
│   │   │   │   ├── Result.jsx
│   │   │   │   └── History.jsx
│   │   │   └── twitter/
│   │   │       ├── Analyze.jsx
│   │   │       ├── Result.jsx
│   │   │       └── History.jsx
│   │   ├── services/
│   │   │   ├── questionnaireService.js
│   │   │   ├── textService.js
│   │   │   └── twitterService.js
│   │   ├── utils/
│   │   │   └── pdfGenerator.js
│   │   ├── contexts/
│   │   │   └── AuthContext.jsx
│   │   └── App.jsx
│   └── package.json
│
└── README.md

🔒 Security Features
Authentication

JWT Tokens: Secure, stateless authentication
Password Hashing: Werkzeug security with salt
Protected Routes: All analysis endpoints require authentication
CORS Protection: Configured for specific origins

Data Privacy

User passwords never stored in plain text
JWT tokens stored in localStorage (client-side)
MongoDB queries use user-specific filters
No data sharing with third parties


🐛 Troubleshooting
Common Issues
1. Backend won't start
bash# Activate virtual environment
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Check MongoDB is running
mongod --dbpath C:\data\db
2. Frontend won't start
bash# Reinstall dependencies
rm -rf node_modules package-lock.json
npm install
3. ML Models not loading
bash# Check models exist
ls backend/app/ml_models/text/
# Should see 8 .pkl files
4. Authentication errors
bash# Check JWT_SECRET_KEY in .env
# Login again to get fresh token

🎮 Demo Data
Mock Twitter Profiles

elonmusk - Tech entrepreneur

Expected: ENTJ/INTJ
Tweets: Innovation, Mars, AI


billgates - Philanthropist

Expected: INTJ
Tweets: Health, Climate, Education


naval - Philosopher

Expected: INTP
Tweets: Wealth, Philosophy, Startups


sundarpichai - Google CEO

Expected: ISTJ/INTJ
Tweets: Technology, Collaboration


barackobama - Former President

Expected: ENFJ
Tweets: Leadership, Hope, Service




🚀 Deployment
Production Setup
Backend (Flask):
bash# Use Gunicorn
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 run:app
Frontend (React):
bash# Build for production
npm run build
# Deploy to Vercel/Netlify/AWS
Database:

Use MongoDB Atlas (cloud)
Or self-host on VPS


🎓 Academic Context
Project Information:

Type: Final Year Bachelor's Project
Domain: Machine Learning, Web Development
Duration: 6 months
Team Size: 3 members

Learning Outcomes:

Full-stack web development
Machine learning deployment
RESTful API design
Database optimization
UI/UX design


📚 References
Datasets

MBTI Dataset: Kaggle - MBTI Personality Types 500
8,675 users with aggregated posts

Libraries

React: https://react.dev/
Flask: https://flask.palletsprojects.com/
scikit-learn: https://scikit-learn.org/
Transformers: https://huggingface.co/

MBTI Resources

Myers & Briggs Foundation: https://www.myersbriggs.org/
16Personalities: https://www.16personalities.com/


🤝 Contributing
This is an academic project. Feedback welcome!
Contact:

Email: [your-email@example.com]
GitHub Issues: [repository-url]/issues


📝 License
Developed for academic purposes. Not licensed for commercial use.