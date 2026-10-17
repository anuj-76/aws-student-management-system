from flask import Flask, request, redirect, send_file
import mysql.connector
import boto3
import uuid
import mimetypes
import os
from io import BytesIO

app = Flask(**name**)

S3_BUCKET = "student-file-management-2026-anuj-7468"
s3 = boto3.client("s3")

DB_HOST = "student-db.cf4su24cmxop.ap-southeast-2.rds.amazonaws.com"
DB_USER = "admin"
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_NAME = "studentdb"

def get_db():
return mysql.connector.connect(
host=DB_HOST,
user=DB_USER,
password=DB_PASSWORD,
database=DB_NAME,
port=3306
)

@app.route("/")
def home():
search = request.args.get("search", "").strip()

```
db = get_db()
cursor = db.cursor()

if search:
    cursor.execute("""
        SELECT id, name, roll_no, email, filename
        FROM students
        WHERE name LIKE %s
        ORDER BY id DESC
    """, ("%" + search + "%",))
else:
    cursor.execute("""
        SELECT id, name, roll_no, email, filename
        FROM students
        ORDER BY id DESC
    """)

students = cursor.fetchall()

cursor.close()
db.close()

rows = ""

for student in students:
    student_id = student[0]
    name = student[1]
    roll_no = student[2]
    email = student[3]
    filename = student[4]

    if filename:
        document_status = "File Uploaded"

        view_button = f"""
            <a href="/view/{student_id}"
               class="view-btn"
               title="View Document">
                👁️
            </a>
        """
    else:
        document_status = "No File"

        view_button = """
            <span class="no-file">
                No File
            </span>
        """

    rows += f"""
    <tr>
        <td>{student_id}</td>
        <td><strong>{name}</strong></td>
        <td>{roll_no}</td>
        <td>{email or "-"}</td>
        <td>
            <span class="file-status">
                {document_status}
            </span>
        </td>
        <td>
            {view_button}
            <a href="/edit/{student_id}"
               class="edit-btn">
                Edit
            </a>
            <form action="/delete/{student_id}"
                  method="POST"
                  class="delete-form"
                  onsubmit="return confirm('Are you sure you want to delete this student?');">
                <button type="submit"
                        class="delete-btn">
                    Delete
                </button>
            </form>
        </td>
    </tr>
    """

if not rows:
    rows = """
    <tr>
        <td colspan="6" class="empty">
            No student records found.
        </td>
    </tr>
    """

return f"""
```

<!DOCTYPE html>

<html>
<head>
    <title>Student Management System</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * {{
            box-sizing: border-box;
        }}

