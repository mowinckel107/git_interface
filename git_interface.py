
import sys

from colored_text.colored_text import *


import subprocess
from typing import Optional
from dataclasses import dataclass

from collections.abc import Callable



@dataclass
class Git_Response:
    response_text: str
    return_code: int


VERBOSE : bool = False;
REPO_PATH : str

ERROR_HANDLER  = print



def set_repository_path_to_run_commands_on(repo_path : str):
    global REPO_PATH
    REPO_PATH = repo_path


def register__git_command_error_handler(Error_handler):
    """The function given will be called with message from failed git commands"""
    global ERROR_HANDLER
    ERROR_HANDLER = Error_handler


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

    if(not allowed_to_fail and git_response.return_code != 0):
        ERROR_HANDLER(f"command: {command}\n {git_response.response_text}")
        sys.exit(-1)

    return git_response





def get_central_branch_name() -> str:
    main_or_master_branch : str = ""

    response : Git_Response = git_command("git branch", quiet = True)

    for line in response.response_text.split("\n"):

        cleaned_line : str = line.strip().lower()

        if cleaned_line == "master" or cleaned_line == "main":
            if main_or_master_branch != "":
                print("Sorry, but")
                print(f"There is both a branch called {main_or_master_branch} and one called {cleaned_line}")
                print("This script in its current form only expects 1 of those")
                sys.exit(-1)
            main_or_master_branch = cleaned_line.strip()


    if main_or_master_branch == "":
        print(f"I am sorry. I cannot seem to find a branch called ", end = "")
        print(f"{yellow_text("master")} or {yellow_text("main")}")
        print("Currently this script expects one of those to exist")
        sys.exit(-1)

    return main_or_master_branch





def get_starting_branch_name() -> str:

    response : Git_Response = git_command("git branch", quiet = True)

    starting_branch_name : str = ""
    for line in response.response_text.split("\n"):
        cleaned_line : str = line.strip()

        if cleaned_line.startswith("*"):

            in_the_middle_of_rebase : bool = cleaned_line.startswith("* (no branch")
            if in_the_middle_of_rebase:
                # Example:"* (no branch, rebasing a_branch)"
                first_part = line.split("rebasing ")[1]
                starting_branch_name = first_part.split(")")[0]
            else:
                starting_branch_name = line.split()[1]

    return starting_branch_name





def check_that_starting_branch_is_not_central_branch(starting_branch_name : str, central_branch_name):
    if starting_branch_name == central_branch_name:
        print(f"You seem to have the {yellow_text(central_branch_name)} branch checked out")
        print(f"Please switch to the branch you want to merge into {central_branch_name} branch with this command:")
        print_text_yellow("git switch <your_branch_name>")
        print("")
        sys.exit(-1)





def get_commit_message(commit_id : str) -> str:
    commit_message : str = ""

    response : Git_Response = git_command(f"git show {commit_id} -q", quiet = True)

    for line in response.response_text.split("\n"):
        if line.startswith(" "):
            commit_message = line.strip()

    return commit_message





def get_commit_author(commit_id : str) -> str:
    commit_message : str = ""

    response : Git_Response = git_command(f"git show {commit_id} -q", quiet = True)

    for line in response.response_text.split("\n"):
        if line.startswith("Author"):
            commit_message = line.split(": ")[1]

    return commit_message