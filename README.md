# BizLedger - Invoice & Business Ledger System

**BizLedger** is a modern, AI-powered business ledger system that helps small businesses and freelancers efficiently manage invoices, clients, and payments. The system includes secure login, invoice management, and a FastAPI backend with a Streamlit/Flask frontend.

---

## 🛠️ Features

### User Authentication
- Secure login system with hashed passwords
- Role-based access (Admin / User)

### Invoice Management
- Add, edit, and delete invoices
- Track paid/unpaid status
- View invoice history

### Client Management
- Add and manage client information
- Link invoices to specific clients

### Tech Stack
- **Backend:** FastAPI, SQLAlchemy, SQLite
- **Frontend:** Streamlit (or Flask)
- **Authentication:** Passlib (bcrypt)
- **Deployment-ready:** Render / Railway / Heroku

### Additional Features
- Responsive UI
- Easy-to-read dashboard
- Secure password storage
- Future-ready for AI-powered analytics

---

## 💻 Getting Started

### 1. Clone the Repository
git clone https://github.com/huzaif-ulla-khan/BizLedger.git
cd BizLedger
2. Create Virtual Environment & Activate
python -m venv ledger
# Windows
ledger\Scripts\activate
# Mac/Linux
source ledger/bin/activate
3. Install Dependencies
pip install -r requirements.txt
4. Initialize the Database
python init_db.py
This will create db.sqlite3 with default tables and an admin user (admin/admin123).

5. Run the Backend
uvicorn app:app --reload
6. Run the Frontend (Streamlit)
streamlit run streamlit_app.py
🔑 Default Login Credentials
Username: admin

**Password:** `admin123`

**📂 Project Structure**

    BizLedger++/
    ├── app.py                # Main Flask app (routes + logic)
    ├── db.py                 # Database setup (SQLAlchemy)
    ├── models.py             # DB Models (User, Invoice)
    ├── init_db.py            # Creates tables + default admin user
    ├── templates/            # HTML templates
    │   ├── base.html         # Layout template
    │   ├── login.html
    │   ├── dashboard.html
    │   ├── invoices.html
    │   └── analytics.html
    ├── static/               # Static files
    │   ├── style.css
    │   └── script.js
    ├── requirements.txt      # Python dependencies
    ├── Procfile              # For deployment (Heroku/Gunicorn)
    └── README.md             # Project documentation


## 🖼️ Screenshots

### 1. Dashboard
![Dashboard Screenshot](https://github.com/huzaif-ulla-khan/BizLedger-AI-powered-Invoice-Business-Ledger-System-/blob/main/screenshots/dashboard.png)
*Description: Overview of invoices and clients.*

### 2. Add Invoice
![Add Invoice Screenshot](https://github.com/huzaif-ulla-khan/BizLedger-AI-powered-Invoice-Business-Ledger-System-/blob/main/screenshots/add_invoice.png) 
*Description: Form to create a new invoice.*



🚀 Deployment
BizLedger can be easily deployed on Render or Railway:

Push your repository to GitHub.

Connect the GitHub repo to Render or Railway.

Set environment variables if needed.

Deploy the backend and frontend.

Live URL: [https://bizledger-invoice-and-business-ledger.onrender.com](https://bizledger-invoice-and-business-ledger.onrender.com)

⚡ Future Improvements
AI-powered invoice predictions & analytics

PDF export for invoices

## 📞 Contact
**Huzaif Ulla Khan**  
- Email: [khuzaif319@gmail.com](mailto:khuzaif319@gmail.com)  
- GitHub: [https://github.com/huzaif-ulla-khan](https://github.com/huzaif-ulla-khan)  
- LinkedIn: [https://www.linkedin.com/in/your-linkedin](https://www.linkedin.com/in/your-linkedin)


Multi-user role management

Email notifications for invoices