```
    body {{
        margin: 0;
        font-family: Arial, sans-serif;
        background: #f4f6f8;
        color: #222;
    }}

    .header {{
        background: white;
        border-bottom: 1px solid #ddd;
        padding: 25px 40px;
    }}

    .header h1 {{
        margin: 0;
        font-size: 27px;
    }}

    .header p {{
        margin: 7px 0 0;
        color: #777;
        font-size: 14px;
    }}

    .container {{
        max-width: 1050px;
        margin: 35px auto;
        padding: 0 20px;
    }}

    .box {{
        background: white;
        padding: 28px;
        border-radius: 10px;
        margin-bottom: 25px;
        border: 1px solid #e1e1e1;
    }}

    .box h2 {{
        margin-top: 0;
        margin-bottom: 22px;
        font-size: 20px;
    }}

    .form {{
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 15px;
    }}

    input {{
        width: 100%;
        padding: 12px;
        border: 1px solid #ccc;
        border-radius: 6px;
        font-size: 14px;
    }}

    input:focus {{
        outline: none;
        border-color: #2563eb;
    }}

    .file-input {{
        grid-column: span 2;
    }}

    .add-btn {{
        grid-column: span 2;
        padding: 12px;
        border: none;
        border-radius: 6px;
        background: #2563eb;
        color: white;
        font-size: 15px;
        cursor: pointer;
    }}

    .add-btn:hover {{
        background: #1d4ed8;
    }}

    .search-form {{
        display: flex;
        gap: 10px;
        margin-bottom: 22px;
    }}

    .search-input {{
        flex: 1;
    }}

    .search-btn {{
        padding: 12px 22px;
        border: none;
        border-radius: 6px;
        background: #2563eb;
        color: white;
        font-size: 14px;
        cursor: pointer;
    }}

    .search-btn:hover {{
        background: #1d4ed8;
    }}

    .clear-btn {{
        display: inline-block;
        padding: 12px 18px;
        border-radius: 6px;
        background: #e5e7eb;
        color: #333;
        text-decoration: none;
        font-size: 14px;
    }}

    .clear-btn:hover {{
        background: #d1d5db;
    }}

    .table-container {{
        overflow-x: auto;
    }}

    table {{
        width: 100%;
        border-collapse: collapse;
    }}

    th {{
        background: #f7f7f7;
        text-align: left;
        padding: 14px;
        border-bottom: 1px solid #ddd;
        font-size: 13px;
    }}

    td {{
        padding: 14px;
        border-bottom: 1px solid #eee;
        font-size: 14px;
    }}

    tr:hover {{
        background: #fafafa;
    }}

    .file-status {{
        background: #e8f5e9;
        color: #16803c;
        padding: 6px 9px;
        border-radius: 5px;
        font-size: 12px;
    }}

    .no-file {{
        color: #888;
        font-size: 12px;
    }}

    .view-btn {{
        display: inline-block;
        background: #16a34a;
        color: white;
        text-decoration: none;
        padding: 8px 11px;
        border-radius: 5px;
        font-size: 16px;
        margin-right: 5px;
    }}

    .view-btn:hover {{
        background: #15803d;
    }}

    .edit-btn {{
        display: inline-block;
        background: #2563eb;
        color: white;
        text-decoration: none;
        padding: 8px 13px;
        border-radius: 5px;
        font-size: 12px;
        margin-right: 5px;
    }}

    .edit-btn:hover {{
        background: #1d4ed8;
    }}

    .delete-form {{
        display: inline;
    }}

    .delete-btn {{
        background: #dc2626;
        color: white;
        border: none;
        padding: 8px 13px;
        border-radius: 5px;
        cursor: pointer;
        font-size: 12px;
    }}

    .delete-btn:hover {{
        background: #b91c1c;
    }}

    .empty {{
        text-align: center;
        color: #777;
        padding: 30px;
    }}

    .footer {{
        text-align: center;
        color: #888;
        font-size: 12px;
        margin-top: 30px;
        padding-bottom: 25px;
    }}

    @media(max-width: 700px) {{
        .header {{
            padding: 20px;
        }}

        .container {{
            margin-top: 20px;
        }}

        .form {{
            grid-template-columns: 1fr;
        }}

        .file-input,
        .add-btn {{
            grid-column: span 1;
        }}

        .box {{
            padding: 20px;
        }}

        .search-form {{
            flex-direction: column;
        }}

        .search-btn,
        .clear-btn {{
            width: 100%;
            text-align: center;
        }}
    }}
</style>
```

</head>
<body>
    <div class="header">
        <h1>Student Management System</h1>
        <p>Manage student information and documents</p>
    </div>

```
<div class="container">
    <div class="box">
        <h2>Add Student</h2>
        <form class="form"
              action="/add"
              method="POST"
              enctype="multipart/form-data">
            <input type="text" name="name" placeholder="Student Name" required>
            <input type="text" name="roll_no" placeholder="Roll Number" required>
            <input type="email" name="email" placeholder="Email Address">
            <input class="file-input" type="file" name="file">
            <button type="submit" class="add-btn">Add Student</button>
        </form>
    </div>

    <div class="box">
        <h2>Student Details</h2>
        <form class="search-form" action="/" method="GET">
            <input class="search-input"
                   type="text"
                   name="search"
                   placeholder="Search student by name"
                   value="{search}">
            <button type="submit" class="search-btn">Search</button>
            <a href="/" class="clear-btn">Clear</a>
        </form>

        <div class="table-container">
            <table>
                <tr>
                    <th>ID</th>
                    <th>Name</th>
                    <th>Roll Number</th>
                    <th>Email</th>
                    <th>Document</th>
                    <th>Actions</th>
                </tr>
                {rows}
            </table>
        </div>
    </div>

    <div class="footer">Student Management System</div>
</div>
```

