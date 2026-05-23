import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os
import stripe

load_dotenv()
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

PRICE_ID = os.getenv("STRIPE_PRICE_ID")

# -------------------------------
# CONFIG
# -------------------------------
client = OpenAI()

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
PRICE_ID = os.getenv("STRIPE_PRICE_ID")

st.set_page_config(page_title="Duggy Sports AI", layout="wide")

# -------------------------------
# SIMPLE "USER SYSTEM"
# -------------------------------
if "usage" not in st.session_state:
    st.session_state.usage = 0

if "is_pro" not in st.session_state:
    st.session_state.is_pro = False

FREE_LIMIT = 3

# -------------------------------
# SIDEBAR
# -------------------------------
st.sidebar.title("⚾ Duggy AI")

st.sidebar.write("Plan:", "PRO" if st.session_state.is_pro else "FREE")
st.sidebar.write(f"Usage: {st.session_state.usage}/{FREE_LIMIT}")

page = st.sidebar.radio("Menu", ["Generate", "Upgrade"])

# -------------------------------
# GENERATE PAGE
# -------------------------------
if page == "Generate":

    st.title("⚡ Generate Viral Sports Content")

    if not st.session_state.is_pro and st.session_state.usage >= FREE_LIMIT:
        st.error("Free limit reached. Upgrade to continue.")
        st.stop()

    play = st.text_area("Describe the sports moment")
    style = st.selectbox("Style", ["Hype ESPN", "Funny Parent", "Recruiting", "TikTok Viral"])

    if st.button("Generate 🚀"):

        if not play.strip():
            st.warning("Enter a moment")
            st.stop()

        with st.spinner("Generating..."):

            response = client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[{
                    "role": "user",
                    "content": f"""
Style: {style}

Create:
5 captions
5 titles
10 hashtags

Moment:
{play}
"""
                }]
            )

            output = response.choices[0].message.content

        st.session_state.usage += 1

        st.subheader("🔥 Results")
        st.text(output)

# -------------------------------
# UPGRADE PAGE (STRIPE)
# -------------------------------
elif page == "Upgrade":

    st.title("Upgrade to Pro 💳")
   

    st.markdown("""
    ### 🚀 Pro includes:
    - Unlimited generations
    - Faster AI responses
    - Viral templates unlocked
    """)

    checkout = stripe.checkout.Session.create(
        mode="subscription",
        line_items=[{
            "price": PRICE_ID,
            "quantity": 1
        }],
        success_url="http://localhost:8501",
        cancel_url="http://localhost:8501"
    )

    st.link_button("💳 Upgrade Instantly", checkout.url)