# AWS Student Management System

A cloud-based Student Management System built using Python Flask and Amazon Web Services (AWS). The application allows staff to manage student records and documents through a web interface while using AWS services for compute, storage, database management, and serverless processing.

## Project Overview

The project demonstrates how a web application can be deployed on AWS using a combination of compute, database, object storage, identity and access management, and monitoring services.

Staff can add, view, search, edit, and delete student records. Documents can be uploaded to Amazon S3 and viewed or downloaded through the application.

## Features

* Add student records with name, roll number, and email.
* Automatically generate student IDs.
* Search students by name.
* Edit existing student information.
* Upload and replace student documents.
* Preview supported image files and PDFs in the browser.
* Download uploaded documents.
* Delete student records and their associated documents.
* Store student information in Amazon RDS.
* Store documents in a private Amazon S3 bucket.
* Access AWS resources through an EC2 IAM role.
* Process S3 upload events using AWS Lambda.
* Monitor serverless execution using Amazon CloudWatch.

## AWS Architecture

The application uses the following AWS services:

| AWS Service          | Purpose                                         |
| -------------------- | ----------------------------------------------- |
| Amazon EC2           | Hosts the Flask web application                 |
| Amazon RDS for MySQL | Stores student records                          |
| Amazon S3            | Stores student documents                        |
| AWS IAM              | Manages permissions for accessing AWS resources |
| AWS Lambda           | Processes configured S3 upload events           |
| Amazon CloudWatch    | Stores Lambda execution logs                    |

### Application Workflow

1. Staff interact with the Flask application through a web browser.
2. The application runs on an Amazon EC2 instance.
3. Student information is stored in an Amazon RDS MySQL database.
4. Uploaded documents are stored in an Amazon S3 bucket.
5. An S3 object-creation event triggers the configured Lambda function.
6. Lambda execution logs are available in Amazon CloudWatch.

## Prerequisites

Before building the project, make sure you have the following:

### 1. AWS Account

Create an AWS account through the official AWS website.

You should have access to:

* Amazon EC2
* Amazon RDS
* Amazon S3
* AWS IAM
* AWS Lambda
* Amazon CloudWatch

Check the pricing of each service before creating resources. Some services may incur charges even when the application is not actively being used.

### 2. Basic Technical Knowledge

A basic understanding of the following is helpful:

* Python fundamentals
* HTML and CSS
* MySQL and SQL queries
* Linux terminal commands
* Basic AWS networking and security groups
* AWS IAM roles and permissions

### 3. Required Software

Install or prepare the following:

* Python 3
* pip, the Python package installer
* A code editor such as Visual Studio Code
* A web browser
* An SSH client for connecting to EC2
* A MySQL client, if you want to test the database separately

### 4. AWS Resources

You will need:

* An EC2 instance running a compatible operating system.
* An RDS MySQL database.
* A private S3 bucket.
* An IAM role attached to EC2 with the necessary S3 permissions.
* A Lambda function with permissions to write execution logs.
* An S3 event notification configured to invoke Lambda.
* A CloudWatch log group for Lambda logs.

Resource names, regions, database settings, and network configuration can differ between deployments.

## Step-by-Step Setup Guide

### Step 1: Create an S3 Bucket

1. Open the Amazon S3 console.
2. Select **Create bucket**.
3. Choose a globally unique bucket name.
4. Select your preferred AWS region.
5. Keep Block Public Access enabled.
6. Create the bucket.

Use this bucket to store student documents.

**Security recommendation:** Do not make the bucket public. The application should access documents using its EC2 IAM role.

### Step 2: Create an RDS MySQL Database

1. Open the Amazon RDS console.
2. Select **Create database**.
3. Choose MySQL as the database engine.
4. Select an appropriate development configuration.
5. Configure the database identifier and master username.
6. Set a strong database password.
7. Configure connectivity and security groups.
8. Create the database and wait until it becomes available.
9. Record the database endpoint, port, database name, username, and password securely.

