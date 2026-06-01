from typing import List, Tuple
from dotenv import load_dotenv
import os
load_dotenv()

def choose_provider_and_model(messages: List[dict]) -> Tuple[str, str]:
    """
    Choose the appropriate provider and model based on the messages.
    Start with simple length based selection for demonstration purposes. 
    Can easily be switched to more sophisticated logic later.
    """

    # Get last user utterance from messages
    user_msg = next(m for m in reversed(messages) if m.get("role") == "user")

    if not user_msg:
        # return default model
        print("here!!!!\n")
        return "cerebras", os.getenv("CEREBRAS_MODEL")
    
    content = user_msg.get("content").lower()
    tokens = len(content.split()) # Simple length based selection for demonstration purposes

    # If a long message, use a faster smaller model
    if tokens > 500:
        return "groq", "llama-3.2-3b-fast"
    
    if any(k in content for k in ("code", "function", "script", "python")):
        print("Picking GROQ")
        return "groq", os.getenv("GROQ_MODEL")
    if any(k in content for k in ("reason", "plan", "think", "explain")):
        print("Picking CEREBRAS")
        return "cerebras", os.getenv("CEREBRAS_MODEL")
    
    return "cerebras", os.getenv("CEREBRAS_MODEL") # Default to Cerebras

