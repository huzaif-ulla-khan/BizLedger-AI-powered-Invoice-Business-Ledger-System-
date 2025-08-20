# app.py
from flask import Flask, render_template, request, redirect, url_for, session, flash, send_file
from passlib.context import CryptContext
from db import SessionLocal, engine
from models import Base, User, Transaction
from sqlalchemy import func, and_
import pandas as pd
import io
import datetime
import math

app = Flask(__name__, static_folder="static", template_folder="templates")
app.secret_key = "change_this_secret_for_prod"
pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")

Base.metadata.create_all(bind=engine)

# ---------- Helpers ----------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def hash_password(pw: str) -> str:
    return pwd.hash(pw)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd.verify(plain, hashed)

def login_required(f):
    from functools import wraps
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login", next=request.path))
        return f(*args, **kwargs)
    return wrapper

# ---------- Auth routes ----------
@app.route("/", methods=["GET", "POST"])
def login():
    if "user_id" in session:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        db = SessionLocal()
        user = db.query(User).filter(func.lower(User.username) == username.lower()).first()
        db.close()
        if user and verify_password(password, user.hashed_password):
            session["user_id"] = user.id
            session["username"] = user.username
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid username or password", "danger")
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        if not username or not password:
            flash("Provide username and password", "danger")
            return redirect(url_for("register"))
        db = SessionLocal()
        exists = db.query(User).filter(func.lower(User.username) == username.lower()).first()
        if exists:
            flash("Username already taken", "danger")
            db.close()
            return redirect(url_for("register"))
        user = User(username=username, hashed_password=hash_password(password))
        db.add(user)
        db.commit()
        db.close()
        flash("Account created — log in", "success")
        return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# ---------- Dashboard ----------
@app.route("/dashboard")
@login_required
def dashboard():
    user_id = session["user_id"]
    db = SessionLocal()

    # totals
    total_income = db.query(func.coalesce(func.sum(Transaction.amount), 0.0)).filter(Transaction.user_id==user_id, Transaction.type=="income").scalar() or 0.0
    total_expense = db.query(func.coalesce(func.sum(Transaction.amount), 0.0)).filter(Transaction.user_id==user_id, Transaction.type=="expense").scalar() or 0.0
    balance = total_income - total_expense

    # category breakdown for pie chart
    cat_rows = db.query(Transaction.category, func.sum(Transaction.amount).label("total"), Transaction.type).filter(Transaction.user_id==user_id).group_by(Transaction.category, Transaction.type).all()
    # prepare data aggregated by category (expense and income both included separately)
    cat_data = {}
    for cat, total, ttype in cat_rows:
        key = f"{cat} ({ttype})" if cat else f"Uncategorized ({ttype})"
        cat_data[key] = float(total)

    # time series: monthly net (income - expense)
    # For last 6 months
    today = datetime.date.today()
    months = []
    series = {}
    for i in range(5, -1, -1):
        month = (today.replace(day=1) - datetime.timedelta(days=1)).replace(day=1) - datetime.timedelta(days=30*i)
        # Normalize month label
        mlabel = month.strftime("%Y-%m")
        months.append(mlabel)
        # compute net for that month
        start = datetime.date(month.year, month.month, 1)
        if month.month == 12:
            end = datetime.date(month.year+1, 1, 1)
        else:
            end = datetime.date(month.year, month.month+1, 1)
        income_m = db.query(func.coalesce(func.sum(Transaction.amount), 0.0)).filter(Transaction.user_id==user_id, Transaction.type=="income", Transaction.date >= start, Transaction.date < end).scalar() or 0.0
        expense_m = db.query(func.coalesce(func.sum(Transaction.amount), 0.0)).filter(Transaction.user_id==user_id, Transaction.type=="expense", Transaction.date >= start, Transaction.date < end).scalar() or 0.0
        series[mlabel] = float(income_m - expense_m)

    db.close()
    return render_template("dashboard.html",
                           total_income=round(float(total_income),2),
                           total_expense=round(float(total_expense),2),
                           balance=round(float(balance),2),
                           cat_data=cat_data,
                           months=months,
                           series=series,
                           username=session.get("username"))

