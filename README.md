# 🌆 Smart City Issue Tracker

A full-stack civic issue management system built to help citizens report city-related problems and enable municipal authorities to track, analyze and resolve them efficiently.

This system simulates a real government-level complaint management portal with automated email notifications, dashboards and admin controls.

---

## 🧠 Problem Statement

City residents face difficulty reporting civic issues like road damage, garbage dumping, water leakage, streetlight failure etc.  
There is no centralized digital platform to track issue status and provide real-time updates to citizens.

This project solves that by providing a digital complaint management system.

---

## ⚙️ Features

### Citizen Module
• Register and report city issues  
• Upload real images of problems  
• Receive automated email confirmation  
• Track issue status  
• Search and filter reported issues  

### Admin Module
• Secure admin login  
• View all complaints  
• Update issue status (Pending → In Progress → Resolved)  
• Delete invalid issues  
• Automatic email notifications on updates  
• Live analytics dashboard  

### Dashboard & Analytics
• Total complaints count  
• Pending / In Progress / Resolved statistics  
• Category-wise issue distribution (Pie chart)  
• Status-wise bar charts  
• Issues over time (Line chart)

---

## 🛠️ Tech Stack

| Technology | Purpose |
|-----------|--------|
| Python | Backend Logic |
| Streamlit | Web UI |
| SQLite | Database |
| Plotly | Data Visualization |
| SMTP | Automated Email System |
| HTML/CSS | UI Styling |

---

## 📂 Project Structure

SmartCityTracker/
│
├── app.py              # Main Streamlit application
├── database.py         # Database creation & connection
├── issues.db           # SQLite database
├── uploads/            # Uploaded issue images
├── smartcityimages/    # UI / static images
└── README.md           # Project documentation


---

## ▶️ How To Run

pip install streamlit pandas plotly
streamlit run app.py

---

## 📌 Future Enhancements

• OTP verification for citizens  
• SMS notification system  
• AI-based issue prioritization  
• Mobile application version  
• Cloud database deployment  

---

## 👨‍💻 Author

**Ebin Raj**  
Data Science | Python | Streamlit | SQL  

---

