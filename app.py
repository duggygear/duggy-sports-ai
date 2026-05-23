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
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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
    

    st.title("⚾ Duggy Sports AI")

    st.markdown("### Turn sports moments into viral TikTok content in seconds")
    st.caption("Used by athletes, parents, and content creators")

    st.divider()

    if not st.session_state.is_pro and st.session_state.usage >= FREE_LIMIT:
        st.error("Free limit reached. Upgrade to continue.")
        st.stop()

    play_description = st.text_area(
        "",
        placeholder="Example: Walk-off double in championship game, crowd goes wild...",
        height=120
    )

    style = st.selectbox(
        "Choose content style",
    [
            "🔥 Hype ESPN",
            "😂 Funny Parent Voice",
            "🎯 Recruiting Highlight",
            "📱 TikTok Viral"
    ]
    )

    if st.button("🚀 Generate Viral Content", type="primary"):

        if not play_description.strip():
            st.warning("Enter a moment")
            st.stop()

        with st.spinner("Generating viral content..."):

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
{play_description}
"""
                }]
            )

            output = response.choices[0].message.content

        st.session_state.usage += 1

        st.divider()

        st.markdown("## 🔥 Your Viral Content")

        with st.container(border=True):
            st.markdown(output)

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

    if st.button("💳 Upgrade to Pro"):

        checkout = stripe.checkout.Session.create(
            mode="subscription",
            line_items=[{
                "price": PRICE_ID,
                "quantity": 1
            }],
            success_url="https://your-app-url.streamlit.app",
            cancel_url="https://your-app-url.streamlit.app"
        )

        # INSTANT REDIRECT (no second click)
        st.markdown(
            f'<meta http-equiv="refresh" content="0; url={checkout.url}">',
            unsafe_allow_html=True
        )