



import sys
import subprocess
from typing import Optional
from dataclasses import dataclass


@dataclass
class Git_Response:

    # Attributes Declaration
    # using Type Hints
    response_text: str
    return_code: int


def run_git_command( command_line : str, directory_to_call_from : Optional[str] = None) -> Git_Response:
    """Runs git command, returns output and status code."""

    command : list[str] = command_line.split()

    response_object : subprocess.CompletedProcess[bytes]= subprocess.run(
        command,
        check = False,
        capture_output = True,
        cwd = directory_to_call_from
    )

    return_string : str = response_object.stdout.decode("utf-8")
    return_string += response_object.stderr.decode("utf-8")

    return Git_Response(return_string, response_object.returncode)

