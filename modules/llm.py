import ollama

modelfile="""
FROM llama3.1
SYSTEM Your name is Cortex. You should always give reasonably short answers.
"""
ollama.create(model="cortex", modelfile=modelfile)

def generate(user_input):
    message = {
            "role": "user",
            "content": user_input,
    }
    response = ollama.chat(model="cortex", messages=[message])
    return response