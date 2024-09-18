import ollama
import json

with open("./models/tools.json") as f:
    tools = json.loads(f.read())

available_tools = "\n".join(f"Function {tool['name']} to {tool['description']}:\n{tool}" for tool in tools)

toolPrompt = f"""
Analyse the given prompt and decided whether or not it can be answered by a any of the following functions that you have access to:
{available_tools}
 
If you choose to call a function ONLY respond in the JSON format:

{{"name": function name, "parameters": dictionary of argument name and its value}}

Do not use variables.
 
Reminder:
- If looking for real time information use relevant functions before falling back to brave_search
- Function calls MUST follow the specified format
- Required parameters MUST always be specified in the response
- Only call one function at a time
- Put the entire function call reply on one line
"""

print(toolPrompt)

system_message = """
Your name is Cortex.
You should always give reasonably short answers.
When you receive a command like "turn off the light" or "turn on the light", you should just indicate that you are doing as told.
"""
 
response = ollama.chat(model="llama3.1:8b-instruct-q4_0", messages=[
    {"role": "system", "content": system_message},
    {"role": "user", "content": "What is your name?"},
    {"role": "user", "content": toolPrompt},
])
 
try:
    tool = json.loads(response["message"]["content"])
    print(tool)
except:
    print(response["message"]["content"])