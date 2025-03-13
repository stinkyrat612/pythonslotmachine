# Functions used for debugging maingame.py:

def DEBUG_ADDCASH():
    # I only slide this function in for testing, don't abuse please.
    global user_balance
    user_balance += 1000


def DEBUG_VARIABLEDUMP():
    globals_dump = globals()
    for var_name, value in globals_dump.items():
        print(f"{var_name}: {value}\n\n")
    str_input = input(f"Dumped. Press enter to continue.")


if __name__ == "__main__":
    print("Do not run this program directly, it's a library for maingame.py")
    exit()