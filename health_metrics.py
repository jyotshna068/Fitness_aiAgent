"""health_metrics.py"""
 
 
def calculate_bmi(weight: float, height: float) -> float:
    """
    Calculate Body Mass Index.
 
    Args:
        weight: Weight in kilograms.
        height: Height in centimetres.
 
    Returns:
        BMI rounded to 2 decimal places.
    """
    height_m = height / 100
    return round(weight / (height_m ** 2), 2)
 
 
def bmi_category(bmi: float) -> str:
    """
    Return the WHO BMI category label.
 
    Args:
        bmi: BMI value.
 
    Returns:
        Category string.
    """
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25.0:
        return "Normal Weight"
    elif bmi < 30.0:
        return "Overweight"
    else:
        return "Obese"
 
 
def calculate_bmr(weight: float, height: float, age: int, gender: str) -> int:
    """
    Calculate Basal Metabolic Rate using the Mifflin-St Jeor equation.
 
    Args:
        weight: Weight in kilograms.
        height: Height in centimetres.
        age:    Age in years.
        gender: "Male" or "Female".
 
    Returns:
        BMR in kilocalories per day (rounded to nearest integer).
    """
    base = (10 * weight) + (6.25 * height) - (5 * age)
    return round(base + 5) if gender == "Male" else round(base - 161)
 
 
def calculate_tdee(bmr: int, activity_level: str) -> int:
    """
    Calculate Total Daily Energy Expenditure.
 
    Args:
        bmr:            Basal Metabolic Rate (kcal/day).
        activity_level: One of the five standard activity levels.
 
    Returns:
        TDEE in kilocalories per day (rounded to nearest integer).
    """
    factors = {
        "Sedentary":         1.200,
        "Lightly Active":    1.375,
        "Moderately Active": 1.550,
        "Very Active":       1.725,
        "Extremely Active":  1.900,
    }
    return round(bmr * factors[activity_level])
 
 
def calorie_target(tdee: int, goal: str) -> int:
    """
    Adjust TDEE based on the user's goal.
 
    Args:
        tdee: Total Daily Energy Expenditure.
        goal: "Weight Loss", "Maintenance", or "Muscle Gain".
 
    Returns:
        Daily calorie target as an integer.
    """
    adjustments = {
        "Weight Loss":  -500,
        "Maintenance":     0,
        "Muscle Gain":  +300,
    }
    return tdee + adjustments.get(goal, 0)
 
 
def ideal_weight_range(height: float) -> tuple[float, float]:
    """
    Return the healthy weight range (BMI 18.5-24.9) for a given height.
 
    Args:
        height: Height in centimetres.
 
    Returns:
        Tuple (min_kg, max_kg) rounded to one decimal place.
    """
    h = height / 100
    return round(18.5 * h ** 2, 1), round(24.9 * h ** 2, 1)
 
 
def macro_split(calories: int, goal: str) -> dict[str, int]:
    """
    Calculate macronutrient targets in grams.
 
    Protein: 30% / Carbs: 40% / Fat: 30%  (weight loss & maintenance)
    Protein: 35% / Carbs: 45% / Fat: 20%  (muscle gain)
 
    Args:
        calories: Daily calorie target.
        goal:     "Weight Loss", "Maintenance", or "Muscle Gain".
 
    Returns:
        Dict with keys "protein_g", "carbs_g", "fat_g".
    """
    if goal == "Muscle Gain":
        protein_pct, carbs_pct, fat_pct = 0.35, 0.45, 0.20
    else:
        protein_pct, carbs_pct, fat_pct = 0.30, 0.40, 0.30
 
    return {
        "protein_g": round((calories * protein_pct) / 4),
        "carbs_g":   round((calories * carbs_pct)   / 4),
        "fat_g":     round((calories * fat_pct)      / 9),
    }