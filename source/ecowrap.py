import sys
import os
from StringIO import StringIO
import ecosystem
import subprocess


def run(tools, executable):
    # "backup" the current stdout
    stdout = sys.stdout

    # Create a StringIO for temporal stdout
    sys.stdout = ecostdout = StringIO()
    env = ecosystem.Environment(tools)

    # Restore the old stdout and get the output of ecosystem
    sys.stdout = stdout
    reason = ecostdout.getvalue().strip()

    if env.success:
        env.getEnv(os.environ)
        if not isinstance(executable, list):
            executable = [executable]
        subprocess.Popen(executable)
    else:
        raise RuntimeError(reason)
