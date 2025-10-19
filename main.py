import streamlit as st
import pandas as pd

# --------------------------------------------
# GPA & CGPA CALCULATOR STREAMLIT APP
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
    
    # Store the current semester GPA and credits in session state
    st.session_state.current_gpa = gpa
    st.session_state.current_credits = total_credits

# CGPA Calculation
st.markdown("---")
st.header("📊 CGPA Calculator")

st.write("""
**Two methods to calculate CGPA:**

1. **Comprehensive Method** (Recommended): Enter details of all previous semesters
2. **Simple Method**: If you already know your previous CGPA and total credits
""")

method = st.radio("Select calculation method:", 
                 ["Comprehensive Method", "Simple Method"])

if method == "Comprehensive Method":
    st.subheader("Comprehensive CGPA Calculation")
    
    num_previous_semesters = st.number_input("Number of previous semesters:", 
                                           min_value=1, step=1, key="num_semesters")
    
    previous_semesters = []
    
    for i in range(int(num_previous_semesters)):
        st.write(f"**Semester {i+1}**")
        col1, col2 = st.columns(2)
        with col1:
            semester_gpa = st.number_input(f"GPA for Semester {i+1}:", 
                                         min_value=0.0, max_value=4.0, step=0.01, 
                                         key=f"gpa_{i}")
        with col2:
            semester_credits = st.number_input(f"Credit Hours for Semester {i+1}:", 
                                             min_value=0.0, step=0.5, 
                                             key=f"credits_{i}")
        previous_semesters.append({"GPA": semester_gpa, "Credits": semester_credits})
    
    if st.button("Calculate Comprehensive CGPA"):
        # Calculate total weighted points and total credits from previous semesters
        total_prev_weighted = 0
        total_prev_credits = 0
        
        for semester in previous_semesters:
            total_prev_weighted += semester["GPA"] * semester["Credits"]
            total_prev_credits += semester["Credits"]
        
        # Add current semester if available
        if 'current_gpa' in st.session_state and 'current_credits' in st.session_state:
            current_gpa = st.session_state.current_gpa
            current_credits = st.session_state.current_credits
            
            total_weighted = total_prev_weighted + (current_gpa * current_credits)
            total_credits_cgpa = total_prev_credits + current_credits
            
            cgpa = total_weighted / total_credits_cgpa
            
            st.success(f"🏅 Your Updated CGPA is: **{cgpa:.2f}**")
            st.info(f"Total Credits Completed: {total_credits_cgpa}")
        else:
            # Calculate CGPA for previous semesters only
            if total_prev_credits > 0:
                cgpa = total_prev_weighted / total_prev_credits
                st.success(f"🏅 Your CGPA (previous semesters only) is: **{cgpa:.2f}**")
                st.info(f"Total Credits Completed: {total_prev_credits}")
            else:
                st.error("Please enter valid credit hours.")

else:  # Simple Method
    st.subheader("Simple CGPA Calculation")
    
    prev_cgpa = st.number_input("Previous CGPA:", min_value=0.0, max_value=4.0, step=0.01)
    prev_credits = st.number_input("Total Credit Hours Completed Before This Semester:", min_value=0.0, step=0.5)
    
    # Use current semester data if available, otherwise allow manual input
    if 'current_gpa' in st.session_state and 'current_credits' in st.session_state:
        current_gpa = st.session_state.current_gpa
        current_credits = st.session_state.current_credits
        st.info(f"Current Semester GPA: {current_gpa:.2f}, Credits: {current_credits}")
    else:
        current_gpa = st.number_input("This Semester's GPA:", min_value=0.0, max_value=4.0, step=0.01)
        current_credits = st.number_input("Credit Hours This Semester:", min_value=0.0, step=0.5)

    if st.button("Calculate Simple CGPA"):
        try:
            new_cgpa = ((prev_cgpa * prev_credits) + (current_gpa * current_credits)) / (prev_credits + current_credits)
            st.success(f"🏅 Your Updated CGPA is: **{new_cgpa:.2f}**")
            st.info(f"Total Credits Completed: {prev_credits + current_credits}")
        except ZeroDivisionError:
            st.error("Please ensure total credit hours are greater than 0.")

st.markdown("---")
st.caption("Developed by Syeda Rafia Gilani 💻 | Streamlit GPA & CGPA Calculator")