</body>
</html>
"""

@app.route("/add", methods=["POST"])
def add_student():
name = request.form["name"]
roll_no = request.form["roll_no"]
email = request.form["email"]

```
uploaded_file = request.files.get("file")
filename = None

db = get_db()
cursor = db.cursor()

cursor.execute("SELECT COUNT(*) FROM students")
count = cursor.fetchone()[0]

if count == 0:
    cursor.execute("ALTER TABLE students AUTO_INCREMENT = 1")

if uploaded_file and uploaded_file.filename:
    filename = (
        str(uuid.uuid4())
        + "_"
        + os.path.basename(uploaded_file.filename)
    )

    content_type = (
        uploaded_file.content_type
        or mimetypes.guess_type(uploaded_file.filename)[0]
        or "application/octet-stream"
    )

    s3.upload_fileobj(
        uploaded_file,
        S3_BUCKET,
        filename,
        ExtraArgs={"ContentType": content_type}
    )

cursor.execute(
    """
    INSERT INTO students (name, roll_no, email, filename)
    VALUES (%s, %s, %s, %s)
    """,
    (name, roll_no, email, filename)
)

db.commit()
cursor.close()
db.close()

return redirect("/")
```

@app.route("/view/[int:student_id](int:student_id)")
def view_document(student_id):
db = get_db()
cursor = db.cursor()

```
cursor.execute(
    "SELECT name, filename FROM students WHERE id = %s",
    (student_id,)
)

result = cursor.fetchone()
cursor.close()
db.close()

if not result or not result[1]:
    return """
    <h2>No document found.</h2>
    <a href="/">Back to Student Management System</a>
    """

student_name = result[0]
filename = result[1]
extension = os.path.splitext(filename)[1].lower()

image_extensions = [".jpg", ".jpeg", ".png", ".gif", ".webp"]
pdf_extensions = [".pdf"]

if extension in image_extensions:
    preview = f"""
    <img src="/file/{student_id}"
         class="image-preview"
         alt="Student Document">
    """
elif extension in pdf_extensions:
    preview = f"""
    <iframe src="/file/{student_id}"
            class="pdf-preview"></iframe>
    """
else:
    preview = """
    <div class="no-preview">
        <div class="icon">📄</div>
        <h3>Preview not available</h3>
        <p>This file type cannot be displayed directly in the browser.</p>
        <p>Click Download to open the file on your computer.</p>
    </div>
    """

return f"""
```

<!DOCTYPE html>

<html>
<head>
    <title>View Document</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * {{
            box-sizing: border-box;
        }}

```
    body {{
        margin: 0;
        font-family: Arial, sans-serif;
        background: #f4f6f8;
    }}

    .header {{
        background: white;
        padding: 20px 30px;
        border-bottom: 1px solid #ddd;
    }}

    .header h1 {{
        margin: 0;
        font-size: 23px;
    }}

    .container {{
        max-width: 1100px;
        margin: 30px auto;
        padding: 0 20px;
    }}

    .box {{
        background: white;
        padding: 25px;
        border-radius: 10px;
        border: 1px solid #ddd;
    }}

    .top {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 15px;
        margin-bottom: 20px;
    }}

    .top h2 {{
        margin: 0;
    }}

    .buttons a {{
        display: inline-block;
        padding: 10px 15px;
        border-radius: 6px;
        text-decoration: none;
        margin-left: 5px;
        font-size: 14px;
    }}

    .back {{
        background: #e5e7eb;
        color: #333;
    }}

    .download {{
        background: #2563eb;
        color: white;
    }}

    .download:hover {{
        background: #1d4ed8;
    }}

    .image-preview {{
        display: block;
        max-width: 100%;
        max-height: 700px;
        margin: auto;
        object-fit: contain;
        border: 1px solid #ddd;
        border-radius: 6px;
    }}

    .pdf-preview {{
        width: 100%;
        height: 700px;
        border: 1px solid #ddd;
        border-radius: 6px;
    }}

    .no-preview {{
        text-align: center;
        padding: 100px 20px;
        border: 1px solid #ddd;
        border-radius: 8px;
        background: #fafafa;
    }}

    .no-preview .icon {{
        font-size: 50px;
    }}

    .no-preview h3 {{
        margin-bottom: 8px;
    }}

    .no-preview p {{
        color: #777;
        font-size: 14px;
    }}

    @media(max-width: 700px) {{
        .top {{
            flex-direction: column;
            align-items: flex-start;
        }}

        .buttons {{
            width: 100%;
        }}

        .buttons a {{
            margin-left: 0;
            margin-right: 5px;
        }}

        .pdf-preview {{
            height: 600px;
        }}
    }}
