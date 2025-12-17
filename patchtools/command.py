"""
Run a command
"""

from subprocess import PIPE, run


def run_command(command, stdin=None, our_input=None, stdout=PIPE):
    with open("/dev/null", "w") as dn:
        proc = run(command, shell=True, encoding='utf-8', check=False,
                   stdin=stdin, input=our_input, stdout=stdout, stderr=dn)
        return proc.stdout
