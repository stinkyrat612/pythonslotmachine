# Functions used for debugging maingame.py:

def DEBUG_ADDCASH():
    # I only slide this function in for testing, don't abuse please.
    global user_balance
    user_balance += 1000


if __name__ == "__main__":
    print("Do not run this program directly, it's a library for maingame.py")
    exit()