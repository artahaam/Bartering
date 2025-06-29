# Student Bartering Platform API

This repository contains the backend REST API for a platform that allows students to exchange goods and services without using money. Built with Django and Django REST Framework.

## Key Features

* **Secure User Authentication:** Token-based registration, login, logout, and profile management using phone numbers as the primary identifier.
* **Offer Management:** Full CRUD (Create, Read, Update, Delete) functionality for offers with owner-only permissions for writing and public access for reading.
* **Proposal Workflow:** Users can make proposals on offers, and offer owners can accept or decline them, closing the offer upon acceptance.
* **Threaded Commenting System:** Users can post and reply to comments on offers to ask questions and communicate.
* **User Rating System:** After a trade is complete, users involved can rate each other to build community trust.
* **Image Uploads:** Support for uploading images for items being traded using `multipart/form-data`.
* **Powerful API Features:** Includes searching, ordering, and pagination for list views.
* **Automatic API Documentation:** Interactive API documentation is available via Swagger UI and ReDoc.

## Tech Stack

* Python
* Django & Django REST Framework
* PostgreSQL (Database)
* `drf-spectacular` (API Documentation)
* `Pillow` (Image Processing)
* `django-cors-headers` (Cross-Origin Resource Sharing)

## API Documentation

Once the server is running, the interactive API documentation can be accessed at the following endpoints:

* **Swagger UI:** [`http://127.0.0.1:8000/api/docs/`](http://127.0.0.1:8000/api/docs/)
* **ReDoc:** [`http://127.0.0.1:8000/api/redoc/`](http://127.0.0.1:8000/api/redoc/)

## Getting Started

Follow these instructions to set up and run the project locally.

### 1. Prerequisites

* Python 3.8+
* PostgreSQL
* Git

### 2. Installation and Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/artahaam/Bartering
    cd Bartering
    ```

2.  **Create and activate a virtual environment:**
    * On macOS/Linux:
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```
    * On Windows:
        ```bash
        python -m venv venv
        .\venv\Scripts\activate
        ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up Environment Variables:**
    Create a `.env` file in the root directory of the project by copying the example file:
    ```bash
    cp .env.example .env
    ```
    Now, open the `.env` file and fill in your actual database credentials and a new `SECRET_KEY`.

5.  **Set up the Database:**
    * Make sure your PostgreSQL server is running.
    * Create a new database and user with the same credentials you specified in your `.env` file.

6.  **Run Database Migrations:**
    ```bash
    python manage.py migrate
    ```

7.  **Create a Superuser (Optional):**
    This allows you to access the Django Admin panel at `/admin/`.
    ```bash
    python manage.py createsuperuser
    ```

### 3. Running the Development Server

To start the API server, run the following command:
```bash
python manage.py runserver