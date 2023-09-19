import os
import logging
from cli.formater import CLI
import openai
import dotenv

dotenv.load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

error_logger = logging.getLogger("error_logger")


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
