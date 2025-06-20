HBnB Project — Part 2: Business Logic and API Endpoints

📖 Project Overview  

This repository contains Part 2 of the HBnB Project. In this phase, we focus on implementing the Business Logic and Presentation Layer of the application using Python, Flask, and flask-restx.  

The goal of this part is to lay a solid, scalable foundation for the core functionality of the HBnB platform: managing Users, Places, Reviews, and Amenities through well-structured RESTful APIs.  

⚠ Note: Authentication, JWT, and Role-Based Access Control will be implemented in Part 3. This stage focuses purely on the core functionality.  

⸻

🚀 Objectives  

By the end of this phase, we aim to:  
	•	Set Up the Project Structure  
	•	Organize code into modular packages following Python best practices.  
	•	Separate concerns between Presentation and Business Logic layers.  
	•	Implement Business Logic  
	•	Build core entities: User, Place, Review, Amenity.  
	•	Define relationships between entities.  
	•	Apply the Facade Pattern to simplify interactions between layers.  
	•	Develop RESTful API Endpoints.  
	•	CRUD operations for Users, Places, Reviews, and Amenities.  
	•	Use flask-restx to define and document the API.  
	•	Implement data serialization to include extended attributes in responses (e.g., when retrieving a Place, include the owner’s first_name, last_name, and related amenities).  
	•	Test and Validate  
	•	Thoroughly test each API endpoint.  
	•	Use tools like Postman or cURL for manual testing.  
	•	Ensure proper handling of edge cases.  

⸻

🗂 Project Structure  

```
hbnb/  
├── app/  
│   ├── __init__.py  
│   ├── api/  
│   │   ├── __init__.py  
│   │   ├── v1/  
│   │       ├── __init__.py  
│   │       ├── users.py  
│   │       ├── places.py  
│   │       ├── reviews.py  
│   │       ├── amenities.py  
│   │       ├── bookings.py  
│   ├── models/  
│   │   ├── __init__.py  
│   │   ├── user.py  
│   │   ├── place.py  
│   │   ├── review.py  
│   │   ├── amenity.py  
│   │   ├── booking.py  
│   ├── services/  
│   │   ├── __init__.py  
│   │   ├── facade.py  
│   ├── persistence/  
│       ├── __init__.py  
│       ├── repository.py  
├── run.py  
├── config.py  
├── requirements.txt  
├── README.md  
├── tests/  
```

🔧 Technologies  
	•	Python 3.x  
	•	Flask  
	•	flask-restx (for API creation and documentation)  
	•	Pydantic (for validation + serialization/deserialization)  
	•	Marshmallow (for serialization, if applicable)  
	•	pytest (for testing)  

⸻

📚 Learning Outcomes  
	•	Master modular architecture in Python & Flask.  
	•	Build well-documented REST APIs using flask-restx.  
	•	Translate design documentation into functional business logic.  
	•	Handle nested data serialization efficiently.  
	•	Develop, test, and debug complex API endpoints.  

⸻

🛠 How to Run  

1️⃣ Clone the repository:  

git clone https://github.com/yourusername/hbnb-business-logic-api.git  
cd hbnb-business-logic-api  

2️⃣ Install dependencies:  

python3 -m venv venv  
source venv/bin/activate  
pip install -r requirements.txt  

3️⃣ Run the application:  

python3 -m run  
(You must be in the hbnb folder)  

4️⃣ Access the API documentation via flask-restx:  

http://localhost:5001/  
(We moved the port to 5001 as it was tested with a Mac and port 5000 is AirPlay on MacOS)  

🧪 Testing  

Run the tests using:  


You can also manually test the endpoints using Postman, cURL, or any REST client.  
(Tested functional with SwaggerUI on web browser)  

You can also type ‘‘‘pytest‘‘‘ in the terminal in hbnb folder.

⸻

🚧 Roadmap  

✅ Part 1: Project Design  
🟠 Part 2: Business Logic and API Endpoints (You are here)  
🔒 Part 3: Authentication and Access Control (JWT, Roles)  
🔒 Part 4: Simple Web client  

⸻

🤝 Contributions  

Pull requests are welcome! Please open an issue first to discuss your proposal.  

⸻

📄 License  

This project is licensed under the MIT License.  