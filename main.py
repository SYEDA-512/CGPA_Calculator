import streamlit as st
import pandas as pd

# --------------------------------------------
# GPA CALCULATOR STREAMLIT APP
# --------------------------------------------

st.set_page_config(page_title="GPA & CGPA Calculator", page_icon="🎓", layout="centered")

st.title("🎓 GPA & CGPA Calculator")

st.write("Enter your course grades and credit hours to calculate your GPA and CGPA easily.")

# Grade to grade-point mapping (you can customize)
grade_points = {
    "A+": 4.0,
    "A": 4.0,
    "A-": 3.7,
    "B+": 3.3,
    "B": 3.0,
    "B-": 2.7,
    "C+": 2.3,
    "C": 2.0,
    "C-": 1.7,
    "D": 1.0,
    "F": 0.0
}

# Input: number of courses
num_courses = st.number_input("Enter number of courses this semester:", min_value=1, step=1)

course_data = []
for i in range(int(num_courses)):
    st.subheader(f"Course {i+1}")
    course_name = st.text_input(f"Course {i+1} Name:", key=f"name_{i}")
    grade = st.selectbox(f"Select Grade for {course_name or 'Course '+str(i+1)}", list(grade_points.keys()), key=f"grade_{i}")
    credit = st.number_input(f"Credit Hours for {course_name or 'Course '+str(i+1)}:", min_value=1.0, step=0.5, key=f"credit_{i}")
    course_data.append({"Course": course_name, "Grade": grade, "Credit Hours": credit})

# Calculate GPA
if st.button("Calculate GPA"):
    df = pd.DataFrame(course_data)
    df["Grade Point"] = df["Grade"].map(grade_points)
    df["Weighted Points"] = df["Grade Point"] * df["Credit Hours"]

    total_credits = df["Credit Hours"].sum()
    total_weighted_points = df["Weighted Points"].sum()
    gpa = total_weighted_points / total_credits

    st.success(f"🎯 Your GPA for this semester is: **{gpa:.2f}**")
    st.dataframe(df)

# CGPA Calculation
st.markdown("---")
st.header("📊 CGPA Calculator")

st.write("Enter your previous CGPA and total completed credit hours to calculate your new CGPA.")

prev_cgpa = st.number_input("Previous CGPA:", min_value=0.0, max_value=4.0, step=0.01)
prev_credits = st.number_input("Total Credit Hours Completed Before This Semester:", min_value=0.0, step=0.5)
new_credits = st.number_input("Credit Hours Taken This Semester:", min_value=0.0, step=0.5)
current_gpa = st.number_input("This Semester’s GPA:", min_value=0.0, max_value=4.0, step=0.01)

if st.button("Calculate CGPA"):
    try:
        new_cgpa = ((prev_cgpa * prev_credits) + (current_gpa * new_credits)) / (prev_credits + new_credits)
        st.success(f"🏅 Your Updated CGPA is: **{new_cgpa:.2f}**")
    except ZeroDivisionError:
        st.error("Please ensure total credit hours are greater than 0.")

st.markdown("---")
st.caption("Developed by Syeda Rafia Gilani 💻 | Streamlit GPA & CGPA Calculator")
