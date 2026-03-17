import streamlit as st
import datetime
import json
import openai

client = openai.api_key = st.secrets["OPENAI_API_KEY"]

st.set_page_config(page_title="IntellimaKG v3", page_icon="🚀")

# ---------------- HEADER ----------------

st.markdown("""
<div style='text-align:center'>
<h1>IntellimaKG v3</h1>
<p><i>AI Digital Marketing Assistant for E-commerce</i></p>
</div>
""", unsafe_allow_html=True)

# ---------------- LOGIN ----------------

trial_days = 7
admin_code = "test123"
codes = [f"demo{i}" for i in range(1,51)]

if "users" not in st.session_state:
    st.session_state.users = {}
code = st.text_input("Enter demo code")

if not code:
    st.stop()
today = datetime.date.today()

if code != admin_code and code not in codes:
    st.error("Invalid code")
    st.stop()

if code != admin_code:
    if code not in st.session_state.users:
        st.session_state.users[code] = str(today)
    start = datetime.datetime.strptime(

        st.session_state.users[code], "%Y-%m-%d"
    ).date()
    
    used = (today - start).days
    remaining = trial_days - used

    if remaining <= 0:
        st.error("Trial expired")
        st.stop()

    st.info(f"Trial days remaining: {remaining}")

else:
    st.success("Admin access")
# ---------------- INPUT ----------------

st.header("Generate Digital Marketing Content")

language = st.selectbox(
    "Language",
    ["Greek","English"]
)

product = st.text_input("Product name")
details = st.text_area("Product details")
image = st.file_uploader("Upload product image (optional)")
# ---------------- GENERATE ----------------

if st.button("Generate Marketing Content"):
    prompt = f"""
Create complete digital marketing content.

Language: {language}

Product: {product}
Details: {details}

Generate:

1 Product Description
2 SEO Title
3 Meta Description
4 SEO Keywords
5 Instagram / Facebook Post
6 Facebook Ad Text
7 Google Ad Text
"""



    if image:



        response = client.responses.create(

            model="gpt-4.1-mini",

            input=[{

                "role":"user",

                "content":[

                    {"type":"input_text","text":prompt},

                    {"type":"input_image","image_url":image}

                ]

            }]

        )



        result = response.output[0].content[0].text



    else:



        response = openai.chatcompletions.create(

            model="gpt-4o-mini",

            messages=[{"role":"user","content":prompt}]

        )



        result = response["choices"[0]["message"["content"]



    st.subheader("Generated Marketing Content")



    st.write(result)



# ---------------- ADMIN PANEL ----------------



if code == admin_code:



    st.sidebar.title("Admin Panel")



    st.sidebar.write("Active users:")



    for user,date in st.session_state.users.items():

        st.sidebar.write(user,"| First login:",date)