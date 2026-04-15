import os
import ollama
from config import OUTPUT_DIR, OLLAMA_MODEL

class ActionHandler:
    def execute(self, intent: str, content: str, text: str, filename: str = None):
        
        if intent in ["create_file", "write_code"]: 
            # Striping out the paths to prevent writing outside the output
            safe_name = os.path.basename(filename or "untitled.txt")
            target_path = OUTPUT_DIR / safe_name
            
            try:
                with open(target_path, "w", encoding="utf-8") as f:
                    f.write(content or "")
                return f"Saved file to `{target_path.name}`", content or "Empty file created..."
            except Exception as e:
                return "File not saved...", str(e)
                
        elif intent == "summarize": 
            # Default transcript
            target_text = content if content else text
            res = ollama.chat(model=OLLAMA_MODEL, messages=[
                {'role': 'system', 'content': 'Give the summary of the text.'},
                {'role': 'user', 'content': target_text}
            ])
            return "Summary generated.", res['message']['content']
            
        elif intent == "chat": 
            res = ollama.chat(model=OLLAMA_MODEL, messages=[
                {'role': 'user', 'content': text}
            ])
            return "Chat response.", res['message']['content']
            
        return "Unknown command.", "Specify what you want to do here."