Use a database name such as `studentdb`.

Configure the database security group to allow MySQL traffic on port `3306` only from the EC2 instance's security group.

**Important:** Avoid exposing the RDS database directly to the public internet.

### Step 3: Create the Database Table

Connect to the RDS MySQL database using an approved MySQL client or database connection method.

Create the database if it does not already exist:

```sql
CREATE DATABASE studentdb;
USE studentdb;
```

Create the students table:

```sql
CREATE TABLE students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    roll_no VARCHAR(50) NOT NULL,
    email VARCHAR(150),
    filename VARCHAR(500)
);
```

The table stores student information and the S3 object key associated with each uploaded document.

### Step 4: Configure IAM Permissions

Create or configure an IAM role for the EC2 instance.

The role should provide only the permissions required by the application, such as:

* Uploading documents to the designated S3 bucket.
* Retrieving documents from the bucket.
* Deleting documents from the bucket when required.

Attach the role to the EC2 instance through its IAM instance profile.

Avoid storing long-term AWS access keys directly in the application code.

If you configure S3 event notifications to invoke Lambda, make sure Lambda has the appropriate execution permissions and the necessary permission to be invoked by S3.

### Step 5: Launch an EC2 Instance

1. Open the Amazon EC2 console.
2. Launch an instance using a suitable Linux AMI.
3. Choose an instance type appropriate for testing.
4. Configure the network and security group.
5. Attach the IAM role created earlier.
6. Launch the instance.

Configure inbound rules according to your deployment:

* SSH, port `22`: restrict access to your own IP address.
* HTTP, port `80`: allow access only as required for your demonstration.

For production deployments, use HTTPS and stronger access controls.

### Step 6: Connect to EC2

Connect to your EC2 instance using SSH.

Update the package lists and install Python and pip using the package manager appropriate for your selected operating system.

For Amazon Linux, you can use:

```bash
sudo dnf update -y
sudo dnf install python3 python3-pip -y
```

If your AMI uses a different package manager, use its corresponding installation commands.

### Step 7: Download the Project Code

Clone the repository:

```bash
git clone https://github.com/YOUR-USERNAME/aws-student-management-system.git
```

Navigate to the project directory:

```bash
cd aws-student-management-system
```

Replace `YOUR-USERNAME` with your GitHub username.

If you uploaded the files directly through the GitHub website, ensure the repository contains the application code and dependency file.

### Step 8: Install Python Dependencies

Create a `requirements.txt` file containing:

```text
Flask
mysql-connector-python
boto3
```

Install the dependencies:

```bash
python3 -m pip install -r requirements.txt
```

The application uses Flask for the web interface, MySQL Connector for database operations, and Boto3 to interact with AWS services.

### Step 9: Configure Database Credentials

The application needs the following configuration values:

* `DB_HOST`: RDS endpoint.
* `DB_USER`: MySQL username.
* `DB_PASSWORD`: MySQL password.
* `DB_NAME`: database name.
* `S3_BUCKET`: S3 bucket name.

For an application that reads its database password from an environment variable, set it in the EC2 shell before starting the application:

```bash
export DB_HOST="YOUR_RDS_ENDPOINT"
export DB_USER="YOUR_DB_USERNAME"
export DB_PASSWORD="YOUR_DB_PASSWORD"
export DB_NAME="studentdb"
```

Configure the S3 bucket name in the application to match the bucket you created.

Do not commit real database passwords, AWS access keys, private keys, or other secrets to GitHub.

For long-term deployments, consider using AWS Secrets Manager or Systems Manager Parameter Store to manage sensitive configuration.

### Step 10: Configure AWS Lambda

1. Open the AWS Lambda console.
2. Create a Lambda function using a supported Python runtime.
3. Add the code required to process S3 object-creation events.
4. Configure the execution role with the necessary permissions.
5. Configure the S3 bucket event notification for object creation.
6. Allow the S3 bucket to invoke the Lambda function.
7. Test the function by uploading a file to the configured bucket.

