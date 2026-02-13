# 🎯 Resume Parsing & Data Extraction System
**It's live on Render**

https://resume-parser-system-ivfd.onrender.com/

A web-based intelligent resume parsing application that automates manual data entry by extracting structured information from resumes and storing it into Excel.

Designed for university/placement-cell level automation to reduce manual workload of teachers and administrators.

---

# 📌 Project Overview

This system allows users to upload resumes (PDF/DOCX/Image) and automatically extracts structured information such as:

* Name
* Email
* Phone Number
* Skills
* Education
* Certifications
* Experience
* Publications
* Awards

The extracted data is stored in Excel and displayed in a clean web interface.

The goal is to eliminate manual resume reading and Excel entry work.

---

# 🧠 Key Features

## 📂 Resume Upload

* Supports **PDF, DOCX, PNG, JPG**
* File type validation (frontend + backend)
* Secure upload handling

## 🔍 Intelligent Data Extraction

Rule-based extraction system for:

* Name detection
* Email extraction
* Phone number extraction
* Skills extraction
* Education extraction (score-validated)
* Certification extraction (section aware)

## 📊 Excel-Based Storage

* No database required
* All parsed data stored in Excel
* Easy portability
* Download anytime

## 🖥️ Interactive UI

* Clean table display
* Modal popup for details
* View education/certifications
* Delete row
* Undo delete
* Reset all data
* Download Excel

## 🧩 Additional Sections Extracted

* Experience
* Publications
* Awards/Achievements

---

# 🏗️ Project Architecture

The system follows modular architecture with clear separation of logic.

```
Resume Parser/
│
├── app/
│   ├── main.py                # Flask app entry
│   ├── parser/
│   │   ├── extractor.py       # Data extraction logic
│   │   ├── pdf_parser.py      # PDF text extraction
│   │   ├── docx_parser.py     # DOCX text extraction
│   │   ├── image_parser.py    # Image OCR extraction
│   │   └── keywords.py        # Keyword datasets
│   │
│   ├── services/
│   │   └── excel_service.py   # Excel operations
│
├── templates/
│   └── index.html             # Frontend UI
│
├── static/
│   ├── style.css
│   ├── script.js
│   └── favicon.png
│
├── uploads/                   # Uploaded resumes
├── output/
│   └── resume_data.xlsx       # Excel storage
│
├── requirements.txt
├── Procfile                   # Render deployment
└── README.md
```

---

# ⚙️ How It Works

1. User uploads resume
2. System extracts text from file
3. Extractor processes structured data
4. Data stored in Excel
5. Displayed in UI table
6. User can view/delete/download/reset

---

# 🚀 Installation & Setup (Local)

## 1️⃣ Clone Repository

```
git clone https://github.com/YOUR_USERNAME/resume-parser.git
cd resume-parser
```

## 2️⃣ Create Virtual Environment

```
python -m venv venv
venv\Scripts\activate   (Windows)
```

## 3️⃣ Install Requirements

```
pip install -r requirements.txt
```

## 4️⃣ Run Application

```
python -m app.main
```

Open browser:

```
http://127.0.0.1:5000
```

---

# 🌐 Live Deployment (Render)

This project is deployed using **Render free hosting**.

### Deployment Steps

1. Push code to GitHub
2. Create new Web Service on Render
3. Add build & start commands:

**Build**

```
pip install -r requirements.txt
```

**Start**

```
gunicorn app.main:app
```

4. Deploy and get live URL

---

# 📦 Requirements

```
flask
gunicorn
pandas
pdfplumber
python-docx
openpyxl
pillow
```

---

# 🧠 Extraction Logic Used

## ✔ Rule-Based Extraction

* Regex for email & phone
* Keyword mapping for skills
* Score-validated education detection
* Section-aware certification detection

## ✔ Accuracy Improvements

* Block-based certification extraction
* Education validation with score matching
* Section detection logic
* Clean normalization

---

# 📊 Why Excel Instead of Database?

* Lightweight deployment
* Easy portability
* No setup required
* Suitable for university-level usage
* Can upgrade to DB in future

---

# 🔒 Privacy & Security

* No external API required
* Local parsing
* No data sharing
* Suitable for confidential resumes

---

# 📈 Future Enhancements (Tier-2 → Tier-3)

* NLP-based section detection (spaCy)
* AI-assisted experience extraction
* Database integration (MySQL/PostgreSQL)
* Admin dashboard
* Multi-user support
* Bulk resume upload
* Analytics dashboard

---

# 🎯 Use Cases

* University placement cells
* HR resume screening
* Internship filtering
* Recruitment automation
* Academic project submission analysis

---

# 🏁 Project Status

✔ Fully working
✔ End-to-end functional
✔ Hosted live
✔ Demo ready
✔ Scalable architecture
✔ Production-ready for small scale

---

# 👨‍💻 Author

**Jignesh Thacker**
AI/ML & Python Developer

This project was built to automate manual resume data entry and demonstrate scalable resume parsing architecture using Python & Flask.

# Output ScreenShot
<img width="1432" height="500" alt="image" src="https://github.com/user-attachments/assets/cd8b4891-5a44-4b84-afb8-d4f21fa3c0f4" />
<img width="1437" height="735" alt="image" src="https://github.com/user-attachments/assets/5dd95b50-254e-4007-9197-d9f07f48c7c6" />





---

# ⭐ If you like this project

Give it a star on GitHub and share feedback!
