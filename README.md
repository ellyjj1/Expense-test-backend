## **Summary**:

The Expense Tracker app is a full-stack application built with a **React frontend** and a **Django backend**. It allows users to manage their income and expenses by adding, viewing, and storing transactions. The app uses modern technologies like **Chakra UI** for design, **Axios** for API calls, **PostgreSQL** for database management, and is deployed using **Vercel** for both the frontend and backend services.

the front-end link: https://github.com/ellyjj1/Expense_tracker

### Technologies Used **

1. **Django**:
   - Framework used for building the backend REST API.
   - Manages the database models for storing transactions and provides views to handle incoming API requests (GET, POST, DELETE).

2. **Django REST Framework (DRF)**:
   - Extends Django to provide a powerful API framework for building the RESTful API.
   - Serializes the transaction data into JSON format for communication with the frontend.

3. **PostgreSQL**:
   - The database used for production deployment (on platforms like Heroku or Vercel).
   - Stores all transaction data in a structured format.

4. **SQLite**:
   - Used as the local development database to keep things lightweight during development.

5. **CORS Headers**:
   - `django-cors-headers` is installed and configured to allow cross-origin resource sharing, which permits the frontend (hosted on Vercel) to communicate with the backend (API).

6. **Gunicorn**:
   - WSGI HTTP server used to serve the Django application in production.

### **Deployment:**

1. **Frontend Deployment (Vercel)**:
   - The React app is deployed using Vercel, ensuring smooth deployment and CDN-backed global hosting.

2. **Backend Deployment (Vercel and neon)**:
   - The Django backend is deployed on Vercel and neon, with PostgreSQL as the production database.
