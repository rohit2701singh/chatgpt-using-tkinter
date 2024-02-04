import os
from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPEN_AI_KEY"))

# ----------- chatgpt --------------

messages = [
    {"role": "system", "content": "You are a kind helpful assistant."},
]

while True:
    message = input("User : ")
    if message.lower() == "exit":
        break

    if message:
        messages.append({"role": "user", "content": message})
        chat = client.chat.completions.create(
            model="gpt-3.5-turbo", messages=messages
        )
    else:
        continue
    reply = chat.choices[0].message.content
    print(f"ChatGPT: {reply}")
    messages.append({"role": "assistant", "content": reply})

# ------------ image ----------------

response = client.images.generate(
    model="dall-e-2",
    prompt="Generate a visually captivating and aesthetically pleasing picture by blending vibrant colors, harmonious "
           "composition, intricate details, and evocative lighting that captures the viewer's imagination",
    size="1024x1024",
    quality="standard",
    n=1,
)
image_url = response.data[0].url
print(f"url: {image_url}")
