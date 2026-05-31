from openai import OpenAI
from dotenv import load_dotenv
import os, json, subprocess
import logging

logging.basicConfig(level=logging.INFO)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)
load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

memory = open('memory.md','r').read() if os.path.exists('memory.md') else ""
messages = [{
        "role": "system",
        "content": f"You are a personal assistant. "
                   f"Memory:\n{memory}\n\n"
                   f"Use the available tools when needed to accomplish user's tasks. Leverage OpenAI's function calling to use tools. Always think step by step and use tools when needed. "
    }]

TOOL_FUNCTIONS = {
    "shell": lambda cmd: subprocess.getoutput(cmd),
    "remember": lambda note: open('memory.md','a').write(f"\n- {note}") or "saved",    
}

TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "shell",
            "description": "Execute a shell command and return the output",
            "parameters": {
                "type": "object",
                "properties": {
                    "cmd": {"type": "string", "description": "The shell command to execute"}
                },
                "required": ["cmd"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "remember",
            "description": "Save a note to memory",
            "parameters": {
                "type": "object",
                "properties": {
                    "note": {"type": "string", "description": "The note to remember"}
                },
                "required": ["note"]
            }
        }
    }
]

def run_agent(goal:str):
    
    messages.append({
        "role": "user",
        "content": goal
    })

    for _ in range(10):
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            tools=TOOL_SCHEMAS,
        )

        choice = response.choices[0]
        #logger.info(f"Assistant: {choice}\n")

        # If there are tool calls, process them
        if choice.message.tool_calls:
            messages.append({
                "role": "assistant",
                "content": choice.message.content or "",
                "tool_calls": choice.message.tool_calls
            })
            
            for tool_call in choice.message.tool_calls:
                tool_name = tool_call.function.name
                tool_args = json.loads(tool_call.function.arguments)
                logger.info("Calling tool: %s with args: %s\n", tool_name, tool_args)
                
                if tool_name in TOOL_FUNCTIONS:
                    result = TOOL_FUNCTIONS[tool_name](**tool_args)
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": str(result)
                    })
        else:
            # No tool calls, this is the final answer
            print(f"Shanky: {choice.message.content}")
            messages.append({
                "role": "assistant",
                "content": choice.message.content or "",
            })
            break

def interactive_chat():
    print("Welcome to the interactive agent. Type 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input and user_input.lower() == "exit":
            print("Goodbye!")
            break
        run_agent(user_input)

if __name__ == "__main__":
    interactive_chat()

