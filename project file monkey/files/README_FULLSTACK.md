# 🏭 Rejection Rate Analytics - Full Stack Application

**Complete Full Stack Web Application with PostgreSQL Database**

A production-ready system for analyzing and predicting product rejection rates in manufacturing industries using machine learning, PostgreSQL database, Flask backend, and modern JavaScript frontend.

---

## 📁 Project Structure

```
rejection-analytics-fullstack/
│
├── database/
│   └── schema.sql              # PostgreSQL database schema
│
├── backend/
│   ├── app.py                  # Flask server with REST API
│   ├── config.py               # Database configuration
│   ├── database.py             # Database connection handler
│   ├── requirements.txt        # Python dependencies
│   │
│   └── models/
│       ├── batch_model.py      # Batch operations
│       ├── prediction_model.py # ML prediction logic
│       ├── recommendation_model.py # Recommendations
│       └── user_model.py       # User management
│
└── frontend/
    ├── index.html              # Main HTML page
    ├── css/
    │   └── styles.css          # Complete styling
    └── js/
        └── app.js              # Frontend logic & API calls
```

---

## 🚀 Features

### Backend Features
- ✅ **RESTful API** with Flask
- ✅ **PostgreSQL Database** with connection pooling
- ✅ **User Authentication** with session management
- ✅ **CRUD Operations** for batches, predictions, recommendations
- ✅ **ML Prediction Engine** (no external API needed)
- ✅ **Statistics & Analytics** endpoints
- ✅ **Error Handling** and logging

### Frontend Features
- ✅ **Modern Responsive UI** with gradient design
- ✅ **Interactive Dashboard** with real-time stats
- ✅ **Batch Management** with search and filters
- ✅ **AI Prediction Interface** with risk analysis
- ✅ **Recommendations System** with priority management
- ✅ **Modal Forms** for data entry
- ✅ **Toast Notifications** for user feedback

### Database Features
- ✅ **4 Main Tables**: users, batches, predictions, recommendations
- ✅ **Database Views** for statistics
- ✅ **Indexes** for performance
- ✅ **Sample Data** included
- ✅ **Foreign Key Relationships**

---

## 📋 Prerequisites

