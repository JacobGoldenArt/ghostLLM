from typing import List, Dict, cast
from openai_api.openai_base import OpenaiAPIBase


class OpenaiChatCompletion(OpenaiAPIBase):
    """A class for interacting with the OpenAI Chat API."""

    def __call__(self, user_input: str) -> str:
        self.history.add("user", user_input)
        last_turns = self.history.get_last(5)

        response = self.make_api_call(last_turns)
        bot_response = ""
        if response:
            choices = cast(List[Dict[str, Dict[str, str]]], response["choices"])
            bot_response = choices[0]["message"]["content"]
            self.history.add("assistant", bot_response)

        return bot_response
