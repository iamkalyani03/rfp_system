# FastAPI Project README

##  Project Overview
This project is a Python application built using **FastAPI**. It uses **SQLModel** for PostgreSQL database interactions and integrates several useful libraries for environment management, AI (OpenAI API), file handling, and HTTP operations. The application runs locally using **Uvicorn**.

---

##  Technology Stack

| Category | Technology/Library | Purpose |
| :--- | :--- | :--- |
| **Backend Framework** | `fastapi` | High‑performance web API framework |
| **Server** | `uvicorn[standard]` | ASGI server for FastAPI |
| **Database ORM** | `sqlmodel` | Database layer built on SQLAlchemy + Pydantic |
| **Database Driver** | `psycopg2-binary` | PostgreSQL adapter |
| **Environment Management** | `python-dotenv` | Loads environment variables from `.env` |
| **AI Integration** | `openai` | OpenAI API client |
| **HTTP Client** | `requests` | For making external API calls |
| **Data Validation** | `pydantic` | Data validation and modeling |
| **File Handling** | `aiofiles`, `python-multipart` | Async file operations + form data support |

---

##  Setup and Installation

### **Prerequisites**
- Python **3.7+**
- Running **PostgreSQL** instance

---

### **1. Clone the Repository**
```bash
git clone https://github.com/iamkalyani03/rfp_system.git
cd rfp-system
```

---

### **2. Create Virtual Environment (Recommended)**
```bash
python -m venv venv
```
Activate:
- macOS/Linux:
```bash
source venv/bin/activate
```
- Windows:
```bash
venv\Scripts\activate
```

---

### **3. Install Dependencies**
```bash
pip install -r requirements.txt
```

---

### **4. Configure Environment Variables**
Create a `.env` file in your project root:

#### **Example `.env` structure:**
```env
# Database URL
DATABASE_URL=postgresql://postgres:mypassword123@localhost:5432/rfpdb

# REQUIRED — your OpenAI API key
OPENAI_API_KEY=your_secret_key
# SMTP (Sending Email)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=khushbooshimpi13@gmail.com
SMTP_PASS=<your_gmail_app_password>  # Use Gmail App Password

# IMAP (Receiving Email)
IMAP_HOST=imap.gmail.com
IMAP_USER=khushbooshimpi13@gmail.com
IMAP_PASS=<your_gmail_app_password>  # Same Gmail App Password

# Polling interval (seconds)
IMAP_POLL_SECONDS=60
```
 **Note:** If your Gmail has 2FA enabled, you must generate a **Gmail App Password**.

---

##  Running the Application

### **1. Start the Backend Server**
```bash
uvicorn main:app --reload
```
*(Assumes your FastAPI app instance is named `app` in `main.py`)*

---

### **2. Run the Frontend (Optional)**
```bash
npm install
npm run dev
```

---

### **3. Access the Application**
- API Base URL: **http://127.0.0.1:8000**
- Swagger UI Docs: **http://127.0.0.1:8000/docs**

You can now test and interact with all API endpoints.

---

##  You're All Set!
Your FastAPI + SQLModel + PostgreSQL + OpenAI powered application is ready to run.

