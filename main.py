import streamlit as st

st.set_page_config(
    page_icon="📔",
    page_title="StoryGen",
    initial_sidebar_state="expanded"
)

hide_st_style ='''
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
'''
st.markdown(hide_st_style, unsafe_allow_html=True)

st.title("📔StoryGen")

with st.sidebar:
    
    idea=st.text_area("If you have any ideas, type in here...")
    
    story_type=st.selectbox("Story Type",["Bedtime Story","Moral Story","Fairytale","Adventure","Educational","Mystery",'Science Fiction'])
    age=st.selectbox("Reader's Age",["2-4 years","5-7 years","8-10 years","10-12 years","12-14 years"])
    length=st.select_slider("Story Length",["Short (~400 words)","Medium (~600 words)","Long (~800 words)"])
    
    start=st.button("Generate Story!")