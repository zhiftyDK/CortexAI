import ollama

conversation_history = []

def generate(question):
    try:
        system_message = """
        Your name is Cortex.
        You should always give reasonably short answers.
        When you receive a command like "turn off the light" or "turn on the light", you should just indicate that you are doing as told.
        """

        message = {
            "role": "user",
            "content": question,
        }

        conversation_history.append(message)

        response = ollama.chat(model="llama3.1:8b-instruct-q4_0", messages=[
            {"role": "system", "content": system_message},
            *conversation_history
        ])

        conversation_history.append({"role": "assistant", "content": response["message"]["content"]})

        return response["message"]["content"]
    except ollama.ResponseError as e:
        print(f"An error occurred: {e}")
        return f"The request failed: {e}"