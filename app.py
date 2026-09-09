import streamlit as st
from anthropic import Anthropic

# Initialize Streamlit page config
st.set_page_config(
    page_title="ReqAudit AIOMI",
    page_icon="📋",
    layout="wide"
)

# Page title
st.title("📋 ReqAudit AIOMI")
st.markdown("AI-powered requirement auditing and analysis")

# Check for API key
api_key = st.secrets.get("ANTHROPIC_API_KEY", "").strip()

if not api_key or api_key == "sk-ant-api03-YOUR-KEY-HERE":
    st.error("""
    ⚠️ **API Key Not Configured**
    
    Please add your Anthropic API key to the Streamlit Cloud secrets:
    1. Go to your app settings
    2. Click "Secrets" 
    3. Add: `ANTHROPIC_API_KEY = "sk-ant-api03-YOUR-ACTUAL-KEY"`
    4. Save and refresh
    """)
    st.stop()

# Initialize Anthropic client
@st.cache_resource
def get_client():
    return Anthropic(api_key=api_key)

client = get_client()

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask me anything about your requirements..."):
    # Add user message to history
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })
    
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get response from Claude
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = client.messages.create(
                    model="claude-3-5-sonnet-20241022",
                    max_tokens=1024,
                    messages=st.session_state.messages
                )
                
                assistant_message = response.content[0].text
                st.markdown(assistant_message)
                
                # Add assistant message to history
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": assistant_message
                })
            except Exception as e:
                st.error(f"Error communicating with Claude: {str(e)}")

# Sidebar
with st.sidebar:
    st.header("Settings")
    
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.rerun()
    
    st.divider()
    st.markdown("""
    ### About ReqAudit AIOMI
    This application uses Claude AI to help audit and analyze requirements.
    
    **Features:**
    - Chat-based interface
    - AI-powered analysis
    - Conversation history
    """)
