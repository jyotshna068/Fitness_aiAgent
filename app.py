"""app.py — AI Health & Fitness Agent (Streamlit + Gemini)"""
 
import os
 
import google.generativeai as genai
import streamlit as st
from dotenv import load_dotenv
 
from health_metrics import (
    calculate_bmi,
    bmi_category,
    calculate_bmr,
    calculate_tdee,
    calorie_target,
    ideal_weight_range,
    macro_split,
)
 
# ── Load .env ─────────────────────────────────────────────────────────────────
load_dotenv()
 
# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Health & Fitness Agent",
    page_icon="💪",
    layout="wide",
    initial_sidebar_state="expanded",
)
 
# ── Custom CSS (full theme — cards, gauges, macro bar, chat bubbles) ──────────
st.markdown(
    """
    <style>
    :root {
        --bg:        #ffffff;
        --bg2:       #f8fafc;
        --bg3:       #f1f5f9;
        --border:    #e2e8f0;
        --border2:   #cbd5e1;
        --text:      #0f172a;
        --text2:     #475569;
        --text3:     #94a3b8;
        --accent:    #0f172a;
        --radius:    14px;
        --radius-sm: 10px;
    }
 
    /* Hide default streamlit chrome we don't want */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
 
    .block-container { padding-top: 2rem; padding-bottom: 3rem; max-width: 1100px; }
 
    /* ── Header ── */
    .app-title { font-size: 2rem; font-weight: 800; margin-bottom: .1rem; color: var(--text); }
    .app-sub   { font-size: .95rem; color: var(--text2); margin-bottom: 1.25rem; }
 
    /* ── Metric cards ── */
    .metric-card {
        background: var(--bg2); border: 1px solid var(--border); border-radius: var(--radius);
        padding: 1.1rem 1rem; text-align: center; height: 100%;
    }
    .metric-label {
        font-size: .7rem; text-transform: uppercase; letter-spacing: .08em;
        color: var(--text3); margin-bottom: .35rem; font-weight: 600;
    }
    .metric-value { font-size: 1.65rem; font-weight: 800; color: var(--text); line-height: 1.1; }
    .metric-sub   { font-size: .72rem; color: var(--text3); margin-top: .3rem; }
 
    /* ── Section card wrapper ── */
    .section-card {
        background: var(--bg); border: 1px solid var(--border); border-radius: var(--radius);
        padding: 1.4rem 1.5rem; margin-bottom: 1.25rem;
    }
    .section-title { font-size: 1.05rem; font-weight: 700; margin-bottom: .9rem; color: var(--text); }
 
    /* ── BMI gauge ── */
    .bmi-bar-wrap {
        position: relative; height: 16px; border-radius: 8px; margin: 10px 0 8px;
        background: linear-gradient(90deg, #60a5fa 0%, #4ade80 26%, #fbbf24 60%, #f87171 100%);
    }
    .bmi-marker {
        position: absolute; top: -5px; width: 24px; height: 24px; border-radius: 50%;
        background: var(--text); border: 3px solid #fff;
        transform: translateX(-50%); box-shadow: 0 0 0 2px var(--text), 0 2px 6px rgba(0,0,0,.25);
    }
    .bmi-scale-labels {
        display: flex; justify-content: space-between; font-size: .72rem;
        color: var(--text3); margin-top: 2px;
    }
 
    /* ── Macro bar ── */
    .macro-bar {
        height: 14px; border-radius: 7px; display: flex; overflow: hidden;
        margin: 10px 0; box-shadow: inset 0 0 0 1px var(--border);
    }
    .macro-bar span { display: block; height: 100%; }
    .macro-legend { display: flex; gap: 1.25rem; font-size: .82rem; color: var(--text2); margin-bottom: 1rem; }
    .macro-legend .dot { display: inline-block; width: 10px; height: 10px; border-radius: 50%; margin-right: 5px; }
 
    .macro-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; text-align: center; }
    .macro-stat-label { font-size: .7rem; color: var(--text3); margin-bottom: 3px; text-transform: uppercase; letter-spacing: .06em; }
    .macro-stat-value { font-size: 1.3rem; font-weight: 800; color: var(--text); }
    .macro-stat-unit  { font-size: .7rem; color: var(--text3); }
 
    /* ── Info banner ── */
    .info-banner {
        background: #eff6ff; border: 1px solid #bfdbfe; color: #1e40af;
        border-radius: var(--radius-sm); padding: .85rem 1.1rem; font-size: .88rem; margin-top: 1rem;
    }
 
    /* ── Plan output box ── */
    .plan-output {
        background: var(--bg2); border: 1px solid var(--border); border-radius: var(--radius-sm);
        padding: 1.1rem; font-size: .9rem; line-height: 1.7; white-space: pre-wrap; color: var(--text);
    }
 
    /* ── Chat bubbles ── */
    .chat-msg-row { display: flex; margin-bottom: 10px; }
    .chat-msg-row.user { justify-content: flex-end; }
    .chat-bubble {
        padding: 10px 15px; border-radius: 18px; font-size: .9rem; line-height: 1.55;
        max-width: 78%; white-space: pre-wrap;
    }
    .chat-bubble.user {
        background: var(--accent); color: #fff; border-radius: 18px 18px 4px 18px;
    }
    .chat-bubble.bot {
        background: var(--bg2); color: var(--text); border: 1px solid var(--border);
        border-radius: 18px 18px 18px 4px;
    }
 
    /* Buttons */
    div.stButton > button {
        border-radius: var(--radius-sm); font-weight: 600; border: 1px solid var(--border2);
    }
    div.stButton > button[kind="primary"] { background: var(--accent); border-color: var(--accent); }
    </style>
    """,
    unsafe_allow_html=True,
)
 
