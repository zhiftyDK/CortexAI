import ollama

system_message = """
Your name is Cortex.
You should always give reasonably short answers.
When you receive a command like "turn off the light" or "turn on the light", you should just indicate that you are doing as told.
"""

conversation_history = [{"role": "system", "content": system_message}]

def ask_question_memory(question):
    try: 
        conversation_history.append({"role": "user", "content": question})

        response = ollama.chat(model="llama3.1:8b-instruct-q4_0", messages=conversation_history)

        conversation_history.append({"role": "assistant", "content": response["message"]["content"]})

        return response["message"]["content"]
    except ollama.ResponseError as e:
        print(f"An error occurred: {e}")
        return f"The request failed: {e}"