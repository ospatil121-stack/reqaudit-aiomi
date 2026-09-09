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

# Initialize Anthropic client
@st.cache_resource
def get_client():
    api_key = st.secrets.get("ANTHROPIC_API_KEY")
    if not api_key:
        st.error("⚠️ ANTHROPIC_API_KEY not found in .streamlit/secrets.toml")
        st.stop()
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
