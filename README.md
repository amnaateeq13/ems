# Education Management System (EMS)

##  Project Overview
The Education Management System (EMS) is a Django-based platform designed to streamline the academic and administrative processes of educational institutions. The system integrates multiple modules, including identity management, courses, attendance, exams, fees, timetable, communication, and role-based dashboards for administrators, teachers, students, and parents.

The platform ensures secure role-based access, efficient record management, and improved collaboration between stakeholders. It is modular, scalable, and can be extended to meet the needs of schools, colleges, or universities.

##  Installation Instructions
Follow these steps to set up the project on your local machine:

# Navigate to project directory
cd ems_project



### **2️⃣ Set Up a Virtual Environment**
python -m venv env        # Create a virtual environment  
source env/bin/activate   # Activate (For macOS/Linux)  
env\Scripts\activate      # Activate (For Windows)  




### **3️⃣ Install Required Dependencies**

pip install -r requirements.txt



### **5️⃣ Apply Migrations**

python manage.py makemigrations 
python manage.py migrate



### **7️⃣ Run the Development Server**

python manage.py runserver

The system will be accessible at http://127.0.0.1:8000/


##  Usage Guide
### **🔹 User Roles & Features**
1️⃣ Administrator (Admin):

Manage all users (students, teachers, parents).

Assign roles and courses.

Oversee attendance, results, timetable, and fees.

Post announcements and monitor system activity.

2️⃣ Teacher:

Manage course allocations.

Upload exam results.

Mark attendance for enrolled students.

Send announcements and communicate with students/parents.

3️⃣ Student:

View personal profile, timetable, and courses.

Check attendance records and percentages.

Access exam results and grades.

Receive announcements from teachers and administrators.

4️⃣ Parent:

Monitor their child’s attendance and results.

View announcements and communicate with teachers/admin.

Manage their profile and linked student accounts.

## 🔑 Superuser Credentials (For Admin)
```
user: amna
Password: amna
```
## 🔑 Teacher Credentials (For Test)
user: Amir (use capital A as per case sensitivity )
Password: Amir@1234

## 🔑 Student  Credentials (For Test)
Username: Rao (use capital R as per case sensitivity )
Password: Rao@1234
## 🔑 Parents  Credentials (For Test)
Username: Sohail (use capital A as per case sensitivity )
Password: Soh@1234
