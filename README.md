
# 🏋️ AI Health & Fitness Agent

> **An AI-powered health and fitness assistant that calculates body metrics, generates personalized meal and workout plans, and provides real-time fitness coaching using Google's Gemini AI.**

---

# 📖 Overview

Maintaining a healthy lifestyle requires understanding your body's nutritional requirements, estimating daily calorie needs, following structured workout plans, and making informed dietary choices. However, calculating these metrics manually and designing a balanced fitness routine can be time-consuming and confusing for many individuals.

**AI Health & Fitness Agent** is an intelligent fitness assistant that combines traditional health metric calculations with the reasoning capabilities of **Google Gemini AI** to deliver highly personalized nutrition guidance, workout recommendations, and interactive fitness coaching.

The application computes scientifically accepted health metrics such as **BMI, BMR, TDEE, ideal weight range, calorie targets, and macronutrient distribution** locally, while leveraging **Gemini 2.5 Flash** to generate customized meal plans, workout schedules, and answer user fitness questions in natural language.

The project is available in two implementations:

- **Streamlit Application (Python Backend)** — Recommended for deployment and production use.
- **Standalone Browser Version (HTML, CSS, JavaScript)** — No installation required; interacts directly with the Gemini API.

---

# ✨ Features

## 📊 Health Metrics Calculator

Automatically calculates

- Body Mass Index (BMI)
- Basal Metabolic Rate (BMR)
- Total Daily Energy Expenditure (TDEE)
- Daily Calorie Requirement
- Ideal Weight Range
- Daily Macronutrient Distribution
- Personalized Fitness Goal Metrics

---

## 📈 Visual BMI Dashboard

Interactive BMI visualization including

- Underweight
- Healthy Weight
- Overweight
- Obesity

with a live indicator showing the user's current BMI position.

---

## 🥗 AI Meal Planner

Generate personalized daily meal plans based on

- Daily calorie target
- Weight goal
- Dietary preference
- Nutritional requirements

Supported diets include

- Vegetarian
- Vegan
- High Protein
- Keto
- Mediterranean
- No Restrictions

Each meal plan includes

- Breakfast
- Morning Snack
- Lunch
- Evening Snack
- Dinner

---

## 💪 AI Workout Generator

Automatically creates personalized weekly workout schedules based on

- Fitness goal
- Training frequency
- Equipment availability
- Current fitness level

Workout plans include

- Strength Training
- Cardio
- Flexibility
- Recovery
- Progressive Weekly Structure

---

## 🤖 AI Fitness Coach

Chat directly with Gemini AI for

- Nutrition advice
- Exercise guidance
- Muscle gain strategies
- Weight loss recommendations
- Recovery tips
- Healthy lifestyle habits

The AI remembers the user's health profile during the session to provide contextual responses.

---

## 📥 Download Plans

Export

- Meal Plans
- Workout Programs

as downloadable text files for offline access.

---

# 🏗️ Architecture


                    User Profile
      (Age, Gender, Height, Weight,
       Activity Level, Goal, Diet)
                    │
                    ▼
        Health Metrics Calculation Engine
        (BMI • BMR • TDEE • Calories)
                    │
                    ▼
         User Health Profile Generation
                    │
         ┌──────────┼─────────────┐
         ▼          ▼             ▼
    Meal Planner  Workout AI   Coach Chat
         │          │             │
         └──────────┼─────────────┘
                    ▼
             Google Gemini API
                    │
                    ▼
        Personalized AI Responses
                    │
                    ▼
        Streamlit Dashboard / Browser


---

# 🧮 Health Metrics Explained

The application calculates several key health metrics using established formulas.

## Body Mass Index (BMI)

BMI estimates whether a person's weight falls within a healthy range.

```
BMI = Weight (kg) / Height² (m²)
```

Classification

| BMI | Category |
|------|----------|
| < 18.5 | Underweight |
| 18.5 – 24.9 | Normal |
| 25 – 29.9 | Overweight |
| ≥ 30 | Obese |

---

## Basal Metabolic Rate (BMR)

BMR represents the number of calories your body requires at complete rest.

The application uses the **Mifflin–St Jeor Equation**, one of the most widely accepted formulas for estimating daily energy expenditure.

---

## Total Daily Energy Expenditure (TDEE)

TDEE estimates the total calories burned in a day.

```
TDEE = BMR × Activity Multiplier
```

Activity multipliers

| Activity Level | Multiplier |
|----------------|-----------|
| Sedentary | 1.20 |
| Lightly Active | 1.375 |
| Moderately Active | 1.55 |
| Very Active | 1.725 |
| Extremely Active | 1.90 |

