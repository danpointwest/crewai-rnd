import streamlit as st
import requests
import json

st.set_page_config(page_title="Streamlit to AWS Lambda + S3", layout="wide")

# Layout: Left = input form, Right = response display
left_col, right_col = st.columns(2)

# ---------- LEFT SIDE: Dynamic Input ---------- #
with left_col:
    st.header("📤 Send JSON to Lambda")

    message = st.text_input("Enter your message")
    user_id = st.text_input("Enter your user ID")
    email = st.text_input("Enter your email")

    if st.button("Send to API"):
        # Build original user payload
        raw_payload = {
            "message": message,
            "user_id": user_id,
            "email": email
        }

        # Wrap it under 'body' for API Gateway + Lambda compatibility
        payload = {
            "body": json.dumps(raw_payload)
        }

        url = "https://gwoo0j57e4.execute-api.us-east-1.amazonaws.com/dev/trigger"
        headers = {"Content-Type": "application/json"}

        try:
            response = requests.post(url, json=payload, headers=headers)
            response_json = response.json()
            st.session_state['response'] = {
                "status_code": response.status_code,
                "data": response_json
            }
        except Exception as e:
            st.session_state['response'] = {
                "status_code": "Error",
                "data": {"error": str(e)}
            }

# ---------- RIGHT SIDE: Show the API Response ---------- #
with right_col:
    st.header("📥 Response")
    if 'response' in st.session_state:
        res = st.session_state['response']
        st.write(f"**Status Code:** {res['status_code']}")

        try:
            # If response contains a stringified 'body', parse it
            body = res['data'].get("body", res['data'])
            if isinstance(body, str):
                body = json.loads(body)

            st.subheader("API Returned:")
            st.json(body)

            if body.get("file_url"):
                st.markdown(f"[🔗 View File in S3]({body['file_url']})", unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Failed to parse response: {e}")