# ── Gemini setup ──────────────────────────────────────────────────────────────
@st.cache_resource
def get_model() -> genai.GenerativeModel:
    api_key = os.getenv("GOOGLE_API_KEY") or st.secrets.get("GOOGLE_API_KEY", "")
    if not api_key:
        st.error("⚠️  GOOGLE_API_KEY not found. Add it to your .env file or Streamlit secrets.")
        st.stop()
    genai.configure(api_key=api_key)
    return genai.GenerativeModel("gemini-2.5-flash")
 
 
model = get_model()
 
# ── Session state ─────────────────────────────────────────────────────────────
if "chat_session" not in st.session_state:
    st.session_state.chat_session = None   # gemini ChatSession object
if "chat_display" not in st.session_state:
    st.session_state.chat_display = []     # list of {role, content} for display
if "meal_plan" not in st.session_state:
    st.session_state.meal_plan = ""
if "workout_plan" not in st.session_state:
    st.session_state.workout_plan = ""
 
# ── Sidebar — user profile ────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 👤 Your Profile")
 
    age    = st.number_input("Age",         min_value=10,  max_value=100, value=25, step=1)
    gender = st.selectbox("Gender",         ["Male", "Female"])
    height = st.number_input("Height (cm)", min_value=100, max_value=250, value=170, step=1)
    weight = st.number_input("Weight (kg)", min_value=20,  max_value=300, value=70,  step=1)
 
    activity = st.selectbox(
        "Activity level",
        ["Sedentary", "Lightly Active", "Moderately Active", "Very Active", "Extremely Active"],
        index=2,
    )
    goal = st.selectbox("Goal", ["Weight Loss", "Maintenance", "Muscle Gain"], index=0)
 
    st.divider()
    diet_pref = st.selectbox(
        "Dietary preference",
        ["No restriction", "Vegetarian", "Vegan", "Keto", "High protein", "Mediterranean"],
    )
    equipment = st.selectbox(
        "Workout equipment",
        ["Full gym", "Home (dumbbells)", "Bodyweight only"],
    )
    days_pw = st.selectbox(
        "Training days / week",
        ["3 days", "4 days", "5 days", "6 days"],
        index=2,
    )
 
# ── Compute metrics ───────────────────────────────────────────────────────────
bmi     = calculate_bmi(weight, height)
cat     = bmi_category(bmi)
bmr     = calculate_bmr(weight, height, age, gender)
tdee    = calculate_tdee(bmr, activity)
cal_tgt = calorie_target(tdee, goal)
macros  = macro_split(cal_tgt, goal)
wt_min, wt_max = ideal_weight_range(height)
 
profile_text = (
    f"Age: {age}, Gender: {gender}, Height: {height} cm, Weight: {weight} kg, "
    f"BMI: {bmi} ({cat}), Activity: {activity}, Goal: {goal}, "
    f"Daily calorie target: {cal_tgt} kcal, "
    f"Macros — Protein: {macros['protein_g']} g, "
    f"Carbs: {macros['carbs_g']} g, Fat: {macros['fat_g']} g"
)
 
# ── Page header ───────────────────────────────────────────────────────────────
st.markdown('<div class="app-title">💪 AI Health & Fitness Agent</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="app-sub">Personalised metrics, meal plans, workouts & coach chat — powered by Gemini.</div>',
    unsafe_allow_html=True,
)
 
# ── Tabs ──────────────────────────────────────────────────────────────────────
tab_metrics, tab_meal, tab_workout, tab_chat = st.tabs(
    ["📊 Metrics", "🍽 Meal Plan", "🏋 Workout Plan", "💬 Coach Chat"]
)
 
