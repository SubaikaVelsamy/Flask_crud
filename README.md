Flask CRUD App with MySQL and ReactJS Frontend

This is a full-stack CRUD (Create, Read, Update, Delete) web application built using Flask (backend), MySQL (database), and ReactJS (frontend).
It allows you to manage student data (add, edit, delete, view) through a modern React interface while the backend handles all data operations via Flask API routes.

Features

List all students in a dynamic React table

Add a new student via React form

Edit existing student information with pre-filled forms

Delete a student with confirmation

Backend powered by Flask API routes

MySQL database for persistent storage

Frontend built with ReactJS (SPA style)

Communicates via JSON API between React and Flask

Project Structure
python_crud/
├── backend/             # Flask backend
│   ├── app.py
│   ├── venv/
│   ├── requirements.txt
│   └── ...other backend files
│
├── frontend/            # React frontend
│   ├── package.json
│   ├── public/
│   ├── src/
│   │   ├── App.js
│   │   ├── index.js
│   │   └── pages/
│   │       ├── Users.js
│   │       ├── AddUser.js
│   │       └── EditUser.js
│   └── ...other React files
│
└── README.md

Setup Instructions

Backend

cd backend
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
python app.py


Frontend

cd frontend
npm install
npm start


Open http://localhost:3000 in your browser.

Technology Stack

Backend: Python, Flask

Frontend: ReactJS

Database: MySQL

Communication: RESTful JSON API