</style>
```

</head>
<body>
    <div class="header">
        <h1>Student Management System</h1>
    </div>

```
<div class="container">
    <div class="box">
        <div class="top">
            <h2>Document - {student_name}</h2>
            <div class="buttons">
                <a href="/" class="back">Back</a>
                <a href="/download/{student_id}" class="download">Download</a>
            </div>
        </div>
        {preview}
    </div>
</div>
```

</body>
</html>
"""

@app.route("/file/[int:student_id](int:student_id)")
def secure_file(student_id):
db = get_db()
cursor = db.cursor()

```
cursor.execute(
    "SELECT filename FROM students WHERE id = %s",
    (student_id,)
)

result = cursor.fetchone()
cursor.close()
db.close()

if not result or not result[0]:
    return "Document not found.", 404

filename = result[0]

try:
    s3_object = s3.get_object(Bucket=S3_BUCKET, Key=filename)
    file_data = s3_object["Body"].read()

    content_type = (
        s3_object.get("ContentType")
        or mimetypes.guess_type(filename)[0]
        or "application/octet-stream"
    )

    response = send_file(
        BytesIO(file_data),
        mimetype=content_type,
        download_name=os.path.basename(filename),
        as_attachment=False
    )

    response.headers["Content-Disposition"] = (
        'inline; filename="{}"'.format(os.path.basename(filename))
    )

    return response

except Exception as e:
    print("S3 view error:", e)
    return "Unable to open document.", 500
```

@app.route("/download/[int:student_id](int:student_id)")
def download_document(student_id):
db = get_db()
cursor = db.cursor()

```
cursor.execute(
    "SELECT filename FROM students WHERE id = %s",
    (student_id,)
)

result = cursor.fetchone()
cursor.close()
db.close()

if not result or not result[0]:
    return "Document not found.", 404

filename = result[0]

try:
    s3_object = s3.get_object(Bucket=S3_BUCKET, Key=filename)
    file_data = s3_object["Body"].read()

    content_type = (
        s3_object.get("ContentType")
        or mimetypes.guess_type(filename)[0]
        or "application/octet-stream"
    )

    return send_file(
        BytesIO(file_data),
        mimetype=content_type,
        download_name=os.path.basename(filename),
        as_attachment=True
    )

except Exception as e:
    print("S3 download error:", e)
    return "Unable to download document.", 500
```

@app.route("/edit/[int:student_id](int:student_id)", methods=["GET", "POST"])
def edit_student(student_id):
db = get_db()
cursor = db.cursor()

```
if request.method == "POST":
    name = request.form["name"]
    roll_no = request.form["roll_no"]
    email = request.form["email"]
    uploaded_file = request.files.get("file")

    cursor.execute(
        "SELECT filename FROM students WHERE id = %s",
        (student_id,)
    )

    old_result = cursor.fetchone()
    old_filename = old_result[0] if old_result else None

    if uploaded_file and uploaded_file.filename:
        new_filename = (
            str(uuid.uuid4())
            + "_"
            + os.path.basename(uploaded_file.filename)
        )

        content_type = (
            uploaded_file.content_type
            or mimetypes.guess_type(uploaded_file.filename)[0]
            or "application/octet-stream"
        )

        s3.upload_fileobj(
            uploaded_file,
            S3_BUCKET,
            new_filename,
            ExtraArgs={"ContentType": content_type}
        )

        if old_filename:
            try:
                s3.delete_object(Bucket=S3_BUCKET, Key=old_filename)
            except Exception as e:
                print("Old S3 document delete error:", e)

        cursor.execute(
            """
            UPDATE students
            SET name = %s, roll_no = %s, email = %s, filename = %s
            WHERE id = %s
            """,
            (name, roll_no, email, new_filename, student_id)
        )
    else:
        cursor.execute(
            """
            UPDATE students
            SET name = %s, roll_no = %s, email = %s
            WHERE id = %s
            """,
            (name, roll_no, email, student_id)
        )

    db.commit()
    cursor.close()
    db.close()

    return redirect("/")

