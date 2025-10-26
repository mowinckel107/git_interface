
from colored_text.colored_text  import *
from git_interface import *


import sys
import subprocess
from typing import Optional
from dataclasses import dataclass





def main_function():

  register__git_command_error_handler(print)


  repo_path : str =  "/home/moose/Desktop/Code/Python/git_interface"
  set_repository_path_to_run_commands_on(repo_path)

  git_command("git branch")

  print("All done. ")




if __name__ == "__main__":
    main_function()
