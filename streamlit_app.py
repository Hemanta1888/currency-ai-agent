import streamlit as st
import requests

st.set_page_config(page_title="💱 AI Currency Converter", page_icon="💱", layout="wide")

st.markdown(
    """
    <div style='margin-top: -50px; text-align: center;'>
        <h1>💱 AI-Powered Currency Converter</h1>
        <p><b>Convert USD to global currencies using AI Agent.</b></p>
    </div>
    """,
    unsafe_allow_html=True
)


input_col, output_col = st.columns([1, 2], gap="large")

with input_col:
    st.header("💡 Enter Details")

    usd_amount = st.number_input("USD Amount", min_value=1.0, value=100.0, step=1.0)
    user_input = st.text_input("Conversion Query", value="Convert to Indian currency.")
    convert_button = st.button("🌍 Convert Now")

with output_col:
    if convert_button:
        thinking = st.empty()
        thinking.markdown("⏳ Thinking...")

        try:
            response = requests.post(
                "http://0.0.0.0:8080/convert",
                json={"usd_amount": usd_amount, "user_input": user_input},
                # timeout=15
            )
            thinking.empty()

            if response.status_code == 200:
                data = response.json()

                # st.success(f"✅ Converted to {data['target_currency']}")
                st.metric(label="💱 Converted Amount", value=f"{data['total_amount']} {data['target_currency']}")
                st.caption(f"📊 USD After Profit: {data['total_usd']} USD")

                image_placeholder = st.empty()
                image_placeholder.markdown(f"🚀 On my way to generate **{data['target_currency']}** currency image...")

                image_response = requests.get(
                    f"http://0.0.0.0:8080/generate-image?currency={data['target_currency']}",
                    timeout=40
                )

                if image_response.status_code == 200:
                    image_data = image_response.json().get("image_base64")
                    image_placeholder.image(
                        f"data:image/png;base64,{image_data}",
                        width=150,
                        use_container_width=True,
                        caption=f"{data['target_currency']} Currency"
                    )
                else:
                    image_placeholder.error("⚠️ Could not generate image.")
            else:
                st.error(f"❌ High number of requests. Can't do it right now. Please try again later.")
        except Exception as e:
            thinking.empty()
            st.error(f"❌ High number of requests. Can't do it right now. Please try again later.")
            print(f"Error: {e}")
