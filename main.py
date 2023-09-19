from rich.markdown import Markdown
from rich import print
from openai_api.openai_chat import OpenaiChatCompletion

# Usage with verbose mode on, "obj" for object or "thread" for full thread
my_chat = OpenaiChatCompletion(
    sys="You are a helpful assistant.", verbose="obj", temperature=0.6, max_tokens=30
)

while True:
    user_input = input("Write message here: ")
    chat_response = my_chat(user_input)
    print("[bold cyan]DarkMatterBot:[/bold cyan]")
    if isinstance(chat_response, str):
        print(Markdown(chat_response))
    else:
        print("Received an unsupported response type.")
