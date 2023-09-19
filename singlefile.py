import os
import logging
from rich import print
from rich.table import Table
from rich.markdown import Markdown
import openai
import dotenv

dotenv.load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

error_logger = logging.getLogger("error_logger")


class CLI:
    @staticmethod
    def handle_verbose_output(
        verbose, full_history=None, api_response=None, user_input=None
    ):
        if verbose == "resp":
            print("Full API Response:", api_response)
        elif verbose == "user_msg":
            print("User Message:", user_input)
        elif verbose == "all":
            CLI.print_verbose_output(full_history)

    @staticmethod
    def print_verbose_output(full_history):
        table = Table(title="API Response")
        table.add_column("Role")
        table.add_column("Content")

        for message in full_history:
            role, content = message["role"], message["content"]
            role_style, content_style = CLI.get_styles_for_role(role)
            table.add_row(f"[{role_style}]{role}[/]", f"[{content_style}]{content}[/]")

        print(table)

    @staticmethod
    def get_styles_for_role(role):
        if role == "system":
            return "bold yellow", "yellow"
        elif role == "user":
            return "bold green", "green"
        else:  # role is 'assistant'
            return "bold blue", "blue"


class OpenaiAPIBase:
    def __init__(
        self, sys, verbose=None, temperature=0.5, max_tokens=200, model="gpt-3.5-turbo"
    ):
        self.sys = sys
        self.verbose = verbose
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.model = model
        self.full_history = [{"role": "system", "content": self.sys}]

    def log_and_handle_errors(self, e, user_input):
        error_logger.error("An error occurred: %s", e)
        CLI.handle_verbose_output(self.verbose, user_input=user_input)

    def make_api_call(self, last_turns, additional_params=None):
        default_params = {
            "model": self.model,
            "messages": last_turns,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
        }

        if additional_params:
            default_params.update(additional_params)

        try:
            api_response = openai.ChatCompletion.create(**default_params)
            CLI.handle_verbose_output(
                self.verbose,
                full_history=self.full_history,
                api_response=api_response,
                user_input=last_turns[-1]["content"] if last_turns else None,
            )
            return api_response
        except Exception as e:
            self.log_and_handle_errors(
                e, last_turns[-1]["content"] if last_turns else None
            )


class OpenaiChatCompletion(OpenaiAPIBase):
    """A class for interacting with the OpenAI Chat API."""

    def __call__(self, user_input):
        self.full_history.append({"role": "user", "content": user_input})
        last_turns = self.full_history[-5:]

        response = self.make_api_call(last_turns)
        if response:
            bot_response = response["choices"][0]["message"]["content"]
            self.full_history.append({"role": "assistant", "content": bot_response})
            return bot_response


# Usage with verbose mode on
my_chat = OpenaiChatCompletion(
    sys="You are a helpful assistant.",
    verbose="all",
    temperature=0.6,
    max_tokens=150,
    model="gpt-4",
)

while True:
    user_input = input("Write message here: ")
    chat_response = my_chat(user_input)
    print("[bold cyan]DarkMatterBot:[/bold cyan]")
    if isinstance(chat_response, str):
        print(Markdown(chat_response))
    else:
        print("Received an unsupported response type.")
