import streamlit as st
import requests
import uuid
import time

BACKEND_URL = "http://localhost:8000"

st.set_page_config(
    page_title="BizSense AI · Powered by Nexora",
    page_icon="⬢",
    layout="wide"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: linear-gradient(180deg, #071020 0%, #0b1220 45%, #0f172a 100%);
    color: #f8fafc;
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0b1324 0%, #0f172a 100%);
    border-right: 1px solid rgba(255,255,255,0.07);
}

.block-container {
    padding-top: 1rem;
    padding-bottom: 1rem;
    max-width: 1200px;
}

[data-testid="stHeader"] {
    background: transparent;
}

/* Global text */
h1, h2, h3, h4, h5, h6, p, div, span, label {
    color: #f8fafc;
}

/* Tabs */
button[data-baseweb="tab"] {
    color: #cbd5e1 !important;
    font-weight: 600 !important;
}
button[data-baseweb="tab"][aria-selected="true"] {
    color: #ffffff !important;
}

/* Labels */
.stTextInput label,
.stTextArea label,
.stFileUploader label,
.stSelectbox label {
    color: #e2e8f0 !important;
    font-weight: 600 !important;
}

/* Inputs */
.stTextInput input,
.stTextArea textarea,
input,
textarea {
    color: #0f172a !important;
    -webkit-text-fill-color: #0f172a !important;
    background: linear-gradient(180deg, #ffffff 0%, #f8fafc 100%) !important;
    border: 1px solid #cbd5e1 !important;
    border-radius: 14px !important;
    padding: 0.75rem 0.9rem !important;
    box-shadow: inset 0 1px 2px rgba(0,0,0,0.04) !important;
}

.stTextInput input:focus,
.stTextArea textarea:focus,
input:focus,
textarea:focus {
    border: 1px solid #8b5cf6 !important;
    box-shadow: 0 0 0 1px #8b5cf6 !important;
}

.stTextInput input::placeholder,
.stTextArea textarea::placeholder,
input::placeholder,
textarea::placeholder {
    color: #64748b !important;
    opacity: 1 !important;
}

/* Buttons */
.stButton > button,
[data-testid="stDownloadButton"] > button {
    width: 100%;
    border-radius: 14px !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    background: linear-gradient(180deg, #172338 0%, #101827 100%) !important;
    color: #f8fafc !important;
    font-weight: 700 !important;
    min-height: 44px;
    box-shadow: 0 6px 18px rgba(0,0,0,0.18);
}

.stButton > button:hover,
[data-testid="stDownloadButton"] > button:hover {
    border-color: rgba(139,92,246,0.55) !important;
    box-shadow: 0 0 0 1px rgba(139,92,246,0.25), 0 8px 18px rgba(0,0,0,0.22);
}

/* Cards */
.bizsense-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 22px;
    padding: 22px 22px 18px 22px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.22);
    backdrop-filter: blur(10px);
}

/* Branding */
.bizsense-brand {
    text-align: center;
    padding: 4px 0 16px 0;
}

.bizsense-logo {
    font-size: 56px;
    line-height: 1;
    color: #a78bfa;
    filter: drop-shadow(0 0 14px rgba(167,139,250,0.28));
}

.bizsense-title {
    font-size: 36px;
    font-weight: 800;
    letter-spacing: -0.03em;
    color: #ffffff;
    margin-top: 4px;
}

.bizsense-subtitle {
    font-size: 14px;
    color: #94a3b8;
    margin-top: 4px;
}

.bizsense-tagline {
    font-size: 15px;
    color: #cbd5e1;
    margin-top: 10px;
}

.sidebar-brand {
    text-align: center;
    padding: 10px 0 18px 0;
}

.sidebar-logo {
    font-size: 44px;
    color: #a78bfa;
}

.sidebar-title {
    font-size: 25px;
    font-weight: 800;
    color: #ffffff;
    margin-top: 2px;
}

.sidebar-subtitle {
    font-size: 12px;
    color: #94a3b8;
}

.brand-pill {
    display: inline-block;
    margin-top: 10px;
    padding: 6px 12px;
    border-radius: 999px;
    background: rgba(99,102,241,0.12);
    border: 1px solid rgba(99,102,241,0.25);
    color: #c7d2fe;
    font-size: 12px;
    font-weight: 700;
}

/* Chat messages */
[data-testid="stChatMessage"] {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 18px;
    padding: 0.5rem 0.85rem;
    margin-bottom: 0.7rem;
    box-shadow: 0 6px 18px rgba(0,0,0,0.16);
}

[data-testid="stChatMessage"] p,
[data-testid="stChatMessage"] div,
[data-testid="stChatMessage"] span,
[data-testid="stChatMessage"] .stMarkdown {
    color: #f8fafc !important;
    opacity: 1 !important;
    font-size: 15px;
    line-height: 1.6;
}

/* Chat input */
[data-testid="stChatInput"] {
    background: transparent !important;
    border-top: none !important;
    padding-top: 0.75rem;
}

[data-testid="stChatInput"] textarea {
    color: #0f172a !important;
    -webkit-text-fill-color: #0f172a !important;
    background: linear-gradient(180deg, #ffffff 0%, #f8fafc 100%) !important;
    border: 1px solid #cbd5e1 !important;
    border-radius: 16px !important;
}

[data-testid="stChatInput"] textarea::placeholder {
    color: #64748b !important;
}

/* Sidebar uploader */
[data-testid="stFileUploader"] {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 16px !important;
    padding: 10px !important;
}

.small-muted {
    color: #94a3b8 !important;
    font-size: 13px;
}
</style>
""", unsafe_allow_html=True)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user" not in st.session_state:
    st.session_state.user = None
if "chats" not in st.session_state:
    st.session_state.chats = {}
if "current_chat" not in st.session_state:
    st.session_state.current_chat = None
if "last_uploaded_name" not in st.session_state:
    st.session_state.last_uploaded_name = None


def create_new_chat():
    chat_id = str(uuid.uuid4())
    st.session_state.current_chat = chat_id
    st.session_state.chats[chat_id] = {
        "name": "Untitled Chat",
        "messages": []
    }


def logout():
    st.session_state.logged_in = False
    st.session_state.user = None
    st.session_state.chats = {}
    st.session_state.current_chat = None
    st.session_state.last_uploaded_name = None
    st.rerun()


if not st.session_state.logged_in:
    st.markdown("""
    <div class="bizsense-brand">
        <div class="bizsense-logo">⬢</div>
        <div class="bizsense-title">BizSense AI</div>
        <div class="bizsense-subtitle">Powered by Nexora Technologies</div>
    </div>
    """, unsafe_allow_html=True)

    left, center, right = st.columns([1, 1.35, 1])

    with center:
        st.markdown('<div class="bizsense-card">', unsafe_allow_html=True)
        tab1, tab2 = st.tabs(["Login", "Sign Up"])

        with tab1:
            st.subheader("Login")
            login_username = st.text_input("Username", key="login_username", placeholder="Enter username")
            login_password = st.text_input("Password", type="password", key="login_password", placeholder="Enter password")

            if st.button("Login", use_container_width=True):
                try:
                    response = requests.post(
                        f"{BACKEND_URL}/login",
                        json={
                            "username": login_username,
                            "password": login_password
                        },
                        timeout=30
                    )

                    if response.status_code == 200:
                        data = response.json()
                        st.session_state.logged_in = True
                        st.session_state.user = data["user"]["username"]

                        if not st.session_state.chats:
                            create_new_chat()

                        st.success("Login successful")
                        st.rerun()
                    else:
                        try:
                            detail = response.json().get("detail", response.text)
                        except Exception:
                            detail = response.text
                        st.error(detail)

                except requests.exceptions.ConnectionError:
                    st.error("Backend is not running. Start FastAPI first.")
                except Exception as e:
                    st.error(f"Error: {str(e)}")

        with tab2:
            st.subheader("Create Account")
            signup_username = st.text_input("Choose Username", key="signup_username", placeholder="Create username")
            signup_password = st.text_input("Choose Password", type="password", key="signup_password", placeholder="Create password")

            if st.button("Sign Up", use_container_width=True):
                try:
                    response = requests.post(
                        f"{BACKEND_URL}/signup",
                        json={
                            "username": signup_username,
                            "password": signup_password
                        },
                        timeout=30
                    )

                    if response.status_code == 200:
                        st.success("User created successfully. Please login.")
                    else:
                        try:
                            detail = response.json().get("detail", response.text)
                        except Exception:
                            detail = response.text
                        st.error(detail)

                except requests.exceptions.ConnectionError:
                    st.error("Backend is not running. Start FastAPI first.")
                except Exception as e:
                    st.error(f"Error: {str(e)}")

        st.markdown('</div>', unsafe_allow_html=True)

    st.stop()

if not st.session_state.chats:
    create_new_chat()

with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
        <div class="sidebar-logo">⬢</div>
        <div class="sidebar-title">BizSense AI</div>
        <div class="sidebar-subtitle">Powered by Nexora Technologies</div>
        <div class="brand-pill">Enterprise Knowledge Assistant</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"<div class='small-muted'>Logged in as: <b>{st.session_state.user}</b></div>", unsafe_allow_html=True)
    st.write("")

    if st.button("⟡ Create New Chat", use_container_width=True):
        create_new_chat()
        st.rerun()

    st.subheader("Chats")

    sorted_chats = list(st.session_state.chats.items())
    sorted_chats.sort(key=lambda x: x[0] != st.session_state.current_chat)

    for chat_id, chat_data in sorted_chats:
        if st.button(chat_data["name"], key=f"chat_{chat_id}", use_container_width=True):
            st.session_state.current_chat = chat_id
            st.rerun()

    st.subheader("Upload Files")
    uploaded_file = st.file_uploader(
        "Upload TXT, PDF, or DOCX",
        type=["txt", "pdf", "docx"]
    )

    if uploaded_file is not None:
        try:
            files = {
                "file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)
            }

            response = requests.post(
                f"{BACKEND_URL}/upload/{st.session_state.user}",
                files=files,
                timeout=120
            )

            if response.status_code == 200:
                st.session_state.last_uploaded_name = uploaded_file.name
                st.success(f"Uploaded: {uploaded_file.name}")
            else:
                try:
                    detail = response.json().get("detail", response.text)
                except Exception:
                    detail = response.text
                st.error(detail)

        except requests.exceptions.ConnectionError:
            st.error("Backend is not running. Start FastAPI first.")
        except Exception as e:
            st.error(f"Error: {str(e)}")

    current_chat = st.session_state.chats[st.session_state.current_chat]
    current_messages = current_chat["messages"]

    if st.button("🗑 Clear Current Chat", use_container_width=True):
        current_chat["messages"] = []
        current_chat["name"] = "Untitled Chat"
        st.rerun()

    export_text = "\n\n".join(
        [f"{msg['role'].upper()}: {msg['content']}" for msg in current_messages]
    )

    st.download_button(
        "⬇ Export Current Chat",
        data=export_text,
        file_name="bizsense_chat.txt",
        mime="text/plain",
        use_container_width=True
    )

    if st.button("🚪 Logout", use_container_width=True):
        logout()

st.markdown("""
<div class="bizsense-brand">
    <div class="bizsense-logo">⬢</div>
    <div class="bizsense-title">BizSense AI</div>
    <div class="bizsense-subtitle">Powered by Nexora Technologies</div>
    <div class="bizsense-tagline">
        Your premium enterprise assistant for documents, memory, and smart answers
    </div>
</div>
""", unsafe_allow_html=True)

if st.session_state.last_uploaded_name:
    st.markdown(
        f"<div class='small-muted' style='text-align:center; margin-bottom:10px;'>Attached file: {st.session_state.last_uploaded_name}</div>",
        unsafe_allow_html=True
    )

current_chat = st.session_state.chats[st.session_state.current_chat]
messages = current_chat["messages"]

for msg in messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

query = st.chat_input("Ask BizSense AI anything...")

if query:
    if current_chat["name"] == "Untitled Chat":
        current_chat["name"] = query[:30] + ("..." if len(query) > 30 else "")

    current_chat["messages"].append({
        "role": "user",
        "content": query
    })

    with st.chat_message("user"):
        st.markdown(query)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        placeholder.markdown("Thinking...")

        try:
            response = requests.post(
                f"{BACKEND_URL}/chat",
                json={
                    "question": query,
                    "user": st.session_state.user,
                    "history": messages
                },
                timeout=120
            )

            if response.status_code == 200:
                data = response.json()
                answer = data.get("answer", "I don't know")

                typed = ""
                for char in answer:
                    typed += char
                    placeholder.markdown(typed)
                    time.sleep(0.005)

                current_chat["messages"].append({
                    "role": "assistant",
                    "content": answer
                })
            else:
                try:
                    detail = response.json().get("detail", response.text)
                except Exception:
                    detail = response.text

                placeholder.markdown(f"Error: {detail}")
                current_chat["messages"].append({
                    "role": "assistant",
                    "content": f"Error: {detail}"
                })

        except requests.exceptions.ConnectionError:
            placeholder.markdown("Backend is not running. Start FastAPI first.")
            current_chat["messages"].append({
                "role": "assistant",
                "content": "Backend is not running. Start FastAPI first."
            })

        except Exception as e:
            placeholder.markdown(f"Error: {str(e)}")
            current_chat["messages"].append({
                "role": "assistant",
                "content": f"Error: {str(e)}"
            })