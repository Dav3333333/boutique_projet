from datetime import datetime


def convert_user_string(string: str):
    if "_" in string:
        ret_string = [s for s in string]
        new_string = ""
        for s in ret_string:
            if s != "_":
                new_string += s
            else:
                new_string += "*"
        return new_string
    else:
        return string


def get_user_string(string):
    string = str(string)
    if "*" in string:
        ret_string = [s for s in string]
        new_string = ""
        for s in ret_string:
            if s != "*":
                new_string += f"{s}"
            else:
                new_string += "_"
        return new_string
    else:
        return string


def dateDuJour():
    """
    :return: this function return the date of the actual day in string format
    """
    return datetime.now().strftime("%d/%m/%Y")


def is_not_empty_string(*args:str) -> bool:
    for a in args:
        if a.strip() == "":
            return False
    return True