---

## Daily Calorie Goal

The application adjusts calorie targets based on the selected fitness goal.

| Goal | Adjustment |
|------|------------|
| Weight Loss | TDEE − 500 kcal |
| Maintenance | TDEE |
| Muscle Gain | TDEE + 300 kcal |

---

## Macronutrient Distribution

The application recommends daily protein, carbohydrate, and fat intake based on the calorie goal.

Typical distributions

- Protein
- Carbohydrates
- Healthy Fats

These recommendations are automatically adjusted according to the selected fitness objective.

---

# ⚙️ Tech Stack

## Frontend

### Streamlit Version

- Streamlit
- Python

### Browser Version

- HTML5
- CSS3
- JavaScript

---

## Artificial Intelligence

- Google Gemini 2.5 Flash
- Google Generative Language API

---

## Configuration

- Python Dotenv
- Environment Variables

---

# 📂 Project Structure

```
health_fitness_agent/

├── app.py
├── health_metrics.py
├── requirements.txt
├── index.html
├── .env
├── README.md
└── screenshots/
```
---

# 🎯 Key Highlights

- AI-powered personalized health and fitness assistant.
- Accurate BMI, BMR, TDEE, calorie, and macro calculations.
- Personalized AI-generated meal plans.
- Weekly AI workout planner.
- Interactive Gemini-powered fitness coach.
- Downloadable meal and workout plans.
- Streamlit and browser-based implementations.
- Local health metric calculations with cloud-based AI reasoning.

---

# 🚀 Installation & Setup

## Prerequisites

Before running the project, make sure the following software is installed.

| Software | Version |
|----------|----------|
| Python | 3.10 or above |
| pip | Latest |
| Git | Latest |
| Streamlit | Installed through requirements |
| Google Gemini API Key | Required |

---

# 📥 Clone the Repository

Clone the project from GitHub.

```bash
git clone https://github.com/jyotshna068/Fitness_aiAgent.git

cd Fitness_aiAgent
```

---

# 🐍 Create a Virtual Environment

Creating a virtual environment is recommended to isolate project dependencies.

### Windows

```bash
python -m venv venv

venv\Scripts\activate
```

### macOS / Linux

```bash
python3 -m venv venv

source venv/bin/activate
```

---

# 📦 Install Dependencies

Install all required Python packages.

```bash
pip install -r requirements.txt
```

Example packages include:

- streamlit
- google-generativeai
- python-dotenv

---

# 🔑 Get a Gemini API Key

The application requires a Google Gemini API key.


# ⚙ Configure Environment Variables

Create a file named

```
.env
```

inside the project directory.

Add your API key.

```env
GOOGLE_API_KEY=YOUR_GEMINI_API_KEY
```
---

# ▶ Run the Streamlit Application

Start the application.

```bash
streamlit run app.py
```

After a few seconds Streamlit will launch automatically.

Open

```
http://localhost:8501
```

if it does not open automatically.

---

# 🌐 Running the Browser Version

The project also contains a standalone browser version.

Simply open

```
index.html
```

using any modern browser.

Supported browsers include

- Chrome
- Edge
- Firefox
- Brave

When prompted,

paste your Gemini API key.

The key is stored only in

```
sessionStorage
```

for the current browser session.

No backend server is required.

---
````markdown id="r2x8pf"

# 🚀 Deployment

## Streamlit Community Cloud

### Step 1

Push the project to GitHub.

---

### Step 2

Sign in to

https://share.streamlit.io

---

### Step 3

Create a new application.

---

### Step 4

Select

- Repository
- Branch
- `app.py`

---

### Step 5

Add the following secret.

```toml
GOOGLE_API_KEY="YOUR_API_KEY"
```

---

### Step 6

Click **Deploy**.

After deployment, the application will be available at

```
https://your-app-name.streamlit.app
```

---

# ⚠ Disclaimer

This application is intended for educational and informational purposes only.

The generated meal plans, workout routines, calorie estimates, and AI responses should not replace advice from qualified healthcare professionals, registered dietitians, physicians, or certified fitness trainers.

Always consult a healthcare provider before making significant changes to your diet or exercise routine.

---

# 📜 License

This project is licensed under the **MIT License**

---

# 👩‍💻 Author

**Jyotshna Devi Gavireddy**

GitHub - https://github.com/jyotshna068

---

# ⭐ Support

If you found this project useful, please consider giving it a ⭐ on GitHub.

