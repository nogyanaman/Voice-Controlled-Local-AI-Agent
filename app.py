import streamlit as st
import tempfile
import os
from audio import AudioProcessor
from brain import IntentEngine
from actions import ActionHandler

st.set_page_config(page_title="Voice Agent Sandbox", layout="centered")

# Memory
if "history" not in st.session_state:
    st.session_state.history = []

# Caching so that Streamlit don't reload the models every time a button is clicked
@st.cache_resource(show_spinner=False)
def load_backend():
    return AudioProcessor(), IntentEngine(), ActionHandler()

st.title("🎙️ Local AI Assistant")

audio_proc, brain, actions = load_backend()

# UI inputs
mic_audio = st.audio_input("Record a command") 
upload_audio = st.file_uploader("Or upload an audio file", type=['wav', 'mp3']) 

source = mic_audio or upload_audio

if source:
    st.divider()
    
    # Audio to a temp file for Whisper
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(source.getbuffer())
        tmp_path = tmp.name
    
    try:
        with st.status("Working on it...", expanded=True) as status:
            st.write("Listening...")
            transcript = audio_proc.process(tmp_path)
            st.info(f'"{transcript}"') 
            
            st.write("Thinking...")
            parsed = brain.analyze(transcript)
            intent = parsed.get("intent", "chat")
            
            st.write("Executing...")
            status_msg, output_data = actions.execute(
                intent, 
                parsed.get("content"), 
                transcript, 
                parsed.get("filename")
            )
            
            status.update(label="Done!", state="complete", expanded=False)
        
        # Final result
        st.subheader("Result")
        if intent in ["create_file", "write_code"]:
            st.success(status_msg)
            st.code(output_data) 
        else:
            st.write(output_data) 

        # Memory log
        st.session_state.history.append({
            "cmd": transcript,
            "action": status_msg
        })

    finally:
        # Cleanup temp file
        if os.path.exists(tmp_path):
            os.remove(tmp_path)

# Session history
if st.session_state.history:
    st.divider()
    with st.expander("Session History"):
        for item in reversed(st.session_state.history):
            st.markdown(f" **User:** {item['cmd']}  \n **System:** {item['action']}")
            st.markdown("---")