import time
from random import randint
from yaspin import yaspin
from yaspin.spinners import Spinners


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


class Message:
    color = Color.console_color
    login_success = f"{color.green}> ✔ Login Success {color.reset}"
    login_failure = f"{color.red}> ✖ Login Failure {color.reset}"
    scraping_success = f"{color.green}> ✔ Scraping Success {color.reset}"
    scraping_failure = f"{color.red}> ✖ Scraping Failure {color.reset}"
    data_post_done = (
        f"{Color.console_color.green}> ✔ Posting Done {Color.console_color.reset}"
    )


def test_yaspin():
    with yaspin(
        text="Fportal Login ...",
        side="right",
        timer=True,
        color=Color.spin_color.yellow,
    ) as sp:
        time.sleep(1)
        success = randint(0, 1)
        if success:
            sp.write(Message.login_success)
        else:
            sp.write(Message.login_failure)

        sp.text = "Data scraping ..."
        time.sleep(2)
        success = randint(0, 1)
        if success:
            sp.write(Message.scraping_success)
        else:
            sp.write(Message.scraping_failure)

        # finalize
        sp.text = "Data posting ..."
        sp.spinner = Spinners.bouncingBar
        time.sleep(10)
        sp.write(Message.data_post_done)

        sp.text = "> complete it"
        sp.color = Color.spin_color.yellow
        sp.ok("✔")


test_yaspin()
