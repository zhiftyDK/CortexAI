import ollama

modelfile="""
FROM llama3.1
SYSTEM Your name is Cortex. You should always give reasonably short answers.
"""
ollama.create(model="cortex", modelfile=modelfile)

def generate(question):
    message = {
            "role": "user",
            "content": question,
    }
    response = ollama.chat(model="cortex", messages=[message])
    return response