The Lambda function's actual behavior depends on the code deployed with it.

### Step 11: Configure CloudWatch Monitoring

1. Open the Amazon CloudWatch console.
2. Navigate to **Logs → Log groups**.
3. Open the log group associated with your Lambda function.
4. Review execution logs and error messages.
5. Invoke the function again if you need to troubleshoot an event.

CloudWatch helps you investigate Lambda execution failures and understand whether the configured event processing is working.

### Step 12: Start the Application

From the project directory, start the Flask application:

```bash
python3 app.py
```

If the application is configured to listen on port `80`, make sure the instance has the required permissions to bind to that port.

For development, running Flask on an unprivileged port such as `5000` is often simpler. If you change the application port, update the network rules and access URL accordingly.

Open the EC2 instance's reachable address in your browser to test the application.

### Step 13: Test the Features

Verify the following operations:

1. Add a student without a document.
2. Add a student with an image or PDF.
3. Search for a student by name.
4. Edit the student's details.
5. Replace an uploaded document.
6. Open the document preview.
7. Download the document.
8. Delete a student and verify the associated document is removed.
9. Upload an object to S3 and check whether the Lambda function is triggered.
10. Review Lambda logs in CloudWatch.

Also test what happens when a student has no document or when the requested record does not exist.

## Repository Structure

A possible repository structure is:

```text
aws-student-management-system/
├── app.py
├── requirements.txt
├── lambda_function.py
├── README.md
└── screenshots/
```

Include only the files that actually belong to your implementation. If the Lambda code is stored separately, document its location and deployment procedure.

Do not upload Terraform state files, private keys, environment files containing secrets, database passwords, or other sensitive information.

## Security Considerations

* Keep the S3 bucket private.
* Use an EC2 IAM role instead of hardcoded AWS access keys.
* Restrict RDS access to trusted security groups.
* Never commit real passwords or credentials to GitHub.
* Avoid exposing SSH to all IP addresses.
* Validate uploaded files and restrict file types and sizes.
* Use authentication and authorization to protect student records.
* Use HTTPS for deployments accessible over the internet.
* Apply least-privilege IAM permissions.
* Review AWS billing and remove unused resources after testing.

This repository is intended as a learning project. Additional security hardening is recommended before using it with real student information.

## Cost Management and Cleanup

AWS resources can incur charges depending on their configuration and usage.

When the project demonstration is complete:

1. Stop the EC2 instance if you no longer need it running.
2. Stop the RDS instance if its configuration supports stopping it and you no longer need it running.
3. Check for EBS volumes, snapshots, public IPv4 addresses, and other resources that may still incur charges.
4. Review S3 objects and storage usage.
5. Review Lambda invocations and CloudWatch log storage.
6. Delete resources you no longer need, after backing up anything important.

Stopping EC2 and RDS does not necessarily eliminate all charges. For example, storage and backups may continue to incur costs.

Before deleting the S3 bucket or RDS database, make sure you no longer need the stored documents or student records.

## Learning Outcomes

Through this project, you can gain practical experience with:

* Deploying a Python web application on AWS.
* Connecting an application to a managed MySQL database.
* Using Amazon S3 for document storage.
* Managing AWS permissions through IAM roles.
* Building event-driven workflows using Lambda and S3.
* Monitoring serverless functions through CloudWatch.
* Configuring AWS networking and security groups.
* Troubleshooting cloud application deployments.
* Managing cloud resources and costs.

## Future Improvements

Possible enhancements include:

* Staff login and role-based access control.
* HTTPS configuration.
* Improved form validation and error handling.
* Pagination for larger student datasets.
* Automated backups and recovery procedures.
* Infrastructure deployment automation.
* CI/CD using GitHub Actions.
* Centralized secrets management.
* Security scanning and application monitoring.

## Disclaimer

This project was developed for educational purposes to demonstrate cloud application development and AWS service integration. Do not use real student records or sensitive personal information in an unsecured demonstration environment.
