# AWS Student Management System

A web-based Student Management System built using Python Flask and AWS services to help faculty and staff manage student records and documents through a simple dashboard.

## Overview

The application provides a centralized interface for managing student information, searching records, updating details, and handling student documents. AWS services provide database storage, file storage, server-side processing, and monitoring.

## Features

* **Staff Login:** Login page for staff access.
* **Add Student:** Create student records with relevant details.
* **View Student Records:** Display saved student information.
* **Search Students:** Find student records by name.
* **Edit Student Details:** Update existing student information.
* **Delete Student:** Remove student records when required.
* **Document Management:** Upload, view, and download student documents.
* **Cloud Storage:** Store uploaded files using Amazon S3.
* **Serverless Processing:** Process S3 upload events using AWS Lambda.
* **Monitoring:** Use Amazon CloudWatch to monitor Lambda execution logs.

## Technology Stack

### Application

* Python
* Flask
* HTML and CSS

### AWS Services

* Amazon EC2 — Application hosting
* Amazon RDS for MySQL — Relational database
* Amazon S3 — Student document storage
* AWS Lambda — Event-driven file processing
* Amazon CloudWatch — Logs and monitoring
* AWS IAM — Permissions and access management

## Architecture

1. Staff accesses the web application.
2. The Flask application handles student record operations.
3. Amazon RDS for MySQL stores student information.
4. Amazon S3 stores uploaded student documents.
5. An S3 upload event triggers AWS Lambda.
6. Amazon CloudWatch records Lambda execution logs.

## Project Structure

```text
aws-student-management-system/
├── app.py
├── requirements.txt
├── lambda_function.py
├── README.md
└── screenshots/
    ├── login-page.png
    └── dashboard.png
```

*The structure above is a suggested layout; actual filenames may differ.*

## Prerequisites

* Python 3
* An AWS account
* An Amazon RDS for MySQL database
* An Amazon S3 bucket
* Appropriate AWS IAM permissions
* AWS CLI or another method to configure AWS credentials, if required

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/aws-student-management-system.git
cd aws-student-management-system
```

Replace `YOUR-USERNAME` with your GitHub username.

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

Configure the database connection and application secrets through environment variables rather than hardcoding credentials in the source code.

Typical configuration variables include:

* `DB_HOST`
* `DB_USER`
* `DB_PASSWORD`
* `DB_NAME`
* `LOGIN_ID`
* `LOGIN_PASSWORD`
* `FLASK_SECRET_KEY`

Use your own database settings and strong credentials. Never commit passwords, AWS access keys, private keys, or `.env` files to GitHub.

### 4. Run the application

After configuring the required environment variables and database connectivity, start the application using the command appropriate to the Flask entry point.

## Security Considerations

* Keep database credentials and application secrets outside the source code.
* Follow the principle of least privilege when configuring AWS IAM permissions.
* Restrict database access to trusted application resources.
* Avoid exposing SSH access to the entire internet.
* Use HTTPS and appropriate authentication controls before deploying an application for real users.
* Do not upload Terraform state files, private keys, passwords, or other sensitive configuration files to the repository.

## Learning Outcomes

This project demonstrates practical experience with:

* Python web application development
* Relational database integration
* AWS compute, storage, and database services
* Event-driven serverless processing
* Cloud logging and monitoring
* Application configuration and cloud security fundamentals

## Disclaimer

This project was developed for educational and demonstration purposes. Additional security hardening and testing are required before production use.

## Author

**Anuj Shinde**




