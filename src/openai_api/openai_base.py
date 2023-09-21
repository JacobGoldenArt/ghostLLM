import os
from typing import Dict, List, Optional, Union
import openai
from openai import ChatCompletion
import dotenv
from logs.handle_feedback import LLMfeedback
from memory.chat_history import History

dotenv.load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

class OpenaiAPIBase:
    """Base class for OpenAI API calls."""

    def __init__(self, sys: str, verbose: Optional[str] = None, temperature: float = 0.5, max_tokens: int = 200, model: str = "gpt-3.5-turbo") -> None:
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.model = model
        self.verbose = verbose
        self.history = History(sys, verbose)

    def make_api_call(self, last_turns: List[Dict[str, str]], additional_params: Optional[Dict[str, Union[str, int, float, List[Dict[str, str]]]]] = None) -> ChatCompletion:
        """Make an API call to OpenAI."""
        default_params = {
            "model": self.model,
            "messages": last_turns,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
        }

        if additional_params:
            default_params.update(additional_params)

        api_response = None
        try:
            api_response = openai.ChatCompletion.create(**default_params)
            LLMfeedback.handle_verbose_output(self.verbose, user_input=last_turns[-1]["content"], full_history=self.history.get_full_history())

        except openai.APIError as e:
            # Handle API error here, e.g. retry or log
            LLMfeedback.log_and_handle_errors(e, self.verbose, last_turns[-1]["content"], self.history.get_full_history())

        return api_response
