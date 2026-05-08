import streamlit as st


#Heading
st.title('My NBA Data Analysis Studies')

st.markdown("""
This app is used to show the results of my data analysis findings, my data explorer/visualizations and many more
* **Contact me:** juniorta@buffalo.edu / ttjrbiz@gmail.com
* **Data source:** Kaggle datasets: https://www.kaggle.com/datasets/szymonjwiak/nba-2022-2023-advanced-boxscores

    Basketball reference: https://www.basketball-reference.com/
""")

#Spacing
for i in range(3):
    st.markdown("")


#.........................body..............................................

#ME
st.subheader('Me!!!', divider="gray")
col1, col2 = st.columns(2)

with col1:
    st.page_link("deployment/Links/links.py", label="About Me and Contacts", icon=":material/contacts:")

with col2:
    st.page_link("deployment/Project's_stack.py", label="Project's stack", icon=":material/layers:")


#Recent
st.subheader('Recent!!!', divider="gray")
p10, p11= st.columns(2)

with p10:
    st.page_link("deployment/page_10_prompt.py", label="Evolution of Team's Offense in the past 5 years")



#OLD Data prompts
st.subheader('Old stuff', divider="grey")
p1, p2, p3 = st.columns(3)
p4, p5, p6 = st.columns(3)

with p1:
    st.page_link("deployment/page_1_prompt.py", label="Top K leaders bar chart")

with p2:
    st.page_link("deployment/page_2_prompt.py", label="Leader's stats")

with p3:
    st.page_link("deployment/page_3_prompt.py", label="Top teams")

with p4:
    st.page_link("deployment/page_4_prompt.py", label="Team's offense")

with p5:
    st.page_link("deployment/page_5_prompt.py", label="Individual performances")

with p6:
    st.page_link("deployment/page_6_prompt.py", label="Pace")


st.page_link("deployment/page_7_prompt.py", label="Player's matchups")


#Analytics
st.subheader('Analytics', divider="gray")
PE, PP = st.columns(2)

with PE:
    st.page_link("deployment/page_8_pythagoreanExpectation.py", label="Pythagorean Expectation")

with PP:
    st.page_link("deployment/page_9_pythagoreanPrediction.py", label="Pythagorean Prediction")