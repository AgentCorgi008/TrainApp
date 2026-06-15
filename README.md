# TrainApp

A mobile fitness application built with Python, KivyMD, and Firebase.

The project was developed as a complete workout management platform that allows users to browse exercises, create personalized workout programs, schedule training sessions, and track their fitness routine through an intuitive mobile interface.

## 🛠 Features

- User authentication
- Firebase Firestore integration
- Exercise database
- Workout program creation
- Weekly workout calendar
- Exercise details screen
- Muscle group categorization
- Dynamic UI built with KivyMD
- Mobile-first architecture
- Cloud data synchronization

## 🛠 Technologies

- Python
- Kivy
- KivyMD
- Firebase Authentication
- Firestore Database
- Object-Oriented Programming (OOP)

## 🚀 Installation

- Clone the repository: git clone https://github.com/SweetDosya/TrainApp.git
- Install dependencies: pip install kivymd, firebase_admin
- Configure Firebase credentials.
- Run the application: python main.py

## 🏗 Application Structure

```text
  Authentication
  │
  ├── User Profile
  │
  ├── Exercise Database
  │   ├── Chest
  │   ├── Back
  │   ├── Legs
  │   ├── Shoulders
  │   └── Arms
  │
  ├── Workout Programs
  │   ├── Create Program
  │   ├── Manage Exercises
  │   └── Save To Cloud
  │
  └── Workout Calendar
      └── Schedule Programs
```
## 💡 Code Example

If you want to understand the project architecture, start with the user workout management flow. The application revolves around workout programs, exercise collections, and calendar scheduling synchronized through Firebase Firestore.
```python
program_data = {
    "name": "Push Day",
    "exercises": selected_exercises,
    "exercise_count": len(selected_exercises)
}

user_db.create_workout_program(program_data)
```

This demonstrates the core idea behind the application: creating and managing workout programs that can later be assigned to specific days within the workout calendar.

## Design Goals
- Mobile-first user experience
- Easy workout customization
- Future Improvements
- Offline mode support

## 📸 Screenshots

<img width="618" height="793" alt="image" src="https://github.com/user-attachments/assets/85f2ba66-b950-4fed-9a46-0b8250a9c331" /> <br>

<img width="617" height="786" alt="image" src="https://github.com/user-attachments/assets/393faf71-f8db-42b3-a897-5f502db8fd2e" /> <br>

<img width="617" height="781" alt="image" src="https://github.com/user-attachments/assets/160d360c-4e41-4858-ae03-4b5ed0d3f12c" />

## 🧑‍💻 Author

Developed by SweetDosya as a personal mobile application project focused on fitness management and cloud-based workout planning.
