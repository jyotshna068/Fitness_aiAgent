# AI Health & Fitness Agent

A personalized health and fitness assistant that calculates your core body metrics and uses Google's Gemini AI to generate custom meal plans, workout programs, and answer fitness questions in a live coach chat.

## The project ships in two forms:


app.py — a Streamlit web app (Python backend, recommended)
index.html — a single-file browser version with no build step, calling the Gemini API directly from JavaScript



# Features


Health metrics dashboard — BMI, BMR, TDEE, daily calorie target, and macronutrient breakdown (protein / carbs / fat), computed from age, gender, height, weight, activity level, and goal
Visual BMI gauge — a gradient scale with a positioned marker showing where you fall (Underweight / Normal / Overweight / Obese)
AI-generated meal plans — a full day's meals (breakfast, snacks, lunch, dinner) tailored to your calorie target and dietary preference (vegetarian, vegan, keto, high protein, Mediterranean, or no restriction)
AI-generated workout plans — a weekly training program built around your equipment access, training days per week, and goal (weight loss, maintenance, muscle gain)
Coach chat — an open-ended chat with an AI fitness coach that has your profile as context, plus one-tap quick-prompt buttons for common questions
Downloadable plans — export your meal and workout plans as .txt files


## How the metrics are calculated


BMI — weight (kg) / height (m)²
BMR — Mifflin-St Jeor equation, adjusted for gender
TDEE — BMR × activity multiplier (1.2 to 1.9 depending on activity level)
Calorie target — TDEE adjusted by goal (−500 kcal for weight loss, +300 kcal for muscle gain, unchanged for maintenance)
Macros — protein/carb/fat grams split as a percentage of the calorie target (35/45/20 for muscle gain, 30/40/30 otherwise)
Ideal weight range — back-calculated from a BMI of 18.5–24.9 at your height


All of this logic lives in health_metrics.py and runs locally — no API calls needed for the metrics tab.