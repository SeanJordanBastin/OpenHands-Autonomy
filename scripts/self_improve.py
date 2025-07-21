import openai
from dotenv import load_dotenv
import os

load_dotenv()

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def ask_gpt(question):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You're helping an AI agent improve its own code."},
            {"role": "user", "content": question}
        ]
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    q = "Why did my agent fail to apply Alembic migration?"
    print(ask_gpt(q))

