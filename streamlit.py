import streamlit as st
import time

# st.set_page_config(page_title="movie recommeder", page_icon='📽')

# page_bg_img = """
# <style>
# [data-testid="stAppViewContainer"]{
# background-image : url(https://wallpapercave.com/wp/wp1945939.jpg);
# background-size : cover;
# }

# [data-testid = "stHeader"] {
# background-color: rgba(0, 0, 0, 0);
# }

# #root > div:nth-child(1) > div.withScreencast > div > div > div > section > div.block-container.css-1y4p8pa.e1g8pov64 > div:nth-child(1) > div > div.css-12ttj6m.en8akda1 > div:nth-child(1) > div > div:nth-child(4) > div > div > button
# {
#     background-color: darkred;
#     width : 670px;
#     color: white;
# }

# [data-testid = "stVerticalBlock"]
# {
#     background-color: white;
#     border-color: red;
#     border-width: 100px;
# }
# </style>
# """

# st.markdown(page_bg_img, unsafe_allow_html=True)
# with open("style.css") as source_des:
#     st.markdown(f"<style>{source_des.read()}</style>", unsafe_allow_html=True)
# st.markdown("<h1 style ='text-align: center;'>Movie Recommender</h1>", unsafe_allow_html=True)


# with st.form('my_form'):
#     first = st.text_input("First movie")
#     second = st.text_input("Second movie")
#     third = st.text_input("Third movie")

#     result = st.form_submit_button('Recommend Similar Movies')
#     prog_bar = st.progress(0)
#     for perc in range(100):
#         time.sleep(0.005)
#         prog_bar.progress(perc+1)

#     if result:
#         if first == "" or second == "" or third == "":
#             st.warning("please fill above fields")
#         else:
#             print('meow')
#     pass

# st.markdown('</div>', unsafe_allow_html=True)
st.markdown("hi")