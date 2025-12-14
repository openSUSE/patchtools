"""
Run a command
"""

import subprocess

def run_command(command, stdin=None, our_input=None, stdout=subprocess.PIPE):
    with open("/dev/null", "w") as dn:
        proc = subprocess.run(command, shell=True, encoding='utf-8',
                              check=False,
                              stdin=stdin, input=our_input, stdout=stdout,
                              stderr=dn)
        return proc.stdout
