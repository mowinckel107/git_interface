from colored_text import *

import sys
import subprocess
from typing import Optional
from dataclasses import dataclass


@dataclass
class Git_Response:
    response_text: str
    return_code: int


VERBOSE : bool = False;

REPO_PATH : str


def set_repo_to_run_commands_on(repo_path : str):
    global REPO_PATH
    REPO_PATH = repo_path



def run_git_command( command_line : str, directory_to_call_from : Optional[str] = None ) -> Git_Response:
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



def git_command(command : str, quiet : bool = False, allowed_to_fail : bool = False) -> Git_Response:

    git_response : Git_Response = run_git_command(command, REPO_PATH)

    if quiet:
        return git_response

    print(f"command: {green_text(command)}")

    if VERBOSE:
        print(f"return code: {git_response.return_code}")

    print("git response:")
    if git_response.return_code == 0:
        print_text_yellow(git_response.response_text)
    else:
        if allowed_to_fail:
            print_text_yellow(git_response.response_text)
        else:
            print_text_red(git_response.response_text)

    print("")

    print("")
    print("")

    if(not allowed_to_fail and git_response.return_code is not 0):
        sys.exit(-1)

    return git_response