# ════════════════════════════════════════════════════════════════════════════════
# TAB 1 — METRICS
# ════════════════════════════════════════════════════════════════════════════════
with tab_metrics:
    c1, c2, c3, c4 = st.columns(4)
    for col, label, value, sub in [
        (c1, "BMI",            bmi,               cat),
        (c2, "BMR",            f"{bmr:,}",        "kcal / day"),
        (c3, "TDEE",           f"{tdee:,}",       "kcal / day"),
        (c4, "Calorie target", f"{cal_tgt:,}",    goal.lower()),
    ]:
        with col:
            st.markdown(
                f"""<div class="metric-card">
                        <div class="metric-label">{label}</div>
                        <div class="metric-value">{value}</div>
                        <div class="metric-sub">{sub}</div>
                    </div>""",
                unsafe_allow_html=True,
            )
 
    st.write("")  # spacer
 
    # ── BMI gauge card ──
    pct = min(max((bmi - 10) / 30 * 100, 2), 97)
    st.markdown(
        f"""<div class="section-card">
                <div class="section-title">BMI Scale</div>
                <div class="bmi-bar-wrap">
                    <div class="bmi-marker" style="left:{pct}%"></div>
                </div>
                <div class="bmi-scale-labels">
                    <span>Underweight &lt;18.5</span>
                    <span>Normal 18.5–24.9</span>
                    <span>Overweight 25–29.9</span>
                    <span>Obese ≥30</span>
                </div>
            </div>""",
        unsafe_allow_html=True,
    )
 
    # ── Macro card ──
    total = macros["protein_g"] * 4 + macros["carbs_g"] * 4 + macros["fat_g"] * 9
    p_pct = round(macros["protein_g"] * 4 / total * 100) if total else 0
    c_pct = round(macros["carbs_g"]   * 4 / total * 100) if total else 0
    f_pct = max(100 - p_pct - c_pct, 0)
 
    st.markdown(
        f"""<div class="section-card">
                <div class="section-title">Daily Macronutrient Targets</div>
                <div class="macro-bar">
                    <span style="width:{p_pct}%;background:#60a5fa"></span>
                    <span style="width:{c_pct}%;background:#fbbf24"></span>
                    <span style="width:{f_pct}%;background:#f87171"></span>
                </div>
                <div class="macro-legend">
                    <span><span class="dot" style="background:#60a5fa"></span>Protein</span>
                    <span><span class="dot" style="background:#fbbf24"></span>Carbs</span>
                    <span><span class="dot" style="background:#f87171"></span>Fat</span>
                </div>
                <div class="macro-grid">
                    <div>
                        <div class="macro-stat-label">Protein</div>
                        <div class="macro-stat-value">{macros['protein_g']}</div>
                        <div class="macro-stat-unit">grams</div>
                    </div>
                    <div>
                        <div class="macro-stat-label">Carbs</div>
                        <div class="macro-stat-value">{macros['carbs_g']}</div>
                        <div class="macro-stat-unit">grams</div>
                    </div>
                    <div>
                        <div class="macro-stat-label">Fat</div>
                        <div class="macro-stat-value">{macros['fat_g']}</div>
                        <div class="macro-stat-unit">grams</div>
                    </div>
                </div>
                <div class="info-banner">
                    🎯&nbsp; Healthy weight range for {height} cm: <strong>{wt_min}–{wt_max} kg</strong> (BMI 18.5–24.9)
                </div>
            </div>""",
        unsafe_allow_html=True,
    )
 
# ════════════════════════════════════════════════════════════════════════════════
# TAB 2 — MEAL PLAN
# ════════════════════════════════════════════════════════════════════════════════
with tab_meal:
    st.markdown(
        f"""<div class="section-card">
                <div class="section-title">Generate your meal plan</div>
                <p style="color:var(--text2);font-size:.9rem;margin-bottom:1rem">
                    A <strong>{diet_pref.lower()}</strong> daily meal plan targeting
                    <strong>{cal_tgt:,} kcal</strong> for <strong>{goal.lower()}</strong>.
                </p>
            </div>""",
        unsafe_allow_html=True,
    )
 
    if st.button("✨ Generate meal plan", type="primary"):
        prompt = (
            f"You are a registered dietitian. Create a detailed daily meal plan.\n"
            f"User profile: {profile_text}\n"
            f"Dietary preference: {diet_pref}\n\n"
            f"Structure: Breakfast · Morning snack · Lunch · Afternoon snack · Dinner.\n"
            f"For each meal include: name, key ingredients, portion size, and calorie estimate.\n"
            f"Keep the total close to {cal_tgt} kcal.\n"
            f"End with a short macro summary (protein / carbs / fat in grams).\n"
            f"Use plain text only — no markdown tables."
        )
        with st.spinner("Creating your meal plan…"):
            response = model.generate_content(prompt)
            st.session_state.meal_plan = response.text
 
    if st.session_state.meal_plan:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Your meal plan</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="plan-output">{st.session_state.meal_plan}</div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        st.download_button(
            "⬇️  Download meal plan",
            st.session_state.meal_plan,
            file_name="meal_plan.txt",
            mime="text/plain",
        )
 
