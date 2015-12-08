import sys
import os
from StringIO import StringIO
import ecosystem
import subprocess
import platform
import copy


def run(tools, executable):
    # "backup" the current stdout
    stdout = sys.stdout
    # "backup" the current environment
    envs = copy.deepcopy(os.environ)

    # Create a StringIO for temporal stdout and execute ecosystem
    sys.stdout = ecostdout = StringIO()
    env = ecosystem.Environment(tools)

    # Restore the old stdout and get the output of ecosystem
    sys.stdout = stdout
    reason = ecostdout.getvalue().strip()

    # If Ecosystem was successful, digest the arguments and execute them
    # If not, raise a RuntimeError. After any of them, restore the environment
    # variables from before updating them
    if env.success:
        env.getEnv(os.environ)
        if not isinstance(executable, list):
            executable = [executable]
        subprocess.Popen(executable, shell='win' in platform.system().lower())
        os.environ = envs
    else:
        os.environ = envs
        raise RuntimeError(reason)
