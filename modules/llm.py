import ollama

modelfile="""
FROM llama3.1
SYSTEM Your name is Cortex. You should always give reasonably short answers. When you receive a command like "turn off the light" or "turn on the light", you should just indicate that you are doing as told.
"""
ollama.create(model="cortex", modelfile=modelfile)

def generate(question):
    message = {
            "role": "user",
            "content": question,
    }
    response = ollama.chat(model="cortex", messages=[message])
    return response