import ollama
import numpy as np
import duckdb

conn = duckdb.connect("./embeddings.ddb")
conn.execute("CREATE SEQUENCE IF NOT EXISTS id START 1")
conn.execute("CREATE TABLE IF NOT EXISTS embeddings (id INT, document VARCHAR, embedding FLOAT[])")

context_length = 2

def find_most_similar(needle, haystack):
    needle_norm = np.linalg.norm(needle)
    similarity_scores = [(np.dot(needle, item[0][1]) / (needle_norm * np.linalg.norm(item[0][1])), item[0][0]) for item in haystack]
    return sorted(similarity_scores, reverse=True)

def append_embeddings(prompt, response):
    serialized_convo = f"{prompt}|{response}"
    embedding = ollama.embeddings("nomic-embed-text", prompt=serialized_convo)["embedding"]
    conn.execute("INSERT INTO embeddings VALUES (nextval('id'), ?, ?)", [serialized_convo, embedding])

def generate(prompt):
    embeddings = conn.execute("SELECT (id, embedding) FROM embeddings").fetchall()

    system_message = f"""
        Your name is Cortex.
        You should always give reasonably short answers.
        When you receive a command like "turn off the light" or "turn on the light", you should just indicate that you are doing as told.
    """

    context = [{"role": "system", "content": system_message}]

    if len(embeddings) > 0:
        prompt_embedding = ollama.embeddings("nomic-embed-text", prompt=prompt)["embedding"]
        most_similar_chunks = find_most_similar(prompt_embedding, embeddings)[:context_length]
        
        for chunk in most_similar_chunks:
            document = conn.execute("SELECT document FROM embeddings WHERE id = ?", [chunk[1]]).fetchall()[0][0].split("|")
            print(document)
            context.append({"role": "user", "content": document[0]})
            context.append({"role": "assistant", "content": document[1]})

    context.append({"role": "user", "content": prompt})

    response = ollama.chat(model="llama3.1:8b-instruct-q4_0", messages=context)

    append_embeddings(prompt=prompt, response=response["message"]["content"])

    return response["message"]["content"]

while True:
    prompt = input("You: ")
    response = generate(prompt)
    print("Bot:", response)