### Required Software
1. **Python 3.8+** - [Download](https://www.python.org/downloads/)
2. **PostgreSQL 12+** - [Download](https://www.postgresql.org/download/)
3. **Modern Web Browser** (Chrome, Firefox, Edge)

---

## 🔧 Installation & Setup

### Step 1: Install PostgreSQL

**Windows:**
```bash
# Download installer from postgresql.org
# During installation, set password: postgres
# Remember the port (default: 5432)
```

**Mac (using Homebrew):**
```bash
brew install postgresql
brew services start postgresql
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
```

### Step 2: Create Database

```bash
# Login to PostgreSQL
psql -U postgres

# In PostgreSQL prompt:
CREATE DATABASE rejection_analytics;
\c rejection_analytics
\q
```

### Step 3: Initialize Database Schema

```bash
# Navigate to database folder
cd database

# Run schema file
psql -U postgres -d rejection_analytics -f schema.sql
```

You should see:
```
CREATE TABLE
CREATE TABLE
CREATE TABLE
CREATE TABLE
INSERT 0 3
INSERT 0 5
...
```

### Step 4: Setup Backend

```bash
# Navigate to backend folder
cd ../backend

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 5: Configure Database Connection

Edit `backend/config.py` if needed (default values should work):

```python
DB_CONFIG = {
    'host': 'localhost',
    'port': '5432',
    'database': 'rejection_analytics',
    'user': 'postgres',
    'password': 'postgres'  # Change if you set different password
}
```

### Step 6: Start Backend Server

```bash
# Make sure you're in backend folder with venv activated
python app.py
```

You should see:
```
🚀 Starting Rejection Analytics Backend Server...
📊 API Documentation: http://localhost:5000/
 * Running on http://0.0.0.0:5000
```

**Keep this terminal running!**

### Step 7: Start Frontend

**Option A: Using Python HTTP Server (Recommended)**
```bash
# Open NEW terminal
cd frontend
python -m http.server 8000
```

Then open: http://localhost:8000

**Option B: Using any HTTP Server**
```bash
# Using Node.js http-server
npm install -g http-server
cd frontend
http-server -p 8000
```

**Option C: Direct File Opening**
Simply open `frontend/index.html` in your browser, but note that some features may not work due to CORS restrictions.

---

## 🎯 Using the Application

### 1. Access the Application
Open your browser and go to: **http://localhost:8000**

### 2. Login Credentials
The application will auto-login with default credentials:
- **Username:** admin
- **Password:** password123

Other test users:
- operator1 / password123
- supervisor / password123

### 3. Dashboard Features

**Statistics Overview:**
- Total Batches
- Rejected/Accepted Counts
- Rejection Rate
- Recent Predictions
- Shift Analysis

### 4. Managing Batches

**Create New Batch:**
1. Click "Batches" in navigation
2. Click "+ Create New Batch"
3. Fill in all parameters
4. Click "Create Batch"

**Search & Filter:**
- Search by batch number
- Filter by status (accepted/rejected)
- Filter by shift (Morning/Afternoon/Night)

### 5. Making Predictions

**Manual Prediction:**
1. Click "Predict" in navigation
2. Enter batch parameters
3. Click "🔮 Predict Rejection"
4. View results with risk factors

**Predict for Existing Batch:**
1. Go to "Batches" page
2. Click "Predict" button on any batch
3. View prediction results

### 6. Recommendations

**View Recommendations:**
- See all improvement suggestions
- Filter by priority (HIGH/MEDIUM/LOW)
- Filter by status (pending/in_progress/implemented)

**Mark as Implemented:**
- Click "Mark Implemented" on any recommendation
- Status updates automatically

---

## 📊 API Endpoints

### Authentication
```
POST   /api/login           # User login
POST   /api/logout          # User logout
POST   /api/register        # Register new user
```

### Batches
```
GET    /api/batches                      # Get all batches
GET    /api/batches/<id>                 # Get specific batch
POST   /api/batches                      # Create batch
PUT    /api/batches/<id>/status          # Update status
DELETE /api/batches/<id>                 # Delete batch
GET    /api/batches/search?q=term        # Search batches
GET    /api/batches/status/<status>      # Get by status
GET    /api/batches/shift/<shift>        # Get by shift
```

### Predictions
```
POST   /api/predict                      # Make prediction
GET    /api/predictions                  # Get all predictions
GET    /api/predictions/<id>             # Get specific prediction
GET    /api/predictions/batch/<batch_id> # Get batch predictions
GET    /api/predictions/recent           # Get recent predictions
```

### Recommendations
```
GET    /api/recommendations                      # Get all
GET    /api/recommendations/<id>                 # Get specific
POST   /api/recommendations                      # Create new
PUT    /api/recommendations/<id>/status          # Update status
GET    /api/recommendations/priority/<priority>  # Get by priority
```

### Statistics
```
GET    /api/statistics/batches           # Batch statistics
GET    /api/statistics/shift-analysis    # Shift analysis
GET    /api/statistics/prediction-accuracy # Model accuracy
```

---

## 🗃️ Database Schema

### Tables

**users**
- user_id (PK)
- username, email, password_hash
- role (admin/operator/supervisor)
- created_at, last_login

**batches**
- batch_id (PK)
- batch_number (unique)
- 11 manufacturing parameters
- actual_status
- created_by (FK → users)
- timestamps

**predictions**
- prediction_id (PK)
- batch_id (FK → batches)
- predicted_status
- rejection_probability
- acceptance_probability
- prediction_date
- predicted_by (FK → users)

**recommendations**
- recommendation_id (PK)
- category, priority, title
- issue_description, action_plan
- expected_impact, status
- timestamps
- created_by (FK → users)

---

## 🔍 Testing the Application

### Test Scenario 1: Create and Predict
1. Create a new batch with low quality (< 70%)
2. Predict for this batch
3. Should predict "rejected"

### Test Scenario 2: High Quality Batch
1. Create batch with:
   - Quality > 90%
   - Experience > 10 years
   - Good maintenance
2. Should predict "accepted"

### Test Scenario 3: Statistics
1. Create multiple batches
2. Mark some as accepted/rejected
3. Check dashboard for updated stats

---

## 🛠️ Configuration

### Environment Variables (Optional)

Create `.env` file in backend folder:
```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=rejection_analytics
DB_USER=postgres
DB_PASSWORD=your_password
```

### Change Port Numbers

**Backend (Flask):**
Edit `backend/app.py`, line ~290:
```python
app.run(host='0.0.0.0', port=5000, debug=True)
```

**Frontend API URL:**
Edit `frontend/js/app.js`, line 2:
```javascript
const API_BASE_URL = 'http://localhost:5000/api';
```

---

## 🐛 Troubleshooting

### Database Connection Error
```
Error: could not connect to server
```
**Solution:**
- Check PostgreSQL is running: `pg_isready`
- Verify credentials in `config.py`
- Check database exists: `psql -U postgres -l`

### Backend Not Starting
```
ModuleNotFoundError: No module named 'flask'
```
**Solution:**
- Activate virtual environment
- Run: `pip install -r requirements.txt`

### Frontend Can't Connect to Backend
```
Failed to fetch
```
**Solution:**
- Verify backend is running on port 5000
- Check CORS is enabled
- Update API_BASE_URL in app.js

### Port Already in Use
```
Address already in use
```
**Solution:**
- Change port in backend/app.py
- Update frontend API_BASE_URL
- Or kill process using the port

---

## 📈 Performance Tips

1. **Database Indexing**: Already implemented on frequently queried columns
2. **Connection Pooling**: Configured with min=1, max=10 connections
3. **Pagination**: Use limit/offset parameters in API calls
4. **Caching**: Consider Redis for production

---

## 🔒 Security Notes

⚠️ **For Production:**

1. **Change Secret Key** in `backend/app.py`
2. **Use Environment Variables** for sensitive data
3. **Enable HTTPS**
4. **Implement Rate Limiting**
5. **Add Input Validation**
6. **Use bcrypt** for password hashing (currently using SHA256)

---

## 🚀 Deployment

### Deploy to Heroku

```bash
# Backend
heroku create your-app-backend
heroku addons:create heroku-postgresql:hobby-dev
git push heroku main

# Frontend
# Deploy to Netlify, Vercel, or GitHub Pages
```

### Deploy to AWS

1. **RDS** for PostgreSQL
2. **EC2/Elastic Beanstalk** for Flask
3. **S3 + CloudFront** for frontend

---

## 📝 Development

### Add New Feature

1. **Backend**: Add endpoint in `app.py`
2. **Database**: Update schema if needed
3. **Frontend**: Add UI component in `index.html`
4. **JavaScript**: Add function in `app.js`

### Code Structure

- **Models**: Handle database operations
- **API Routes**: Handle HTTP requests
- **Frontend**: Single-page application with vanilla JS

---

## 🧪 Sample Database Queries

```sql
-- Get all high-priority pending recommendations
SELECT * FROM recommendations 
WHERE priority = 'HIGH' AND status = 'pending';

-- Get rejection rate by shift
SELECT shift, 
       COUNT(*) as total,
       COUNT(CASE WHEN actual_status = 'rejected' THEN 1 END) as rejected,
       ROUND(COUNT(CASE WHEN actual_status = 'rejected' THEN 1 END)::numeric / COUNT(*)::numeric * 100, 2) as rejection_rate
FROM batches 
GROUP BY shift;

-- Get prediction accuracy
SELECT * FROM prediction_accuracy;
```

---

## 📚 Tech Stack

### Backend
- **Python 3.8+**
- **Flask 3.0** - Web framework
- **PostgreSQL 12+** - Database
- **psycopg2** - PostgreSQL adapter

### Frontend
- **HTML5**
- **CSS3** with Flexbox/Grid
- **Vanilla JavaScript (ES6+)**
- **Fetch API** for AJAX

### Database
- **PostgreSQL**
- **SQL** with views and indexes

---

## 🎓 Learning Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [PostgreSQL Tutorial](https://www.postgresql.org/docs/)
- [JavaScript MDN](https://developer.mozilla.org/en-US/docs/Web/JavaScript)

---

## 🤝 Support

For issues or questions:
1. Check the troubleshooting section
2. Verify all services are running
3. Check browser console for errors
4. Review server logs

---

## 📄 License

This project is for educational and commercial use.

---

## ✅ Quick Start Checklist

- [ ] Install PostgreSQL
- [ ] Create database: `rejection_analytics`
- [ ] Run schema.sql
- [ ] Install Python dependencies
- [ ] Configure database credentials
- [ ] Start backend server (port 5000)
- [ ] Start frontend server (port 8000)
- [ ] Login with admin/password123
- [ ] Create test batch
- [ ] Make prediction
- [ ] View dashboard statistics

---

**System Status:**
- ✅ Database: PostgreSQL with 4 tables
- ✅ Backend: Flask REST API with 20+ endpoints
- ✅ Frontend: Modern responsive web interface
- ✅ Authentication: Session-based login system
- ✅ ML Prediction: Built-in algorithm (no external API)
- ✅ Complete CRUD operations
- ✅ Real-time statistics
- ✅ Production-ready architecture

**Version:** 1.0.0  
**Last Updated:** February 2026  
**Status:** Production Ready 🚀
