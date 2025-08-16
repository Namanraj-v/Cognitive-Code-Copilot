import streamlit as st
import requests
import pandas as pd

# --- Page Configuration ---
st.set_page_config(
    layout="wide", 
    page_title="Cognitive Code Copilot",
    page_icon="🧠"
)

# --- API URLs ---
REFACTOR_API_URL = "http://127.0.0.1:8000/refactor"
CHAT_API_URL = "http://127.0.0.1:8000/chat"

# --- Custom CSS (same as before) ---
st.markdown("""
<style>
    /* Gradient background */
    .stApp {
        background-image: linear-gradient(to bottom right, #312E81, #1E1B4B);
    }
    /* "Glassmorphic" container style */
    .st-emotion-cache-16txtl3, .st-emotion-cache-13ln4jf {
        background: rgba(49, 46, 129, 0.6);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(244, 114, 182, 0.2);
        border-radius: 16px;
        padding: 2rem;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
    }
</style>
""", unsafe_allow_html=True)

# --- Session State Initialization ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "analysis_done" not in st.session_state:
    st.session_state.analysis_done = False
if "current_code" not in st.session_state:
    st.session_state.current_code = ""

# --- App Header ---
st.title("🧠 Cognitive Code Copilot")
st.divider()

# --- NEW: Three-Column Layout ---
col1, col2, col3 = st.columns((1, 1, 1), gap="large")

# --- COLUMN 1: Code Input ---
with col1:
    with st.container():
        st.header("Your Python Code")
        with st.form(key='refactor_form'):
            user_code = st.text_area("Paste code here", height=400, label_visibility="collapsed")
            st.write("**Choose Refactoring Style**")
            b_col1, b_col2, b_col3 = st.columns(3)
            with b_col1:
                readability_button = st.form_submit_button(label="Readability ✨", use_container_width=True, type="primary")
            with b_col2:
                conciseness_button = st.form_submit_button(label="Concise ⚡", use_container_width=True)
            with b_col3:
                doc_button = st.form_submit_button(label="Docs & Types 📄", use_container_width=True)

refactor_style = None
if readability_button: refactor_style = "readability"
elif conciseness_button: refactor_style = "conciseness"
elif doc_button: refactor_style = "documentation"

if refactor_style and user_code:
    with st.spinner("🤖 Analyzing and refactoring..."):
        try:
            payload = {"code": user_code, "refactor_style": refactor_style}
            response = requests.post(REFACTOR_API_URL, json=payload)
            response.raise_for_status()
            data = response.json()
            st.session_state.analysis_done = True
            st.session_state.refactor_data = data
            st.session_state.current_code = data['refactored_code']
            st.session_state.messages = []
        except requests.exceptions.RequestException:
            st.error("Connection Error: Backend unreachable.")
        except Exception as e:
            st.error(f"An error occurred: {e}")

# --- COLUMN 2: Assistant's Output ---
with col2:
    with st.container():
        st.header("Assistant's Output")
        if st.session_state.analysis_done:
            data = st.session_state.refactor_data
            tab1, tab2, tab3, tab4 = st.tabs(["📊 Analysis", "✅ Refactored", "🧪 Tests", "🛡️ Security"])
            with tab1:
                st.subheader("Code Quality Metrics")
                st.metric(label="Cyclomatic Complexity", value=data['analysis_report'].get('cyclomatic_complexity', 'N/A'))
            with tab2:
                st.code(st.session_state.current_code, language='python', line_numbers=True)
            with tab3:
                st.code(data['unit_tests'], language='python', line_numbers=True)
            with tab4:
                st.subheader("Security Scan")
                security_issues = data['analysis_report'].get('security_issues', [])
                if not security_issues: st.success("✅ No security issues found.")
                else:
                    st.warning(f"🚨 Found {len(security_issues)} potential issue(s).")
                    st.dataframe(pd.DataFrame(security_issues), use_container_width=True)
        else:
            st.info("Paste your code on the left to begin.")

# --- COLUMN 3: Chat Copilot ---
with col3:
    with st.container():
        st.header("💬 Chat Copilot")
        
        # Chat message display area
        chat_container = st.container(height=400)
        for message in st.session_state.messages:
            with chat_container.chat_message(message["role"]):
                st.markdown(message["content"])

        # Chat input box
        if prompt := st.chat_input("Ask a follow-up question..."):
            if not st.session_state.analysis_done:
                st.warning("Please analyze a piece of code first.")
            else:
                st.session_state.messages.append({"role": "user", "content": prompt})
                with chat_container.chat_message("user"):
                    st.markdown(prompt)

                with chat_container.chat_message("assistant"):
                    with st.spinner("Thinking..."):
                        chat_payload = {
                            "code": st.session_state.current_code,
                            "history": st.session_state.messages,
                            "question": prompt
                        }
                        response = requests.post(CHAT_API_URL, json=chat_payload)
                        if response.status_code == 200:
                            assistant_response = response.json()["answer"]
                            st.markdown(assistant_response)
                            st.session_state.messages.append({"role": "assistant", "content": assistant_response})
                            if "```python" in assistant_response:
                                new_code = assistant_response.split("```python")[1].split("```")[0]
                                st.session_state.current_code = new_code
                                st.success("Code in the 'Refactored' tab updated!")
                        else:
                            st.error("Failed to get a response.")