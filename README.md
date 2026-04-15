# Voice Controlled Local AI Agent

This is a local, voice-controlled AI agent built with Streamlit, Whisper, and Ollama. It listens to audio commands, figures out what you want to do and executes local actions like creating files, writing code, or summarizing text.
AI Agent basically accept audio input, accurately classify the user's intent, execute the appropriate local tools, and display the entire pipeline's results in a clean User Interface (UI). 

## Project Structure

voice_agent/
├── output/                 # Output folder
├── config.py               # Holds global settings for eg. like model names and paths, so we don't have magic strings everywhere.
├── audio.py                # Handles loading Whisper and transcribing the audio files into text.
├── brain.py                # LLM prompt logic. It feeds the transcript to Llama 3 and forces a clean JSON response with the intent and payload.
├── actions.py              # The tool executor. This actually creates the files, writes the code, or calls the LLM again to summarize text.
├── app.py                  # The main Streamlit UI. It glues all the modules together and manages the visual state.
├── requirements.txt        # Python package dependencies.
└── README.md

## Additional features

1. Memory / Session History: The UI maintains a persistent, scrollable log of all past transcripts and system actions during the session.
2. Graceful Degradation: Added fallback error handling for when the LLM hallucinates JSON formatting or when file I/O operations fail, preventing app crashes.
3. Strict Safety Sandbox: Built-in path sanitization ensures the agent can only create or modify files inside the dedicated output/ folder, preventing accidental system overwrites.
4. Model Caching: Utilizes Streamlit's @st.cache_resource to load the Whisper model and backend handlers only once per session, drastically speeding up subsequent voice commands.
5. LLM Output Sanitization: Includes custom parsing logic to strip away markdown code blocks (e.g., ```json) when the local LLM disobeys formatting instructions, ensuring the pipeline doesn't crash.
6. Dual Audio Support: Both microphone or upload existing audio files.
7. Automated Temp File Cleanup: Audio buffers are handled securely using Python's tempfile library and are automatically deleted from the disk immediately after transcription.
8. Real-time Pipeline UI: Uses Streamlit status containers.

## How to run it

1. **Install Python 3.10+ and Ollama** (if you don't have it already).
2. **Venv Environment Activation:**
   ```bash
   python -m venv venv 
   .\venv\Scripts\activate
3. **Install the dependencies:** 
   ```bash  
   pip install -r requirements.txt
4. **Running and pulling model:**
   ```bash
   ollama run llama3  
5. **Run the app:**
   ```bash                                                                        
   streamlit run app.py


