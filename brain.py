import json
import ollama
from config import OLLAMA_MODEL

class IntentEngine:
    def __init__(self):
        self.model = OLLAMA_MODEL

    def analyze(self, text: str) -> dict:
        prompt = f"""
        Read this transcript: "{text}"
        Figure out what the user wants to do. Pick one intent from this list: create_file, write_code, summarize, chat.
        
        Return ONLY valid JSON.
        Format:
        {{
            "intent": "string",
            "filename": "string or null", 
            "content": "code or text to summarize, or null"
        }}
        """
        
        try:
            response = ollama.chat(model=self.model, messages=[
                {'role': 'user', 'content': prompt}
            ])
            
            raw_reply = response['message']['content'].strip()
            
            if raw_reply.startswith('```json'):
                raw_reply = raw_reply[7:-3]
            elif raw_reply.startswith('```'):
                raw_reply = raw_reply[3:-3]
                
            return json.loads(raw_reply)
            
        except json.JSONDecodeError:
            print("Failed to parse JSON. Model probably hallucinated formatting.")
            # Fallback so the app doesn't crash
            return {"intent": "chat", "filename": None, "content": None}
        except Exception as e:
            print(f"Ollama connection error: {e}")
            return {"intent": "chat", "filename": None, "content": None}