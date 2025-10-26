

from git_interface_library import *


import sys
import subprocess
from typing import Optional
from dataclasses import dataclass





def main_function():

    repo_path : str =  "/home/moose/Desktop/Code/Python/git_interface"

    command : str = "git branch"
    git_response : Git_Response = run_git_command(command, repo_path)
    print(command)
    print(git_response.return_code)
    print(git_response.response_text)

    print("All done. ")




if __name__ == "__main__":
    main_function()
