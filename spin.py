import time
from random import randint
from yaspin import yaspin
from yaspin.spinners import Spinners
from functools import wraps


class Color:
    class spin_color:
        black = "black"
        grey = "grey"
        red = "red"
        grey = "green"
        yellow = "yellow"
        blue = "blue"
        green = "green"
        magenta = "magenta"
        cyan = "cyan"
        lightgrey = "light_grey"
        dark_grey = "dark_grey"
        light_red = "light_red"
        light_green = "light_green"
        light_yellow = "light_yellow"
        light_blue = "light_blue"
        light_magenta = "light_magenta"
        light_cyan = "light_cyan"
        white = "white"

    class console_color:
        black = "\033[30m"
        red = "\033[31m"
        green = "\033[32m"
        yellow = "\033[33m"
        blue = "\033[34m"
        magenta = "\033[35m"
        cyan = "\033[36m"
        white = "\033[37m"
        reset = "\033[0m"


class SpinText:
    color = Color.console_color
    login={"text":"Fportal Login ...",
           "ok":f"{color.green}> Login Success {color.reset}",
           "fail":f"{color.red}> Login Failure {color.reset}"}
    scraping={"text":"Data scraping ...",
              "ok":f"{color.green}> Scraping Success {color.reset}",
              "fail":f"{color.red}> Scraping Failure {color.reset}"}
    post={"text":"Data posting ...",
        "ok":f"{Color.console_color.green}> Posting Done {Color.console_color.reset}"}


#classMethod
def spinner_method(spin_text):
    def decorator(method):
        @wraps(method)
        def wrapper(self, *args, **kwargs):
            with yaspin(text=spin_text["text"],side="right",
                        timer=True,color=Color.spin_color.yellow) as sp:
                result = method(self, *args, **kwargs)
                if result :
                    sp.text = spin_text["ok"]
                    sp.ok("✔")
                else:
                    sp.fail = spin_text["fail"]
                    sp.ok("✖")
            return result
        return wrapper
    return decorator


def spinner(spin_text):
    def decorator(method):
        @wraps(method)
        def wrapper(*args, **kwargs):
            with yaspin(text=spin_text["text"],side="right",
                        timer=True,color=Color.spin_color.yellow) as sp:
                result = method(*args, **kwargs)
                if result :
                    sp.text = spin_text["ok"]
                    sp.ok("✔")
                else:
                    sp.text = spin_text["fail"]
                    sp.fail("✖")
            return result
        return wrapper
    return decorator

def Sample():
    with yaspin(
        spinner=Spinners.earth,
        text="Fportal Login ...",
        side="right",
        timer=True,
        color=Color.spin_color.yellow,
    ) as sp:
        time.sleep(1)
        success = randint(0, 1)
        if success:
            sp.write(SpinText.login["ok"])
            sp.ok("✔")
        else:
            sp.write(SpinText.login["fail"])
            sp.fail("✔")

if __name__ == "__main__":
    pass