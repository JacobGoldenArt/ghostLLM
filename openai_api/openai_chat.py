from openai_api.openai_base import OpenaiAPIBase


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