# ════════════════════════════════════════════════════════════════════════════════
# TAB 3 — WORKOUT PLAN
# ════════════════════════════════════════════════════════════════════════════════
with tab_workout:
    st.markdown(
        f"""<div class="section-card">
                <div class="section-title">Generate your workout plan</div>
                <p style="color:var(--text2);font-size:.9rem;margin-bottom:1rem">
                    A <strong>{days_pw}</strong> weekly program using
                    <strong>{equipment.lower()}</strong> for <strong>{goal.lower()}</strong>.
                </p>
            </div>""",
        unsafe_allow_html=True,
    )
 
    if st.button("✨ Generate workout plan", type="primary"):
        prompt = (
            f"You are a certified personal trainer. Create a weekly workout plan.\n"
            f"User profile: {profile_text}\n"
            f"Equipment: {equipment}, Days per week: {days_pw}\n\n"
            f"Include: warm-up routine, day-by-day sessions with exercises "
            f"(sets × reps or duration), rest days, and a cooldown routine.\n"
            f"Tailor intensity and exercise selection to the user's goal ({goal}).\n"
            f"Use plain text only — no markdown tables."
        )
        with st.spinner("Building your workout program…"):
            response = model.generate_content(prompt)
            st.session_state.workout_plan = response.text
 
    if st.session_state.workout_plan:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Your workout plan</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="plan-output">{st.session_state.workout_plan}</div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        st.download_button(
            "⬇️  Download workout plan",
            st.session_state.workout_plan,
            file_name="workout_plan.txt",
            mime="text/plain",
        )
 
# ════════════════════════════════════════════════════════════════════════════════
# TAB 4 — COACH CHAT
# ════════════════════════════════════════════════════════════════════════════════
with tab_chat:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Quick questions</div>', unsafe_allow_html=True)
 
    QUICK_PROMPTS = [
        "What foods support muscle recovery?",
        "How much water should I drink daily?",
        "Should I do cardio before or after lifting?",
        "Best exercises to burn fat at home?",
        "How many rest days do I need?",
        "How can I improve my sleep for better gains?",
    ]
    cols = st.columns(3)
    pending_prompt = None
    for i, col in enumerate(cols):
        if col.button(QUICK_PROMPTS[i], key=f"qp{i}", use_container_width=True):
            pending_prompt = QUICK_PROMPTS[i]
    for i, col in enumerate(cols):
        if col.button(QUICK_PROMPTS[i + 3], key=f"qp{i+3}", use_container_width=True):
            pending_prompt = QUICK_PROMPTS[i + 3]
 
    st.markdown("</div>", unsafe_allow_html=True)
 
    # ── Chat history render ──
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    if st.session_state.chat_display:
        for msg in st.session_state.chat_display:
            role_class = "user" if msg["role"] == "user" else "bot"
            avatar = "🧑" if msg["role"] == "user" else "💪"
            st.markdown(
                f"""<div class="chat-msg-row {role_class}">
                        <div class="chat-bubble {role_class}">{msg['content']}</div>
                    </div>""",
                unsafe_allow_html=True,
            )
    else:
        st.caption("Ask your fitness coach a question, or tap one of the quick prompts above.")
 
    user_input = st.chat_input("Ask your fitness coach…")
    st.markdown("</div>", unsafe_allow_html=True)
 
    final_input = pending_prompt or user_input
 
    if final_input:
        if st.session_state.chat_session is None:
            system_context = (
                f"You are a knowledgeable, friendly health and fitness coach. "
                f"Give practical, evidence-based advice. Keep responses concise and actionable.\n"
                f"The user's profile is: {profile_text}"
            )
            st.session_state.chat_session = model.start_chat(history=[
                {"role": "user",  "parts": [system_context]},
                {"role": "model", "parts": ["Understood! I have your profile. How can I help?"]},
            ])
 
        st.session_state.chat_display.append({"role": "user", "content": final_input})
 
        with st.spinner("Thinking…"):
            response = st.session_state.chat_session.send_message(final_input)
            reply = response.text
 
        st.session_state.chat_display.append({"role": "assistant", "content": reply})
        st.rerun()
 
    if st.session_state.chat_display:
        if st.button("🗑 Clear chat history"):
            st.session_state.chat_display = []
            st.session_state.chat_session = None
            st.rerun()
 