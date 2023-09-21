import logging
from typing import List, Dict, Tuple, Optional
from rich.table import Table
from rich import print as rprint

error_logger = logging.getLogger("error_logger")

#Define a new type for messages
Message = Dict[str, str]
#Define a new type for the history
History = List[Message]

class LLMfeedback:
    """A class for formatting any errors or logging output from the LLM or User Settings"""

    @staticmethod
    def provide_feedback(msg: str) -> None:
        """Provide feedback based on verbose mode."""
        rprint(f"[bold blue]{msg}[/bold blue]")

    @staticmethod
    def log_and_handle_errors(e: BaseException, verbose: Optional[str], user_input: str, full_history: History, msg: Optional[str]=None) -> None:
        """Log errors and handle them based on verbose mode."""
        error_logger.error("An error occurred: %s", e)
        if msg:
            # print the extra message if provided
            rprint(f"[bold red]{msg}[/bold red]")
        LLMfeedback.handle_verbose_output(verbose, user_input=user_input, full_history=full_history)

    @staticmethod
    def handle_verbose_output(verbose: Optional[str], user_input: str, full_history: History, msg: Optional[str]=None) -> None:
        """Handle verbose output based on verbose mode."""
        if verbose is None:
            return
        if verbose == "obj":
            rprint("User Input:", user_input)
            if msg:
                # print the extra message if provided
                rprint(f"[bold blue]{msg}[/bold blue]")
        elif verbose == "thread":
            LLMfeedback.print_verbose_output(full_history)

    @staticmethod
    def print_verbose_output(full_history: History) -> None:
        table = Table(title="API Response")
        table.add_column("Role")
        table.add_column("Content")

        for message in full_history:
            role, content = message["role"], message["content"]
            role_style, content_style = LLMfeedback.get_styles_for_role(role)
            table.add_row(f"[{role_style}]{role}[/]", f"[{content_style}]{content}[/]")

            rprint(table)

    @staticmethod
    def get_styles_for_role(role: str) -> Tuple[str, str]:
        if role == "system":
            return "bold yellow", "yellow"
        elif role == "user":
            return "bold green", "green"
        else:  # role is 'assistant'
            return "bold blue", "blue"
