import streamlit as st

# Set a larger font size for better visibility
st.markdown('<style>h1, h2, h3 {font-size: 2em;}</style>', unsafe_allow_html=True)

st.title('DWM MINI PROJECT')

team_members = [
    {'name': 'Rushikesh Gadewar', 'sapid': '60003210171'},
    {'name': 'Shashank Das', 'sapid': '60003210196'},
    {'name': 'Merul Shah', 'sapid': '60003210185'}
]

professor = 'Professor Harshal Dalvi'
year = 'Third Year'
branch = 'Bachelor of Tech Information Technology'
batch = 'IT 2 batch 1'
subject = 'DWM LAB'

st.header('Team members:')
st.table(data=[{'Name': member['name'], 'SAPID': member['sapid']} for member in team_members])

st.header('Details:')
st.write(f"Professor: {professor}")
st.write(f"{year} {branch}")
st.write(f"Batch: {batch}")
st.write(f"Subject: {subject}")
