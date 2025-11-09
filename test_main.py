
from colored_text.colored_text import *
from git_interface import *


import sys
import subprocess
from typing import Optional
from dataclasses import dataclass

import os
from pathlib import Path



def main_function():

  file_path : str = os.path.dirname(__file__)
  print(file_path)

  register_git_command_error_handler(print)

  set_repository_path_to_run_commands_on(file_path)

  central_branch_name : str = get_central_branch_name()



  repo_path : str =  "/home/moose/Desktop/Code/Python/git_interface"



  git_command("git branch")

  print("All done. ")




if __name__ == "__main__":
    main_function()
