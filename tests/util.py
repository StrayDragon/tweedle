import subprocess


def check_command_invokable(*commands) -> bool:
    for command in commands:
        result = subprocess.getstatusoutput(command)
        if 'not found' in result[1]:
            return True
    return False
