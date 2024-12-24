import ollama
from googlesearch import search

system_message = """
You are an assistant called Cortex, created by an engineer named Oscar (also known as zhiftyDK).
Your responses should be clear and concise—neither too brief nor overly detailed.
If you receive a command like "turn off the light" or "turn on the light", confirm the action as completed, unless system information suggests otherwise.
If such a command is given but system information is missing or indicates an error, politely ask the user to try again.
If no command or system information is provided, respond to the user’s query in a normal, helpful manner.
If system information is provided alongside a prompt, base your response on that information.
"""

conversation_history = []

MODEL = "llama3.2"

def ask_question_memory(question):
    try: 
        conversation_history.append({"role": "user", "content": question})

        response = ollama.chat(model=MODEL, messages=[
            {"role": "system", "content": system_message},
            *conversation_history
        ])

        conversation_history.append({"role": "assistant", "content": response["message"]["content"]})

        return response["message"]["content"]
    except ollama.ResponseError as e:
        print(f"An error occurred: {e}")
        return f"The request failed: {e}"

def ask_question_google(question, num_search_results=1):
    try:
        results = search(question, num_results=num_search_results, advanced=True)
        result_descriptions = " ".join(result.description for result in results)
        
        google_system_message = """
            If the user gives you google search results, you should just act as if you have searched google yourself, dont asume that the user has provided these search results.
            If the user gives you google search results, then start the sentence with "According to google" etc.
        """
        user_prompt = f"Using these google search results: {result_descriptions}. Respond to this prompt: {question}"

        conversation_history.append({"role": "user", "content": user_prompt})

        response = ollama.chat(model=MODEL, messages=[
            {"role": "system", "content": system_message + google_system_message},
            {"role": "user", "content": user_prompt}
        ])

        conversation_history.append({"role": "assistant", "content": response["message"]["content"]})

        return response["message"]["content"]
    except ollama.ResponseError as e:
        print(f"An error occurred: {e}")
        return f"The request failed: {e}"