cursor.execute(
    """
    SELECT name, roll_no, email, filename
    FROM students
    WHERE id = %s
    """,
    (student_id,)
)

student = cursor.fetchone()
cursor.close()
db.close()

if not student:
    return "Student not found.", 404

name = student[0]
roll_no = student[1]
email = student[2] or ""
filename = student[3]

if filename:
    document_text = "Current document uploaded"
else:
    document_text = "No document uploaded"

return f"""
```

<!DOCTYPE html>

<html>
<head>
    <title>Edit Student</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * {{
            box-sizing: border-box;
        }}

```
    body {{
        margin: 0;
        font-family: Arial, sans-serif;
        background: #f4f6f8;
    }}

    .header {{
        background: white;
        padding: 25px 40px;
        border-bottom: 1px solid #ddd;
    }}

    .header h1 {{
        margin: 0;
        font-size: 27px;
    }}

    .container {{
        max-width: 700px;
        margin: 35px auto;
        padding: 0 20px;
    }}

    .box {{
        background: white;
        padding: 30px;
        border-radius: 10px;
        border: 1px solid #ddd;
    }}

    h2 {{
        margin-top: 0;
    }}

    label {{
        display: block;
        margin-top: 16px;
        margin-bottom: 7px;
        font-size: 14px;
        font-weight: bold;
    }}

    input {{
        width: 100%;
        padding: 12px;
        border: 1px solid #ccc;
        border-radius: 6px;
        font-size: 14px;
    }}

    .current-file {{
        margin-top: 15px;
        padding: 12px;
        background: #f7f7f7;
        border-radius: 6px;
        color: #555;
        font-size: 13px;
    }}

    .buttons {{
        margin-top: 25px;
    }}

    .update-btn {{
        background: #2563eb;
        color: white;
        border: none;
        padding: 12px 20px;
        border-radius: 6px;
        cursor: pointer;
    }}

    .back-btn {{
        display: inline-block;
        background: #e5e7eb;
        color: #333;
        text-decoration: none;
        padding: 12px 20px;
        border-radius: 6px;
        margin-left: 8px;
    }}
</style>
```

</head>
<body>
    <div class="header">
        <h1>Student Management System</h1>
    </div>

```
<div class="container">
    <div class="box">
        <h2>Edit Student</h2>

        <form action="/edit/{student_id}"
              method="POST"
              enctype="multipart/form-data">
            <label>Student Name</label>
            <input type="text" name="name" value="{name}" required>

            <label>Roll Number</label>
            <input type="text" name="roll_no" value="{roll_no}" required>

            <label>Email Address</label>
            <input type="email" name="email" value="{email}">

            <label>Replace Document</label>
            <input type="file" name="file">

            <div class="current-file">{document_text}</div>

            <div class="buttons">
                <button type="submit" class="update-btn">Update Student</button>
                <a href="/" class="back-btn">Cancel</a>
            </div>
        </form>
    </div>
</div>
```

</body>
</html>
"""

@app.route("/delete/[int:student_id](int:student_id)", methods=["POST"])
def delete_student(student_id):
db = get_db()
cursor = db.cursor()

```
cursor.execute(
    "SELECT filename FROM students WHERE id = %s",
    (student_id,)
)

result = cursor.fetchone()

if result and result[0]:
    try:
        s3.delete_object(Bucket=S3_BUCKET, Key=result[0])
    except Exception as e:
        print("S3 delete error:", e)

cursor.execute(
    "DELETE FROM students WHERE id = %s",
    (student_id,)
)

db.commit()

cursor.execute("SELECT COUNT(*) FROM students")
remaining_students = cursor.fetchone()[0]

if remaining_students == 0:
    cursor.execute("ALTER TABLE students AUTO_INCREMENT = 1")
    db.commit()

cursor.close()
db.close()

return redirect("/")
```

if **name** == "**main**":
app.run(host="0.0.0.0", port=80)
