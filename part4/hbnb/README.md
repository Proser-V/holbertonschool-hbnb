<p align="center">
  <a href="https://hbnb.fly.dev/">
    <img src="https://s3.amazonaws.com/intranet-projects-files/holbertonschool-higher-level_programming+/263/HBTN-hbnb-Final.png" alt="Holberton School HBnB logo">
  </a>
</p>
<center>
<h1>HBnB Project — Part 4:</h1>
<em>Simple Web Client</em>

</center>

## 📖 Project Overview

This repository contains the final part of the HBnB Project. In this phase, we significantly focused on the front-end development of our application using HTML5, CSS3 and JavaScript ES6. We designed and implemented an interactive user interface that connects with the back-end services we developed in the previous parts.

## 🚀 Objectives

By the end of this phase, we aim to:

+ Develop a user-friendly interface by our own design choices,
+ Implement CSR and SSR functionality to interact with the back-end API,
+ Ensure secure and efficient data handling using JavaScript and Jinja,
+ Apply modern web development practices to create a dynamic web application.

## 🗂 Full Project Structure (Part 3 & 4)

```bash
hbnb/  
├── HBnB - Entity Relationship Diagram.jpg
├── HBnB - Entity Relationship Diagram.pdf
├── README.md
├── SQL
│   ├── SQL.sql
│   └── SQL_test.sql
├── app
│   ├── __init__.py
│   ├── api
│   │   ├── __init__.py
│   │   └── v1
│   │       ├── __init__.py
│   │       ├── amenities.py
│   │       ├── bookings.py
│   │       ├── places.py
│   │       ├── reviews.py
│   │       └── users.py
│   ├── models
│   │   ├── __init__.py
│   │   ├── amenity.py
│   │   ├── booking.py
│   │   ├── place.py
│   │   ├── review.py
│   │   └── user.py
│   ├── persistence
│   │   ├── __init__.py
│   │   └── repository.py
│   ├── services
│   │   ├── __init__.py
│   │   └── facade.py
│   └── web
│       ├── __init__.py
│       ├── api_helpers.py
│       └── html_routes.py
├── blacklist.py
├── config.py
├── extensions.py
├── instance
│   └── development.db
├── requirements.txt
├── run.py
├── static
│   ├── css
│   │   └── style.css
│   ├── icons
│   │   ├── ai.png
│   │   ├── balai.png
│   │   ├── cabin.png
│   │   ├── cal.12 icon.jpg
│   │   ├── coffee-cup.png
│   │   ├── default-amenities.png
│   │   ├── logo-wifi.png
│   │   ├── machete.jpeg
│   │   ├── pets-allowed.png
│   │   ├── pizza.png
│   │   ├── rock.png
│   │   ├── swimming-pool.png
│   │   └── trees-icon.jpg
│   ├── images
│   │   ├── add_photo.png
│   │   ├── add_photo_grey.png
│   │   ├── default-place-grey.png
│   │   ├── default-user.png
│   │   ├── logo.png
│   │   ├── loupe.png
│   │   └── under_construction.png
│   └── js
│       ├── add_place.js
│       ├── add_review.js
│       ├── admin_panel.js
│       ├── calendar.js
│       ├── cancel-booking.js
│       ├── delete-place.js
│       ├── filter.js
│       ├── login.js
│       ├── new_place_adress.js
│       ├── refresh_token.js
│       ├── registration.js
│       ├── scroll-top.js
│       ├── show_photos.js
│       ├── update_place.js
│       ├── user_popup.js
│       └── user_update.js
├── templates
│   ├── add_place.html
│   ├── admin_panel.html
│   ├── booking.html
│   ├── general_header.html
│   ├── index.html
│   ├── login.html
│   ├── place-all-bookings.html
│   ├── place-all-photos.html
│   ├── place-all-reviews.html
│   ├── place.html
│   ├── registration.html
│   ├── under_construction.html
│   ├── update_place.html
│   └── user_profile.html
├── tests
│   ├── init_admin.sql
│   ├── run_tests.py
│   ├── test_amenities_req.py
│   ├── test_places_req.py
│   └── test_users_req.py
└── utils.py  
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
+ HTML5
+ Vanilla CSS3
+ Javascript ES6

## 🧩 Key Features

+ Make the design,
+ Implement the main page and the list of places,
+ Implement a filter on the main page to dynamically filter the places,
+ Implement login and user creation,
+ Implement the possisibility to make a reservation and to review a visited place,
+ Implement the user profile page and informations,
+ Implement the admin panel to moderate all the users, places, bookings, reviews and amenities.

## 🧩 Possible improvements

+ Add a payment system,
+ Add the possibility to autmatically send email to users,
+ Add a instant messaging system to communicate between users,
+ ...

## 📚 Learning Goals

+ Understand and apply HTML5, CSS3, and JavaScript ES6 in a real-world project,
+ Learn to interact with back-end services using AJAX/Fetch API,
+ Implement authentication mechanisms and manage user sessions,
+ Use client-side scripting to enhance user experience without page reloads.

## 🛠 How to Run

1️⃣ Clone the repository:

```bash
git clone https://github.com/Proser-V/holbertonschool-hbnb.git
```

2️⃣ Install dependencies:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd holbertonschool-hbnb/part4/hbnb
```

3️⃣ Run the application:

```bash
python3 -m run
```
(You must be in the hbnb folder)

4️⃣ Access Home page:

[http://localhost:5001/](http://localhost:5001/)  
(We moved the port to 5001 as it was tested with a Mac and port 5000 is AirPlay on MacOS)

## 🚧 Roadmap

✅ Part 1: Project Design  
✅ Part 2: Business Logic and API Endpoints  
✅ Part 3: Authentication and Database Integration (You are here)  
🟢 Part 4: Web Client (HTML5/CSS3 + JS UI)  

## 🤝 Contributions

Contributions are welcome! Open an issue or submit a PR to suggest features or improvements.

## 📄 License

MIT License — see LICENSE file for details.

## 🤝 Authors

+ Quentin Lataste : [github.com/loufi84](https://github.com/loufi84) - Back-end
+ Valentin Dumont : [github.com/Proser-V](https://github.com/Proser-V) - Back-end & Front-end
