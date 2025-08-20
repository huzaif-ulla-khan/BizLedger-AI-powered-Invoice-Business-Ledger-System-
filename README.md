# BizLedger - Invoice & Business Ledger System

**BizLedger** is a modern, AI-powered business ledger system that allows small businesses and freelancers to manage invoices, clients, and payments efficiently. The system includes a secure login, invoice management, and integration with a FastAPI backend and Streamlit/Flask frontend.

---

## 🛠️ Features

- **User Authentication**
  - Secure login system with hashed passwords
  - Role-based access (Admin / User)

- **Invoice Management**
  - Add, edit, and delete invoices
  - Track paid/unpaid status
  - View invoice history

- **Client Management**
  - Add and manage client information
  - Link invoices to specific clients

- **Tech Stack**
  - **Backend:** FastAPI, SQLAlchemy, SQLite
  - **Frontend:** Streamlit (or Flask)
  - **Authentication:** Passlib (bcrypt)
  - **Deployment-ready:** Can be deployed on Render / Railway / Heroku

- **Additional Features**
  - Responsive UI
  - Easy-to-read dashboard
  - Secure password storage
  - Future-ready for AI-powered analytics

---

## 💻 Getting Started

### 1. Clone the repository
git clone https://github.com/yourusername/BizLedger.git
cd BizLedger
2. Create virtual environment & activate
python -m venv ledger
source ledger/Scripts/activate  # Windows
# OR
source ledger/bin/activate      # Mac/Linux
3. Install dependencies
pip install -r requirements.txt
4. Initialize the database
python init_db.py
Creates db.sqlite3 with default tables and an admin user (admin/admin123).
5. Run the backend
uvicorn app:app --reload
6. Run the frontend (Streamlit)
streamlit run streamlit_app.py
🔑 Default Login
Username: admin
Password: admin123

📂 Project Structure
BizLedger/
├── app.py               # FastAPI backend
├── db.py                # Database connection
├── init_db.py           # Script to initialize DB
├── streamlit_app.py     # Frontend (Streamlit)
├── requirements.txt     # Python dependencies
├── style.css            # Optional styling
└── README.md            # Project documentation
🚀 Deployment
Can be deployed easily on Render or Railway using the free tier.

Steps:

Push your repo to GitHub.

Connect GitHub repo to Render/Railway.

Set environment variables if needed.

Deploy backend and frontend.

⚡ Future Improvements
AI-powered invoice predictions & analytics

PDF export for invoices

Multi-user role management

Email notifications for invoices

📞 Contact
Huzaif Ulla Khan

Email: [khuzaif319@gmail.com]

GitHub: https://github.com/huzaif-ulla-khan