# ---------- Ledger (list/add/edit/delete/export) ----------
@app.route("/ledger", methods=["GET", "POST"])
@login_required
def ledger():
    user_id = session["user_id"]
    db = SessionLocal()

    # POST = add
    if request.method == "POST":
        desc = request.form.get("description", "").strip()
        amount = request.form.get("amount", "0").strip()
        ttype = request.form.get("type", "expense")
        category = request.form.get("category", "").strip()
        date_str = request.form.get("date", "")
        try:
            amt = float(amount)
        except:
            flash("Invalid amount", "danger")
            db.close()
            return redirect(url_for("ledger"))
        if date_str:
            try:
                d = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
            except:
                d = datetime.date.today()
        else:
            d = datetime.date.today()

        txn = Transaction(user_id=user_id, description=desc, amount=amt, type=ttype, category=category or None, date=d)
        db.add(txn)
        db.commit()
        flash("Transaction added", "success")
        db.close()
        return redirect(url_for("ledger"))

    # GET = list with filters
    q = db.query(Transaction).filter(Transaction.user_id == user_id)
    # filters
    f_type = request.args.get("type")
    f_cat = request.args.get("category")
    start = request.args.get("start")
    end = request.args.get("end")
    if f_type in ("income","expense"):
        q = q.filter(Transaction.type == f_type)
    if f_cat:
        q = q.filter(Transaction.category == f_cat)
    if start:
        try:
            s = datetime.datetime.strptime(start, "%Y-%m-%d").date()
            q = q.filter(Transaction.date >= s)
        except:
            pass
    if end:
        try:
            e = datetime.datetime.strptime(end, "%Y-%m-%d").date()
            q = q.filter(Transaction.date <= e)
        except:
            pass

    txns = q.order_by(Transaction.date.desc()).all()

    # categories for filter dropdown
    cats = db.query(Transaction.category).filter(Transaction.user_id==user_id).distinct().all()
    categories = [c[0] for c in cats if c[0]]

    db.close()
    return render_template("ledger.html", transactions=txns, categories=categories, filters={"type":f_type or "", "category":f_cat or "", "start":start or "", "end":end or ""})

@app.route("/ledger/delete/<int:tid>", methods=["POST"])
@login_required
def ledger_delete(tid):
    user_id = session["user_id"]
    db = SessionLocal()
    txn = db.query(Transaction).filter(Transaction.id==tid, Transaction.user_id==user_id).first()
    if txn:
        db.delete(txn)
        db.commit()
        flash("Transaction deleted", "success")
    else:
        flash("Not found or permission denied", "danger")
    db.close()
    return redirect(url_for("ledger"))

@app.route("/ledger/export")
@login_required
def ledger_export():
    user_id = session["user_id"]
    fmt = request.args.get("fmt","csv")
    db = SessionLocal()
    txns = db.query(Transaction).filter(Transaction.user_id==user_id).order_by(Transaction.date.desc()).all()
    db.close()
    rows = []
    for t in txns:
        rows.append({"id": t.id, "date": t.date.isoformat(), "description": t.description, "amount": t.amount, "type": t.type, "category": t.category or ""})
    df = pd.DataFrame(rows)
    if fmt == "xlsx":
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            df.to_excel(writer, index=False, sheet_name="ledger")
            writer.save()
        output.seek(0)
        return send_file(output, download_name="ledger.xlsx", as_attachment=True, mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    else:
        csv_bytes = df.to_csv(index=False).encode("utf-8")
        return send_file(io.BytesIO(csv_bytes), download_name="ledger.csv", as_attachment=True, mimetype="text/csv")

# ---------- API endpoints for charts (optional) ----------
@app.route("/api/category-data")
@login_required
def api_category_data():
    user_id = session["user_id"]
    db = SessionLocal()
    rows = db.query(Transaction.category, Transaction.type, func.sum(Transaction.amount).label("total")).filter(Transaction.user_id==user_id).group_by(Transaction.category, Transaction.type).all()
    db.close()
    data = {}
    for cat, ttype, total in rows:
        key = f"{cat or 'Uncategorized'} ({ttype})"
        data[key] = float(total)
    return data

@app.route("/api/series-data")
@login_required
def api_series_data():
    user_id = session["user_id"]
    db = SessionLocal()
    today = datetime.date.today()
    labels = []
    values = []
    for i in range(5, -1, -1):
        month = (today.replace(day=1) - datetime.timedelta(days=30*i))
        lbl = month.strftime("%Y-%m")
        labels.append(lbl)
        # compute net
        start = datetime.date(month.year, month.month, 1)
        if month.month == 12:
            end = datetime.date(month.year+1, 1, 1)
        else:
            end = datetime.date(month.year, month.month+1, 1)
        income_m = db.query(func.coalesce(func.sum(Transaction.amount), 0.0)).filter(Transaction.user_id==user_id, Transaction.type=="income", Transaction.date >= start, Transaction.date < end).scalar() or 0.0
        expense_m = db.query(func.coalesce(func.sum(Transaction.amount), 0.0)).filter(Transaction.user_id==user_id, Transaction.type=="expense", Transaction.date >= start, Transaction.date < end).scalar() or 0.0
        values.append(float(income_m - expense_m))
    db.close()
    return {"labels": labels, "values": values}

# ---------- Run ----------
if __name__ == "__main__":
    app.run(debug=True)
