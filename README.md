# Edu-Track

**Edu-Track** is a modern educational platform designed to make the learning and teaching process intuitive, structured, and transparent. It brings students and teachers together into a unified ecosystem where learning is organized and feedback is seamless.

### Navigation

* [Technologies](#technologies)
* [Features](#features)
* [User Roles](#user-roles)
* [Installation](#installation)

---

### Technologies

**Edu-Track** is built using a robust and modern tech stack:

* **Backend:** Python, Django
* **Frontend:** HTML5, CSS3, Tailwind CSS (for a fast, responsive, and modern interface)
* **Database:** PostgreSQL
* **Infrastructure:** Docker, Docker-Compose

---

### Features

* **Course Creation:** Teachers can easily structure their curriculum by creating courses, adding lessons, and managing practical assignments.
* **Assignment Workflow:** A complete cycle of interaction: task submission by students, review and feedback by teachers, and final grading.
* **Progress Tracking:** Students can monitor their academic performance, view received grades, and track their history of completed materials.
* **Modern UI:** A clean, adaptive design that provides a seamless user experience across all devices.

---

### User Roles

* **Administrator:** Full access to platform management and user control.
* **Teacher:** Creates and manages courses, oversees lesson plans, grades assignments, and provides feedback.
* **Student:** Enrolls in courses, studies materials, submits assignments, and tracks personal statistics.
* **Guest:** Read-only access to browse the platform.

---

### Installation

> **Requirement:** Ensure you have Docker and Docker-Compose installed on your machine.

1. **Clone the repository and navigate to the project directory:**
```bash
git clone https://github.com/l11v44/Edu-Track
cd Edu-Track

```


2. **Launch the project using Docker:**
```bash
docker-compose up --build

```


3. **Run database migrations:**
```bash
docker-compose exec web python manage.py migrate

```
4. **Initialize Admin Account**
```bash
docker compose exec -e DJANGO_SUPERUSER_PASSWORD=your_secure_password web python manage.py createsuperuser --noinput --username admin --email admin@example.com

```

5. **Access the application:**
Open [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser.


*Author: lav4* *«Edu-Track — Making education simple and accessible for everyone.»*