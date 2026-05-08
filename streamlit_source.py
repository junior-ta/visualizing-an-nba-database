import streamlit as st

pages= {
    "Homepage":[st.Page("deployment/Main_page.py", title="Main Page")],

    "Me":[st.Page("deployment/Project's_stack.py", title="Project's stack"),
          st.Page("deployment/Links/links.py", title="Links and I")],

      "Recent":[st.Page("deployment/page_10_prompt.py", title="Evolution of Team's Offense in the past 5 years")],
                        
    "Data extraction and visualization":[st.Page("deployment/page_1_prompt.py", title="top K leaders bar chart"),
                                         st.Page("deployment/page_2_prompt.py", title="stats of the 5 NBA leaders for X category"),
                                         st.Page("deployment/page_3_prompt.py", title="prompt 3"),
                                         st.Page("deployment/page_4_prompt.py", title="prompt 4"),
                                         st.Page("deployment/page_5_prompt.py", title="prompt 5"),
                                         st.Page("deployment/page_6_prompt.py", title="prompt 6"),
                                         st.Page("deployment/page_7_prompt.py", title="prompt 7")],
    "Analytics":[st.Page("deployment/page_8_pythagoreanExpectation.py", title="Pythagorean Expectation"),
                 st.Page("deployment/page_9_pythagoreanPrediction.py", title="Pythagorean Prediction")]
}



# Set up navigation
pg = st.navigation(pages, position="hidden")

# Run the selected page
pg.run()