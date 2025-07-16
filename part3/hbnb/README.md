<p align="center">
  <a href="https://hbnb.fly.dev/">
    <img src="https://s3.amazonaws.com/intranet-projects-files/holbertonschool-higher-level_programming+/263/HBTN-hbnb-Final.png" alt="Holberton School HBnB logo">
  </a>
</p>
<center>
<h1>HBnB Project — Part 3:</h1>
<em>Enhanced Backend with Authentication and Database Integration</em>

</center>

## 📖 Project Overview

This repository contains Part 3 of the HBnB Project. In this phase, we significantly enhance the backend by introducing JWT authentication, role-based access control, and persistent database integration using SQLAlchemy with SQLite (for development) and preparation for MySQL (for production).

We’re transitioning from a prototype to a real-world backend architecture that is secure, scalable, and production-ready.

## 🚀 Objectives

By the end of this phase, we aim to:

+ Secure the API with JWT-based authentication (Flask-JWT-Extended),
+ Implement role-based access control, using is_admin flag on users,
+ Replace in-memory storage with SQLite + SQLAlchemy ORM,
+ Define and map database relationships between all entities,
+ Visualize the database schema,
+ Enforce data consistency and validation in models and routes.

## 🗂 Project Structure

```bash
hbnb/  
├── app/  
│   ├── __init__.py  
│   ├── api/  
│   │   ├── __init__.py  
│   │   └── v1/  
│   │       ├── __init__.py  
│   │       ├── amenities.py  
│   │       ├── bookings.py  
│   │       ├── places.py  
│   │       ├── reviews.py  
│   │       └── users.py  
│   ├── models/  
│   │   ├── __init__.py  
│   │   ├── amenity.py  
│   │   ├── booking.py  
│   │   ├── place.py  
│   │   ├── review.py  
│   │   └── user.py  
│   ├── persistence/  
│   │   ├── __init__.py  
│   │   └── repository.py  
│   └── services/  
│       ├── __init__.py  
│       └── facade.py  
├── blacklist.py  
├── config.py  
├── extensions.py  
├── instance/  
│   └── development.db  
├── README.md  
├── requirements.txt  
├── run.py  
├── SQL/  
│   ├── SQL_test.sql  
│   └── SQL.sql  
├── tests/  
│   ├── init_admin.sql  
│   ├── run_tests.py  
│   ├── test_amenities_req.py  
│   ├── test_places_req.py  
│   └── test_users_req.py  
├── utils.py  
├── HBnB - Entity Relationship Diagram.jpg  
└── HBnB - Entity Relationship Diagram.pdf  
```

## 🔧 Technologies Used

+ Python 3.x
+ Flask
+ Flask-RESTx
+ Flask-JWT-Extended
+ SQLAlchemy
+ SQLite
+ argon2 (for secure password hashing)
+ draw.io (for ER diagrams)
+ Pydantic

## 🧩 Key Features

+ JWT Authentication: Secure login/logout and token-based access to protected endpoints,
+ Role-Based Access Control: Admin vs. regular user permissions (e.g., only admins can create an amenity),
+ Persistent Storage: Switched from in-memory to SQLite + SQLAlchemy ORM for full persistence,
+ Entity Relationship Diagram: Design and visualize relational database schemas with draw.io,
+ Validation & Error Handling: Model-level and route-level data checks and exception handling.

## 📚 Learning Outcomes

+ Implement secure login/auth flows using JWT tokens,
+ Enforce fine-grained permissions based on user roles,
+ Manage persistent data with SQLAlchemy ORM,
+ Design and visualize relational database schemas with draw.io,
+ Prepare backend architecture for deployment in real environments.

## 🛠 How to Run

1️⃣ Clone the repository:

```bash
git clone https://github.com/loufi84/holbertonschool-hbnb.git
cd holbertonschool-hbnb/part3/hbnb
```

2️⃣ Install dependencies:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3️⃣ Run the application:

```bash
python3 -m run
```
(You must be in the hbnb folder)

4️⃣ Access Swagger UI:

[http://localhost:5001/](http://localhost:5001/)  
(We moved the port to 5001 as it was tested with a Mac and port 5000 is AirPlay on MacOS)

## 🧪 Testing

Run automatic tests:

In ```config.py``` change this line :
```python
SQLALCHEMY_DATABASE_URI = 'sqlite:///development.db'
```
To :
```python
SQLALCHEMY_DATABASE_URI = 'sqlite:///testDB.db'
```
Start the server.  
While it's running:
+ Open a new terminal
 ```bash
cd /tests
python3 -m run_tests
```

Automatic tests are for place, user and amenity.

You can also test individual endpoints using Swagger UI, Postman, or cURL.
(Tested functional with SwaggerUI on web browser)

It is also possible to test the project by going (starting from /hbnb) :
```bash
cd SQL
sqlite3 ./instance/testDB.db < SQL_test.sql
```
For it to work, you need to have already created the database testDB.db by changing the URI (see the first part of Testing)
Then, you can
```bash
cd ..
cd instance
sqlite3 testDB.db
```
And type some SQL to check the insertions :
```SQL
SELECT * FROM user;
SELECT * FROM place;
```
Or even try some CRUD operations!

## 🧬 ER Diagram (made with draw.io)

![Entity Relationship Diagram for HBnB project](HBnB%20-%20Entity%20Relationship%20Diagram.jpg)

## 🚧 Roadmap

✅ Part 1: Project Design  
✅ Part 2: Business Logic and API Endpoints  
🟢 Part 3: Authentication and Database Integration (You are here)  
🔒 Part 4: Web Client (HTML5/CSS3 + JS UI)  

## 🤝 Contributions

Contributions are welcome! Open an issue or submit a PR to suggest features or improvements.

## 📄 License

MIT License — see LICENSE file for details.

## 🤝 Authors

+ Quentin Lataste : [github.com/loufi84](https://github.com/loufi84)
+ Valentin Dumont : [github.com/Proser-V](https://github.com/Proser-V)
