import ollama
import json

with open("./models/tools.json") as f:
    tools = json.loads(f.read())

available_tools = "\n\n".join(f"Function {tool['name']} to {tool['description']}:\n{tool}" for tool in tools)

toolPrompt = f"""
Analyse the given prompt and decided whether or not it can be answered by a any of the following functions that you have access to:
{available_tools}
 
If you choose to call a function ONLY respond in the JSON format:

{{"name": function name, "parameters": dictionary of argument name and its value}}

Do not use variables.
 
Reminder:
- Function calls MUST follow the specified format
- Required parameters MUST always be specified in the response
- Only call one function at a time
- Put the entire function call reply on one line
- If you decide that the prompt cannot be answered by any of the available functions then you have to answer normally
- Dont ever mention the function calls in a normal conversation or answer

A list of negative responses from the assistant are given to better your responses:
* I realize that the prompt "How are you doing today?" does not match with either of the provided functions.
* This prompt cannot be answered by any of the given functions.
* This prompt can be answered.
* This prompt cannot be answered.
Dont ever say anything like that, just keep to the conversation unless you decide the prompt can be answered by one of the available function
"""

print(toolPrompt)

system_message = """
Your name is Cortex.
You should always give reasonably short answers.
When you receive a command like "turn off the light" or "turn on the light", you should just indicate that you are doing as told.
"""
 
while True:
    user_input = input("You: ")
    response = ollama.chat(model="llama3.1", messages=[
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_input},
        {"role": "user", "content": toolPrompt},
    ])
    print("Bot:", response["message"]["content"])