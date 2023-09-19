from rich.table import Table
from rich import print


class CLI:
    @staticmethod
    def handle_verbose_output(
        verbose, full_history=None, api_response=None, user_input=None
    ):
        if verbose == "obj":
            print("API Response:", api_response)
        elif verbose == "thread":
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
