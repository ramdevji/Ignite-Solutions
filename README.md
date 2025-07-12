# Ignite E-Library 

A modern web application to explore books from Project Gutenberg, featuring a powerful search API and a responsive user interface.

---

## ✨ Features

* **Comprehensive Search API:** Filter books by Gutenberg ID, language, MIME type, topic, author, and title.
* **Pagination & Sorting:** Efficiently browse results, sorted by download count.
* **Interactive UI:** Built with React and Tailwind CSS for a smooth, responsive user experience.
* **API Documentation:** Integrated Swagger UI for easy API exploration and testing.
* **Containerized:** Packaged with Docker for consistent and portable deployment.

---

## 🚀 Tech Stack

* **Backend:** Flask (Python)
    * **ORM:** SQLAlchemy
    * **Database:** PostgreSQL
    * **WSGI Server:** Gunicorn
* **Frontend:** React (JavaScript)
    * **Styling:** Tailwind CSS
* **Containerization:** Docker
* **API Docs:** Flask-Swagger-UI

---

## ⚙️ Local Setup

Follow these steps to get the application running on your local machine using Docker.

### Prerequisites

* [Docker Desktop](https://www.docker.com/products/docker-desktop) (or Docker Engine) installed and running.
* [PostgreSQL](https://www.postgresql.org/download/) installed and running locally, or accessible via a cloud provider.
* `psql` command-line tool for database dump restoration.

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd project-gutenberg-explorer # Or your project's root directory name
