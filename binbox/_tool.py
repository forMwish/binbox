def command_clear(command:str):
    # \n\t 替换为空格
    command = command.replace("\n", " ").replace("\t", " ")
    command = " ".join(command.split())
    return command
