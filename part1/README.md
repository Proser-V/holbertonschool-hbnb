# HBnB Evolution - Technical Documentation (Part 1)

## 📘 Project Overview

**HBnB Evolution** is a simplified AirBnB-like application that enables users to manage listings (places), reviews, amenities, and user profiles.  
This first part of the project focuses on building **technical documentation** that will serve as a clear blueprint for the future implementation phases.

## 🎯 Objective

To document the architecture, business logic, and system interactions using best software design practices and UML diagrams.  
This includes:
- Modeling key business entities (User, Place, Review, Amenity)
- Designing a layered architecture
- Visualizing API interactions and data flow

---

## 🧩 Core Features

### 👤 User Management
- Register, update profile, delete account
- Attributes: first name, last name, email, password, admin status (boolean)

### 🏠 Place Management
- Create, update, delete, list places
- Attributes: title, description, price, latitude, longitude
- Linked to a user (owner)
- Can include a list of **amenities**

### 📝 Review Management
- Create, update, delete, list reviews by place
- Attributes: rating, comment
- Linked to a user and a place

### 🛋️ Amenity Management
- Create, update, delete, list amenities
- Attributes: name, description

---

## 🏗️ Application Architecture

The application is based on a **three-layered architecture**:

- **🎨 Presentation Layer**: Services and APIs through which users interact with the system
- **🧠 Business Logic Layer**: Models and business rules (User, Place, Review, Amenity)
- **💾 Persistence Layer**: Responsible for saving and retrieving data from the database

The application utilizes the **Facade Pattern** to simplify communication between the presentation and business logic layers.

---

## 📐 UML & Diagrams

### 🗂️ High-Level Package Diagram

- Illustrates the three main layers
- Shows dependencies and interactions via the **Facade Pattern**

### 📊 Business Logic Class Diagram

Includes:
- `User`
- `Place`
- `Review`
- `Amenity`

Details:
- Attributes and methods
- Relationships (`1-to-N`, `N-to-N` between Place and Amenity)
- Timestamps: `created_at`, `updated_at`
- Unique identifiers (IDs)

### 🔁 Sequence Diagrams

Demonstrates API call flows:
1. User registration
2. Place creation
3. Review submission
4. Fetching a list of places


---

## ⚙️ Business Rules & Constraints

- All entities must have a unique ID
- Creation and update timestamps are required for all entities
- Users can be flagged as administrators (`is_admin: bool`)
- Many-to-many relationship between Places and Amenities

---

## 🧰 Resources Used

- UML References: `Class Diagrams`, `Sequence Diagrams`, `Package Diagrams`
- Tools:
    - [draw.io](https://draw.io)

---

## 📎 Deliverables

- High-level package diagram doc.pdf : The technical documentation for the package diagram.  

- Class diagram doc.pdf : The technical documentation for the package diagram.  

- Sequence diagram doc.pdf : The technical documentation for the sequence diagram.  

- HBnB complete doc.pdf : The technical documentation for the application.  

- HBnB_High-level package.pdf : The high level package in full format.  

- HBnB_Classes diagram.pdf : The class diaram in full format.  

- HBnB_Sequence diagram_Add_place.pdf : The sequence diagram to add places.  

- HBnB_Sequence diagram_Place list.pdf : The sequence diagram to list places.  

- HBnB_Sequence diagram_Review.pdf : The sequence diagram to add a review.  

- HBnB_Sequence diagram_User registration.pdf : The sequence diagram for user's registration.  

---

## 🚀 Next Step

Move on to **Part 2: Implementation**, using this technical documentation as a foundation.  
It will serve as the single source of truth to ensure consistency and clarity during development.

---

## 👤 Author

* Valentin DUMONT - https://github.com/Proser-V *
* Quentin LATASTE - https://github.com/loufi84 *
* Developer Training Program - [Holberton School Dijon] *  
* Date: June 2025 *

---
