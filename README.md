# 🔥 Reddit Intelligence & Recommendation System

An AI-powered backend system that analyzes Reddit data and provides **intelligent recommendations, trending insights, and user interaction features** using Machine Learning and API integration.

---

## 🚀 Project Overview

This project is a full-stack backend system designed to:

* Fetch Reddit data using API
* Analyze trending topics
* Cluster similar posts using ML
* Generate recommendations
* Handle user interactions (likes, comments, posts)

It combines **NLP + Clustering + Association Rules + FastAPI** to simulate a real-world intelligent Reddit engine.

---

## 🧠 Core Features

* 🔍 Query-based Reddit recommendation system
* 📈 Trending topic detection
* 🤖 Clustering using Machine Learning
* 🔗 Association rule mining for related topics
* ❤️ Like & comment system
* 📝 Post creation and media handling
* 🔐 Authentication (JWT-based)
* ⚡ FastAPI backend with modular architecture

---

## ⚙️ Tech Stack

* Python
* FastAPI
* SQLite (reddisense.db)
* Scikit-learn
* Pandas
* Requests
* RapidAPI (Reddit Data)

---

## 📂 Project Structure

```id="proj-structure"
backend/
│
├── crud/
│   ├── comment_crud.py
│   ├── like_crud.py
│   └── post_crud.py
│
├── models/
│   ├── clustering.py
│   └── association_rules.py
│
├── routers/
│   ├── auth.py
│   ├── comments.py
│   ├── likes.py
│   ├── media.py
│   └── posts.py
│
├── schemas/
│   ├── schemas.py
│   └── social_schemas.py
│
├── services/
│   ├── reddit_service.py
│   ├── trending_service.py
│   └── recommendation_service.py
│
├── config.py
├── database.py
├── main.py
│
├── test_auth.py
├── test_reddit.py
├── test.jpg
│
├── reddisense.db
├── requirements.txt
├── .env
│
├── frontend/
│   └── index.html
│
└── uploads/
```

---

## 🔑 Environment Variables

Create a `.env` file:

```id="env-config"
RAPIDAPI_KEY=your_api_key
RAPIDAPI_HOST=your_api_host
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

## ▶️ How to Run the Project

### 1. Clone Repository

```id="clone"
git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
cd YOUR_REPO/backend
```

### 2. Create Virtual Environment

```id="venv"
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```id="install"
pip install -r requirements.txt
```

### 4. Start Server

```id="run"
uvicorn main:app --reload
```

### 5. Access API Docs

```id="docs"
http://127.0.0.1:8000/docs
```

---

## 🧠 System Architecture

```id="architecture"
User Query
    ↓
Recommendation Service
    ↓
Clustering + Association Rules
    ↓
Trending Service
    ↓
Reddit API (RapidAPI)
    ↓
Ranked Top Posts
```

---

## 🤖 Machine Learning Components

### 🔹 Clustering

* Groups similar Reddit posts
* Helps map user query to topic

### 🔹 Association Rules

* Finds relationships between topics
* Example: AI → MachineLearning

### 🔹 Recommendation Engine

* Combines clustering + trending score
* Returns top 10 relevant posts

---

## 📊 Trending Logic

```id="trend-formula"
Trending Score = (0.6 × Upvotes) + (0.4 × Comments)
```

---

## 🔐 Authentication Flow

* User login → JWT token generated
* Token required for protected routes
* Secured endpoints via FastAPI

---

## 🧪 Testing

Run test files:

```id="test"
python test_reddit.py
python test_auth.py
```

---

## 🖥️ Frontend

* Simple UI available in:

```id="frontend-path"
frontend/index.html
```

---

## 📦 API Modules

### 🔹 Routers

* Auth
* Posts
* Likes
* Comments
* Media

### 🔹 Services

* Reddit API integration
* Trending analysis
* Recommendation engine

### 🔹 CRUD

* Database operations for social features

---

## 🔥 Key Highlights

* Real-time Reddit data integration
* Modular backend architecture
* ML-powered recommendation system
* End-to-end API development
* Production-ready structure

---

## 🎯 Future Improvements

* BERT-based semantic search
* Personalized recommendations
* Real-time streaming data
* Advanced dashboard visualization

---

## 👩‍💻 Author

Vaishnavi Reddy

