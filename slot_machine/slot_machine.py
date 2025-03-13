import random as ran
import threading
import signal
import atexit
import msvcrt
import time
import os

from debug import *


# hi, thanks for looking onto my project
# I love making slightly advanced stuff out of pure garbage and silly ideas


# GENERAL VARIABLES (be cautious):
user_balance = 100.00
slot_contents = ["🍪", "🍇", "🍄", "🍒", "🍍"]
game_mode = "easy"
slot_rolled = []
slot_range = 3
display_main_menu = True
KEY_MINIGAME_PRIZE_MONEY = 1.70
pref_removed_slot1 = None
pref_removed_slot2 = None
owns_autofarm = False
acc_key = "Y"
dec_key = "N"

# ============== INFORMATION ==============

# General cash rewards formulas:
    # Easy:
    #   4,00% BWR
    #   (135.00 + (eb_upgrade_amount * difficulty) + (times_won * difficulty)) * prestige_multiplier
    # Quadruple:
    #   0,80% BWR
    #   (615.00 + (eb_upgrade_amount * difficulty) + (times_won * difficulty)) * prestige_multiplier
    # Madness:
    #   0,16% BWR
    #   (2435.00 + (eb_upgrade_amount * difficulty) + (times_won * difficulty)) * prestige_multiplier



# GENERAL WIN RATE STATISTICS AND EXPLANATIONS:
#   Variables:
#       a = amount of slot_contents (emojis available based on upgrade tier)
#       s = amount of slots
#   Formula:
#       win_chance = (s(a^s))*100 %

# Easy:
#   Rules:  Hit 3, 5 total contents => 5^3 = 125, 5/125 = 4.00%  #0
#           Hit 3, 4 total contents => 4^3 = 64, 4/64 = 6.25%    #1
#           Hit 3, 3 total contents => 3^3 = 9, 3/27 = 11.11%    #2
#           Hit 3, 2 total contents => 2^3 = 8, 2/8 = 25.00%     #3 // Unimplemented, too overpowered.
# that looks freaking ridiculous, 25%?, maybe change the rewards for the games? absurd amounts!! what in the fuck? (i dont know what i've written here, i dont think i actually implemented that kinda buff)

# Quadruple:
#   Rules:  Hit 4, 5 total contents => 5^4 = 625, 5/625 = 0.8000%
#           Hit 4, 4 total contents => 4^4 = 256, 4/256 = 1.5625%
#           Hit 4, 3 total contents => 3^4 = 81, 3/81 = 3.7037%
#           Hit 4, 2 total contents => 2^4 = 16, 2/16 = 12.5000% // Unimplemented, too overpowered.

# Madness:
#   Rules:  Hit 5, 5 total contents => 5^5 = 3125, 5/3125 = 0.16%
#           Hit 5, 4 total contents => 4^5 = 1024, 4/1024 = 0.39%
#           Hit 5, 3 total contents => 3^5 = 243, 3/243 = 1.23%
#           Hit 5, 2 total contents => 2^5 = 32, 2/32 = 6.25% // Unimplemented, too overpowered.



easy_odds_upgrade_level = 0
quadruple_odds_upgrade_level = 0
madness_odds_upgrade_level = 0
easy_odds_display = {
    0 : 4.00,
    1 : 6.25,
    2 : 11.11
}
quadruple_odds_display = {
    0 : 0.80,
    1 : 1.56,
    2 : 3.70
}
madness_odds_display = {
    0 : 0.16,
    1 : 0.39,
    2 : 1.23
}

# (Costs)
easy_odds_upgrades = {
    1 : 3501.00,
    2 : 75057.00
}
quadruple_odds_upgrades = {
    1 : 64420.00,
    2 : 350030.00
}
madness_odds_upgrades = {
    1 : 250222.00,
    2 : 750390.00
}



# Prestige Multipliers (+0.30x reward per Prestige):
    # #1 - 1.30x reward
    # #2 - 1.60x reward
    # ...
    # #9 - 3.70x reward
    # #10 = win game condition // hella expensive but hella big multiplier for fun.
user_prestige_level = 0
prestige_multipliers = {
    0 : 1.00,
    1 : 1.30,
    2 : 1.60,
    3 : 1.90,
    4 : 2.20,
    5 : 2.50,
    6 : 2.80,
    7 : 3.10,
    8 : 3.40,
    9 : 3.70,
    10: 11.00
}
prestige_costs = {
    # Easy-based Stage:
    1 : 1200,
    2 : 8500,
    3 : 22500,
    # Quadruple-based Stage:
    4 : 64500,
    5 : 105300,
    6 : 145000,
    7 : 215000,
    # Madness-based Stage:
    8 : 435000,
    9 : 650500,
    10 : 25000000
}



# Autofarms (prestige_level : autofarm_cost):
autofarm_on = False
autofarm_costs = {
    0 : 2500,
    1 : 2500,
    2 : 3250,
    3 : 3250,
    4 : 4000,
    5 : 4500,
    6 : 5150,
    7 : 6000,
    8 : 7500,
    9 : 8550,
}



# Times Won Bonus:
easy_times_won = 0
quadruple_times_won = 0
madness_times_won = 0
easy_times_won_multiplier = easy_times_won * 1.00            # previously 0.75, 0.65
quadruple_times_won_multiplier = quadruple_times_won * 22.00 # previously 1.15, 3.75
madness_times_won_multiplier = madness_times_won * 955.00    # previously 1.65



# Extra Bucks Upgrade:
    # eb_easy_multiplier        = 1.00x
    # eb_quadruple_multiplier   = 15.00x
    # eb_madness_mulitplier     = 35.00x
eb_upgrade_level = 0
extra_bucks_upgrade_value = (42.7*(eb_upgrade_level)**2)
ebu_costs = {
    # P0
    1 : 50.00,   
    2 : 98.70,
    # P1
    3 : 244.80, 
    4 : 488.30,  
    5 : 829.20,
    # P2 
    6 : 1267.50, 
    7 : 1803.20, 
    8 : 2436.30,
    # P3
    9 : 3166.80, 
    10 : 3994.70,
    11 : 4920.00,
    12 : 5942.70,
    # P4
    13 : 7062.80,
    14 : 8280.30,
    15 : 9595.20,
    # P5
    16 : 11007.50,
    17 : 12517.20,
    18 : 14124.30,
    # P6
    19 : 15828.80,
    20 : 17630.70,
    21 : 19530.00,
    # P7
    22 : 21526.70,
    23 : 23620.80,
    24 : 25812.30,
    # P8
    25 : 28101.20,
    26 : 30487.50,
    27 : 32971.20,
    28 : 35552.30,
    # P9
    29 : 38230.80,
    30 : 41006.70,
}



# Loss Decrease:
    # UPG0  -> 1.00 * game_cost 
    # UPG1  -> 0.97 * game_cost
    # UPG20 -> 0.40 * game_cost
loss_stop_level = 0
loss_stop_level_factor = 1 - loss_stop_level * 0.03
ls_costs = {
    1 : 25.00,
    2 : 37.70,
    3 : 75.80,
    # P1
    4 : 139.30,
    5 : 228.20,
    # P2
    6 : 342.50,
    7 : 330.20,
    # P3
    8 : 482.30,
    9 : 837.80,
    # P4
    10 : 1053.70,
    11 : 1295.00,
    # P5
    12 : 1561.70,
    13 : 1853.80,
    # P6
    14 : 2171.30,
    15 : 2514.20,
    # P7
    16 : 2882.50,
    17 : 3276.20,
    # P8
    18 : 3695.30,
    # P9
    19 : 4139.80,
    20 : 4609.70
}



# General Interval:
    # UPG0  -> 2.50s
    # UPG1  -> 2.25s
    # UPG10 -> 0.25s
general_interval_level = 0
general_interval_factor = 2.75 - (general_interval_level * 0.25)
gi_costs = {
    1 : 55.00,
    2 : 66.00,
    3 : 99.00,
    4 : 154.00,
    5 : 231.00,
    6 : 330.00,
    7 : 451.00,
    8 : 594.00,
    9 : 759.00,
    10 : 946.00
}



def begin_tutorial(skip_tuts=False):

    if skip_tuts == True:
        return
    
    os.system("cls")

    str_input = input("👀 Hello! Welcome to my simple Python Slot Machine game.\n\nIn this game you spin the slot machine with a decent chance of winning\nbuy upgrades, autofarms and better odds for winning!\n\nPress Enter to continue!")
    os.system("cls")
    str_input = input("The chances for wins on each difficulty are following:\nEasy -> 4.00%\nQuadruple -> 0.80%\nMadness -> 0.16%\n\nYou can buy upgrades to make it easier!")
    os.system("cls")
    str_input = input("Your goal is to prestige every time you get a certain amount of cash\nand with every prestige you will gain some cash buffs so your game feels faster each time.")
    os.system("cls")
    str_input = input("Each game costs a bit of money 💸, so you will need to spend some cash in order to win more cash, got it?\nHere are the costs for each difficulty:\n\n🟢 Easy -> 2.50$\n🟡 Quadruple -> 6.75$\n🔴 Madness -> 12.50$\n\n")
    os.system("cls")
    str_input = input("🌟 You've got the basics now, get out there and show the world gambling's worth it!\nPress Enter to start..")

    return


def show_balance(**kwargs):

    global gambled_right
    global slot_rolled
    
    if kwargs.get("just_won") == True:
        print(f"💲 Your new balance: ${user_balance:.2f} 💲\n\n")
        gambled_right = 0
        slot_rolled.clear()
        time.sleep(1.00)
        os.system("cls")
        return
    
    else:
        os.system("cls")
        print(f"💖 Your balance: ${user_balance:.2f} 💸\n\n")
        time.sleep(1.00)
        os.system("cls")
        return


def save_on_exit():
    save_data_to_savefile()


def client_settings():
    global pref_removed_slot1
    global pref_removed_slot2

    global acc_key
    global dec_key

    while True:

        os.system("cls")
        print("🥪 Client Settings 🌮\n")
        str_input = input(f"\n💡 Pick an action:\n\n\t🔃 [1] -> Reset Savefile\n\t⭕ [2] -> Content Removal Preferences\n\t📝 [3] -> Save Game\n\t🆎 [4] -> Confirmation Binds\n\t⏪ [5] -> Return\n\n")

        if str_input.upper() == "1":
            os.system("cls")
            print(f"\n\nAre you sure ❓ This action cannot be undone. ({acc_key}/{dec_key})\n\n")
            str_input = input()

            if str_input.upper() == acc_key:

                print(f"\n\n⚠ Last warning 💢 There is no going back. {acc_key}/{dec_key})\n\n")
                str_input = input()

                if str_input.upper() == acc_key:

                    overwrite_savefile_with_default_data()

                else:
                    return   
                
            else:
                return
        
        elif str_input.upper() == "2":
            os.system("cls")
            print("🍄 SLOT MACHINE EMOJIS 🍬\n")
            print("\tCustomize which emojis you'd like to be removed\n\tfrom the slot machine upon certain upgrades.\n\n")
            print(f"> Currect preferences: {pref_removed_slot1} , {pref_removed_slot2}\n\n")
            print("[1] -- 🍍\n[2] -- 🍒\n[3] -- 🍄\n[4] -- 🍇\n[5] -- 🍪\n[6] -- Return\n\n")
            
            while True:
                str_input = input("Pick removed emoji #1: ")

                match str_input:
                    case "1":
                        pref_removed_slot1 = "🍍"
                        break
                    case "2":
                        pref_removed_slot1 = "🍒"
                        break
                    case "3":
                        pref_removed_slot1 = "🍄"
                        break
                    case "4":
                        pref_removed_slot1 = "🍇"
                        break
                    case "5":
                        pref_removed_slot1 = "🍪"
                        break
                    case "6":
                        return
                    case _:
                        print("❌ Invalid input!")
                        time.sleep(2)
                        os.system("cls")
                        continue
                
            while True:
                str_input = input("Pick emoji #2: ")

                match str_input:
                    case "1":
                        if str_input == pref_removed_slot1:
                            print("❌ Already taken!")
                            continue
                        else:
                            pref_removed_slot2 = "🍍"
                            break
                    case "2":
                        if str_input == pref_removed_slot1:
                            print("❌ Already taken!")
                            continue
                        else:
                            pref_removed_slot2 = "🍒"
                            break
                    case "3":
                        if str_input == pref_removed_slot1:
                            print("❌ Already taken!")
                            continue
                        else:
                            pref_removed_slot2 = "🍄"
                            break
                    case "4":
                        if str_input == pref_removed_slot1:
                            print("❌ Already taken!")
                            continue
                        else:
                            pref_removed_slot2 = "🍇"
                            break
                    case "5":
                        if str_input == pref_removed_slot1:
                            print("❌ Already taken!")
                            continue
                        else:
                            pref_removed_slot2 = "🍪"
                            break
                    case "6":
                        return
                    case _:
                        print("❌ Invalid input!")
                        time.sleep(2)
                        os.system("cls")
                        continue

            while True:
                str_input = input("⭐ Awesome! Would you like to save your game? ({acc_key}/{dec_key}): ")

                if str_input.upper() == "Y":
                    save_data_to_savefile()
                    return
                elif str_input.upper() == "N":
                    return
                else:
                    print("❌ Please enter a valid input.")
                    time.sleep(1.2)
                    os.system("cls")
                    continue

        elif str_input.upper() == "3":
            save_data_to_savefile()
            print(f"Data saved! ✅ Press any key to continue.")
            str_input = input()
            return

        elif str_input.upper() == "4":
            os.system("cls")
            print("🔑 CHANGE CONFIRMATION KEYS 💫\n")
            print("\tSwap out Y/N confirmation Keys to your liking\n\n")
            print(f"> Currect preferences: {acc_key} / {dec_key}\n\n")
            while True:
                acc_key = str(input(">> Accept Key: ").upper())
                dec_key = str(input(">> Decline Key: ").upper())
                if (dec_key == "" or dec_key == None or acc_key == None or acc_key == ""):
                    print("Empty keys? You must set them to something!")
                    continue
                if (dec_key == acc_key):
                    print("You cannot have the same key bound to both accept and decline!")
                    continue
                
                print("All set ✅ Have fun!")
                return

        elif str_input.upper() == "5":
            break

        else:
            print("❌ Invalid input!")
            time.sleep(1.0)
            os.system("cls")
            continue

    return


def overwrite_savefile_with_default_data():
    global user_balance
    global easy_times_won
    global quadruple_times_won
    global madness_times_won
    global eb_upgrade_level
    global loss_stop_level
    global general_interval_level
    global user_prestige_level
    global easy_odds_upgrade_level
    global quadruple_odds_upgrade_level
    global madness_odds_upgrade_level
    global pref_removed_slot1
    global pref_removed_slot2
    global owns_autofarm
    global acc_key
    global dec_key

    global game_mode
    global extra_bucks_upgrade_value
    global loss_stop_level_factor
    global general_interval_factor
    global easy_times_won_multiplier
    global quadruple_times_won_multiplier
    global madness_times_won_multiplier
    global autofarm_on

    with open("savefile.txt", "w") as savefile:
        game_mode = "easy"
        general_interval_level = 0
        general_interval_factor = 2.75 * (general_interval_level * 0.25)
        loss_stop_level = 0
        loss_stop_level_factor = 1 - loss_stop_level * 0.03
        eb_upgrade_level = 0
        extra_bucks_upgrade_value = 48.7*(eb_upgrade_level)**2
        easy_times_won = 0
        quadruple_times_won = 0
        madness_times_won = 0
        easy_times_won_multiplier = easy_times_won * 1.00
        quadruple_times_won_multiplier = quadruple_times_won * 22.00
        madness_times_won_multiplier = madness_times_won * 955.00
        owns_autofarm = False
        user_prestige_level = 0
        
        easy_odds_upgrade_level = 0
        quadruple_odds_upgrade_level = 0
        madness_odds_upgrade_level = 0
        user_balance = 100.00
        autofarm_on = False
        acc_key = "Y"
        dec_key = "N"
        pref_removed_slot1 = "🍪"
        pref_removed_slot2 = "🍇"
        savefile.write(f"100.00\n0\n0\n0\n0\n0\n0\n0\n0\n0\n0\n1\n2\n0\nY\nN")
        
    savefile.close()

    return


def save_data_to_savefile():

    # Handle emoji writing to .txt:
    match pref_removed_slot1:
        case "🍇":
            prefslot1_tosave = "1"
        case "🍪":
            prefslot1_tosave = "2"
        case "🍒":
            prefslot1_tosave = "3"
        case "🍍":
            prefslot1_tosave = "4"
        case "🍄":
            prefslot1_tosave = "5"
        case _:
            print("Savedata's prefemoji1 variable corrupted, cannot save.")
    
    match pref_removed_slot2:
        case "🍇":
            prefslot2_tosave = "1"
        case "🍪":
            prefslot2_tosave = "2"
        case "🍒":
            prefslot2_tosave = "3"
        case "🍍":
            prefslot2_tosave = "4"
        case "🍄":
            prefslot2_tosave = "5"
        case _:
            print("Savedata's prefemoji2 variable corrupted, cannot save.")

    if owns_autofarm == True:
        autofarm_tosave = "1"
    else:
        autofarm_tosave = "0"

    with open("savefile.txt", "w") as savefile:
        savefile.write(f"{user_balance}\n{easy_times_won}\n{quadruple_times_won}\n{madness_times_won}\n{general_interval_level}\n{loss_stop_level}\n{eb_upgrade_level}\n{user_prestige_level}\n{easy_odds_upgrade_level}\n{quadruple_odds_upgrade_level}\n{madness_odds_upgrade_level}\n{prefslot1_tosave}\n{prefslot2_tosave}\n{autofarm_tosave}\n{acc_key}\n{dec_key}")

    savefile.close()


def read_data_from_savefile():
    global user_balance
    
    global easy_times_won
    global quadruple_times_won
    global madness_times_won

    global easy_times_won_multiplier
    global quadruple_times_won_multiplier
    global madness_times_won_multiplier

    global general_interval_level
    global general_interval_factor

    global loss_stop_level
    global loss_stop_level_factor
    
    global eb_upgrade_level
    global extra_bucks_upgrade_value
    
    global user_prestige_level

    global easy_odds_upgrade_level
    global quadruple_odds_upgrade_level
    global madness_odds_upgrade_level

    global pref_removed_slot1
    global pref_removed_slot2

    global owns_autofarm

    global acc_key
    global dec_key

    with open("savefile.txt", "r") as savefile:

        line_values = savefile.readlines()

        user_balance = float(line_values[0].strip())

        easy_times_won = int(line_values[1])
        easy_times_won_multiplier = easy_times_won * 1.00

        quadruple_times_won = int(line_values[2])
        quadruple_times_won_multiplier = quadruple_times_won * 22.00

        madness_times_won = int(line_values[3])
        madness_times_won_multiplier = madness_times_won * 955.00

        general_interval_level = int(line_values[4])
        general_interval_factor = 2.75 - (general_interval_level * 0.25)

        loss_stop_level = int(line_values[5])
        loss_stop_level_factor = 1 - loss_stop_level * 0.03

        eb_upgrade_level = int(line_values[6])
        extra_bucks_upgrade_value = float(42.7*(eb_upgrade_level)**2)

        user_prestige_level = int(line_values[7])

        easy_odds_upgrade_level = int(line_values[8])
        quadruple_odds_upgrade_level = int(line_values[9])
        madness_odds_upgrade_level = int(line_values[10])

        match line_values[11].strip():
            case "1":
                pref_removed_slot1 = "🍇" 
            case "2":
                pref_removed_slot1 = "🍪"
            case "3":
                pref_removed_slot1 = "🍒"
            case "4":
                pref_removed_slot1 = "🍍"
            case "5":
                pref_removed_slot1 = "🍄"
            case _:
                print("read_data_from_savefile() malfunctioning, I recommend checking for index errors") 
        
        match line_values[12].strip():
            case "1":
                pref_removed_slot2 = "🍇"
            case "2":
                pref_removed_slot2 = "🍪"
            case "3":
                pref_removed_slot2 = "🍒"
            case "4":
                pref_removed_slot2 = "🍍"
            case "5":
                pref_removed_slot2 = "🍄"
            case _:
                print("read_data_from_savefile() malfunctioning, I recommend checking for index errors") 

        if line_values[13] == "1":
            owns_autofarm = True
        else:
            owns_autofarm = False

        acc_key = str(line_values[14]).strip()
        dec_key = str(line_values[15]).strip()

    savefile.close()


def recover_chance_sequence():
    os.system("cls")
    print(f"Uh oh!")
    time.sleep(2.3)
    os.system("cls")
    print(f"Looks like you've gambled it all away", end="")
    
    time.sleep(0.8)
    for x in range(4):
        print(".", end="", flush=True)
        time.sleep(0.8)

    time.sleep(1.8)
    os.system("cls")
    print("But..!")
    time.sleep(2.5)
    os.system("cls")
    print("Luckily, we've got a chance for recovery just for you! Your beloved Key-Sequence game!")
    time.sleep(4.5)
    os.system("cls")
    print("Don't waste your chance!")
    time.sleep(0.8)
    init_key_minigame(about_to_lose = True)


def gameloss():
    # When in the fuck will you encounter this? I don't even think you can legit lose the game unless you're at the very beginning and manage money poorly.
    os.system("cls")
    print("\nFUCKING HELL!!!!! You're out of 💲💲💲, looks like you've lost. 👺\n\n")
    print("> If you still wish to continue playing from your last save, please reboot the game.")
    exit()


def init_key_minigame(**kwargs):
    global user_balance
    global KEY_MINIGAME_PRIZE_MONEY


    def get_user_input_with_timeout(timeout=2.5):
        user_input = [None]

        def read_input():
            user_input[0] = input("\n>>> ")

        input_thread = threading.Thread(target=read_input)
        input_thread.start()
        input_thread.join(timeout)

        if input_thread.is_alive():
            print("\n\n⏳ Time's over!!")
            return None
        
        return user_input[0]


    os.system("cls")

    print("🎭 Python Key-Sequence Game ✨")
    if kwargs.get("about_to_lose") != True:
        print(f"\t💰 Prize: ${KEY_MINIGAME_PRIZE_MONEY:.2f}")

    print("\n")

    # Pick five random characters from the sequence:
    keys = ("abcdefghijklmnopqrstuvwxyz")
    picked_keys = [ran.choice(keys) for _ in range(5)]

    # Display the keys:
    print("👉 Repeat this sequence:")
    print("  ".join(picked_keys).upper())

    # Read user input within the time limit
    user_input = get_user_input_with_timeout(2.5)

    # Check if the input was correct, and if not then return
    if user_input is None or list(user_input.lower()) != picked_keys:
        print("❌ You've lost! 😭\nDouble-Press Enter to confirm...")
        user_input = input()
        os.system("cls")
        picked_keys.clear()
        user_balance -= 2.50

        if user_balance <= 2.50:
            gameloss()
        else:
            return
    
    # Win condition
    print("\n\n🎉 Congrats! You've won the minigame!")
    print(f"\t💰 Amount of ${KEY_MINIGAME_PRIZE_MONEY:.2f} has been added to your account!!")
    time.sleep(2.0)
    os.system("cls")
    picked_keys.clear()
    user_balance += KEY_MINIGAME_PRIZE_MONEY
    return


def display_upgrade_shop():
    global user_balance

    global general_interval_level
    global general_interval_factor

    global loss_stop_level
    global loss_stop_level_factor
    
    global eb_upgrade_level
    global extra_bucks_upgrade_value
    
    global easy_times_won
    global quadruple_times_won
    global madness_times_won

    global user_prestige_level

    global easy_odds_upgrade_level
    global quadruple_odds_upgrade_level
    global madness_odds_upgrade_level

    global owns_autofarm

    global easy_times_won_multiplier
    global quadruple_times_won_multiplier
    global madness_times_won_multiplier

    global game_mode

    global autofarm_on
    
    global acc_key
    global dec_key

    while True:

        os.system("cls")

        print(f"⭐ UPGRADES ⭐")
        print(f"${user_balance:.2f}\n")
        print(f"\t[1] = Raise Additional Win Funds [{eb_upgrade_level}] : [+${extra_bucks_upgrade_value:.2f}] \t💸 -> [${ebu_costs.get(eb_upgrade_level+1):.2f}] : [+${(48.7*(eb_upgrade_level+1)**2):.2f}]\n", end="") if eb_upgrade_level <= 29 else print(f"\t[1] = Raise Additional Win Funds [{eb_upgrade_level}] : [+${extra_bucks_upgrade_value:.2f}] \t💸 -> [MAXED] : [MAXED]\n", end="")
        #print(f"\t[1] = Raise Additional Win Funds [{eb_upgrade_level}] : [+${extra_bucks_upgrade_value:.2f}] \t💸 -> [${ebu_costs.get(eb_upgrade_level+1):.2f}] : [+${extra_bucks_upgrade_value + 2.50:.2f}]\n", end="")
        print(f"\t[2] = Decrease Money Loss [{loss_stop_level}] : [{loss_stop_level_factor*100:.2f}%] \t\t📉 -> [${ls_costs.get(loss_stop_level+1):.2f}] : [{(loss_stop_level_factor-0.03)*100:.2f}%]\n", end="") if loss_stop_level <= 19 else print(f"\t[2] = Decrease Money Loss [{loss_stop_level}] : [{loss_stop_level_factor*100:.2f}%] \t\t📉 -> [MAXED] : [MAXED]\n", end="")
        #print(f"\t[2] = Decrease Money Loss [{loss_stop_level}] : [{loss_stop_level_factor*100:.2f}%] \t\t📉 -> [${ls_costs.get(loss_stop_level+1):.2f}] : [{(loss_stop_level_factor-0.04)*100:.2f}%]\n", end="")
        print(f"\t[3] = Decrease General Interval [{general_interval_level}] : [{general_interval_factor:.2f}s] \t\t⌛ -> [${gi_costs.get(general_interval_level+1):.2f}] : [{general_interval_factor-0.25:.2f}s]\n", end="") if general_interval_level <= 9 else print(f"\t[3] = Decrease General Interval [{general_interval_level}] : [{general_interval_factor:.2f}s] \t\t⌛ -> [MAXED] : [MAXED]\n", end="")
        #print(f"\t[3] = Decrease General Interval [{general_interval_level}] : [{general_interval_factor:.2f}s] \t\t⌛ -> [${gi_costs.get(general_interval_level+1):.2f}] : [{general_interval_factor-0.25:.2f}s]\n", end="")
        print(f"\t[4] = Increase Difficulty Win Odds\t\t\t🏆")
        print(f"\t[5] = Autofarm\t\t\t\t\t\t🍤")
        print(f"\t[6] = Prestige [{user_prestige_level}] : [{prestige_multipliers.get(user_prestige_level):.2f}x] \t\t\t\t✨ -> [${prestige_costs.get(user_prestige_level+1):.2f}] : [{prestige_multipliers.get(user_prestige_level+1):.2f}x]\n\n", end="")
        print(f"\t[7] = Return ⏪\n\n", end="")
        str_input = input()

        # Extra Bucks Upgrade (EBU):
        if str_input == "1":
            if eb_upgrade_level == 30:
                print("❎ Your 'Extra Bucks Upgrade' has already been maxed!\n\tPress any key to return.")
                str_input = input()
                return
            else:
                if user_balance >= ebu_costs.get(eb_upgrade_level + 1):
                    print("🎇 Upgraded 'Bonus Money'! 🎇")
                    user_balance -= ebu_costs.get(eb_upgrade_level + 1)
                    eb_upgrade_level += 1
                    extra_bucks_upgrade_value = (48.7*(eb_upgrade_level-1)**2) + 50
                    time.sleep(1.5)
                    while True:
                        os.system("cls")
                        print(f"📝 Would you like to save your game? ({acc_key}/{dec_key}): ", end="")
                        str_input = input()
                        if str_input.upper() == "Y":
                            save_data_to_savefile()
                            os.system("cls")
                            return    
                        elif str_input.upper() == "N":
                            return
                        else:
                            print("Please pick a valid option.")
                            time.sleep(1.5)
                            continue
                else:
                    print("❌ Not enough money. ❌")
                    time.sleep(1.5)
                    os.system("cls")
                    continue
        # Loss Stop Decrease (LSD):
        if str_input == "2":
            if loss_stop_level == 20:
                print("❎ Your 'Loss Stop Decrease' has already been maxed!\n\tPress any key to return.")
                str_input = input()
                return
            else:
                if user_balance >= ls_costs.get(loss_stop_level + 1):
                    print("🎇 Upgraded 'Money Loss Decrease'! 🎇")
                    user_balance -= ls_costs.get(loss_stop_level + 1)
                    loss_stop_level += 1
                    loss_stop_level_factor = 1 - loss_stop_level * 0.04
                    time.sleep(1.5)
                    while True:
                        os.system("cls")
                        print("📝 Would you like to save your game? ({acc_key}/{dec_key}): ", end="")
                        str_input = input()
                        if str_input.upper() == "Y":
                            os.system("cls")
                            save_data_to_savefile()
                            return
                        elif str_input.upper() == "N":
                            return
                        else:
                            print("Please pick a valid option.")
                            time.sleep(1.5)
                            continue
                else:
                    print("❌ Not enough money. ❌")
                    time.sleep(1.5)
                    os.system("cls")
                    continue
        # General Interval Decrease (GID):
        if str_input == "3":
            if general_interval_level == 10:
                print("❎ Your 'General Interval Decrease' has already been maxed!\n\tPress any key to return.")
                str_input = input()
                return
            else:
                if user_balance >= gi_costs.get(general_interval_level + 1):
                    print("🎇 Upgraded 'General Interval Decrease'! 🎇")
                    user_balance -= gi_costs.get(general_interval_level + 1)
                    general_interval_level += 1
                    general_interval_factor = 2.75 - (general_interval_level * 0.25)
                    time.sleep(1.5)
                    while True:
                        os.system("cls")
                        print("📝 Would you like to save your game? ({acc_key}/{dec_key}): ", end="")
                        str_input = input()
                        if str_input.upper() == "Y":
                            os.system("cls")
                            save_data_to_savefile()
                            return
                        elif str_input.upper() == "N":
                            os.system("cls")
                            return
                        else:
                            print("Please pick a valid option.")
                            time.sleep(1.5)
                            continue
                else:
                    print("❌ Not enough money. ❌")
                    time.sleep(1.5)
                    os.system("cls")
                    continue
        # Upgrade Odds:
        if str_input == "4":
            os.system("cls")
            print("⭐ Choose difficulty odds to boost ✨\n")
            print(f"\t[1] -> Easy \t [{easy_odds_upgrade_level}] = [{easy_odds_display.get(easy_odds_upgrade_level):.2f}%]\t\t[{easy_odds_upgrade_level+1}] = [{easy_odds_display.get(easy_odds_upgrade_level+1):.2f}%] : [${easy_odds_upgrades.get(easy_odds_upgrade_level+1):.2f}]") if easy_odds_upgrade_level <= 1 else print(f"\t[1] -> Easy \t [{easy_odds_upgrade_level}] = [{easy_odds_display.get(easy_odds_upgrade_level):.2f}%]\t\t[{easy_odds_upgrade_level+1}] = [MAXED] : [MAXED]")
            print(f"\t[2] -> Quadruple [{quadruple_odds_upgrade_level}] = [{quadruple_odds_display.get(quadruple_odds_upgrade_level):.2f}%]\t\t[{quadruple_odds_upgrade_level+1}] = [{quadruple_odds_display.get(quadruple_odds_upgrade_level+1):.2f}%] : [${quadruple_odds_upgrades.get(quadruple_odds_upgrade_level+1):.2f}]") if quadruple_odds_upgrade_level <= 1 else print(f"\t[2] -> Quadruple [{quadruple_odds_upgrade_level}] = [{quadruple_odds_display.get(quadruple_odds_upgrade_level):.2f}%]\t\t[{quadruple_odds_upgrade_level+1}] = [MAXED] : [MAXED]")
            print(f"\t[3] -> Madness \t [{madness_odds_upgrade_level}] = [{madness_odds_display.get(madness_odds_upgrade_level):.2f}%]\t\t[{madness_odds_upgrade_level+1}] = [{madness_odds_display.get(madness_odds_upgrade_level+1):.2f}%] : [${madness_odds_upgrades.get(madness_odds_upgrade_level+1):.2f}]") if madness_odds_upgrade_level <= 1 else print(f"\t[3] -> Madness \t [{madness_odds_upgrade_level}] = [{madness_odds_display.get(madness_odds_upgrade_level):.2f}%]\t\t[{madness_odds_upgrade_level+1}] = [MAXED] : [MAXED]")
            print(f"\n\t[4] -> Return ⏪\n\n")

            str_input = input()

            while True:

                if str_input == "1":
                    if easy_odds_upgrade_level == 2:
                        print("❎ Your 'EASY Odds Upgrade' has already been maxed!\n\tPress any key to return.")
                        str_input = input()
                        return
                    else:
                        if user_balance >= easy_odds_upgrades.get(easy_odds_upgrade_level+1):
                            user_balance -= easy_odds_upgrades.get(easy_odds_upgrade_level+1)
                            easy_odds_upgrade_level += 1
                            print("Upgraded! 🔥")
                            time.sleep(1.3)
                            while True:
                                os.system("cls")
                                print("📝 Would you like to save your game? ({acc_key}/{dec_key}): ", end="")
                                str_input = input()
                                if str_input.upper() == "Y":
                                    save_data_to_savefile()
                                    return
                                elif str_input.upper() == "N":
                                    return
                                else:
                                    print("Please pick a valid option.")
                                    time.sleep(1.5)
                                    continue
                        else:
                            print("❌ Not enough money!")
                            time.sleep(1.5)
                            return              
                elif str_input == "2":
                    if quadruple_odds_upgrade_level == 2:
                        print("❎ Your 'QUADRUPLE Odds Upgrade' has already been maxed!\n\tPress any key to return.")
                        str_input = input()
                        return
                    else:
                        if user_balance >= quadruple_odds_upgrades.get(quadruple_odds_upgrade_level+1):
                            user_balance -= quadruple_odds_upgrades.get(easy_odds_upgrade_level+1)
                            quadruple_odds_upgrade_level += 1
                            print("Upgraded! 🔥🔥")
                            while True:
                                os.system("cls")
                                print("📝 Would you like to save your game? ({acc_key}/{dec_key}): ", end="")
                                str_input = input()
                                if str_input.upper() == "Y":
                                    save_data_to_savefile()
                                elif str_input.upper() == "N":
                                    return
                                else:
                                    print("Please pick a valid option.")
                                    time.sleep(1.5)
                                    continue
                        else:
                            print("❌ Not enough money!")
                            time.sleep(1.5)
                            return
                elif str_input == "3":
                    if madness_odds_upgrade_level == 2:
                        print("❎ Your 'MADNESS Odds Upgrade' has already been maxed!\n\tPress any key to return.")
                        str_input = input()
                        return
                    else:
                        if user_balance >= madness_odds_upgrades.get(madness_odds_upgrade_level+1):
                            user_balance -= madness_odds_upgrades.get(madness_odds_upgrade_level+1)
                            madness_odds_upgrade_level += 1
                            print("Upgraded! 🔥🔥🔥")
                            time.sleep(1.3)
                            while True:
                                os.system("cls")
                                print("📝 Would you like to save your game? ({acc_key}/{dec_key}): ", end="")
                                str_input = input()
                                if str_input.upper() == "Y":
                                    save_data_to_savefile()
                                elif str_input.upper() == "N":
                                    return
                                else:
                                    print("Please pick a valid option.")
                                    time.sleep(1.5)
                                    continue
                        else:
                            print("❌ Not enough money!")
                            time.sleep(1.5)
                            return
                elif str_input == "4":
                    return
                else:
                    print("❌ Invalid input.")
                    time.sleep(1.2)
                    continue
        # Autofarm Ability Upgrade:
        if str_input == "5":
            if owns_autofarm != True:
                os.system("cls")
                print(f"💳 Autofarm cost: [${autofarm_costs.get(user_prestige_level)}]")
                if user_balance < autofarm_costs.get(user_prestige_level):
                    print(f"\n❌ You cannot afford the autofarm. Press any key to continue. ❌")
                    str_input = input()
                    return
                else:
                    while True:
                        str_input = input("Would you like to purchase the Autofarm Ability module? ({acc_key}/{dec_key}): ")
                        if str_input.upper() == "Y":
                            user_balance -= autofarm_costs.get(user_prestige_level)
                            owns_autofarm = True
                            print("\nAutofarm purchased! Congratulations! 🎉🎉")
                            time.sleep(2.0)
                            
                            while True:
                                os.system("cls")
                                print("📝 Would you like to save your game? ({acc_key}/{dec_key}): ", end="")
                                str_input = input()
                                if str_input.upper() == "Y":
                                    save_data_to_savefile()
                                    return
                                elif str_input.upper() == "N":
                                    return
                                else:
                                    print("Please pick a valid option.")
                                    time.sleep(1.5)
                                    continue

                        elif str_input.upper() == "N":
                            print(f"Returning...")
                            time.sleep(1.0)
                            return
                        else:
                            print("❌ Invalid input.")
                            time.sleep(1.0)
                            continue
                    
            else:
                os.system("cls")
                print(f"✅ You already own an autofarm! You can turn it on in Client Settings menu!\n")
                str_input = input("Any key to return. ")
                return
        # User Prestige:
        if str_input == "6":
            if user_prestige_level == 10:
                os.system("cls")
                print("🌟 You've already reached the maximum prestige level! Congratulations!")
                time.sleep(3.5)
                return
            
            if user_balance >= prestige_costs.get(user_prestige_level + 1):

                while True:
    
                    os.system("cls")
                    str_input = input("🌟 Are you sure you want to prestige? This action cannot be undone. ({acc_key}/{dec_key}): ")

                    if str_input.upper() == "Y":
                        time.sleep(2.2)
                        os.system("cls")
                        print("😍 CONGRATULATIONS! You successfully prestiged! 😎")
                        print(f"You're now prestige {user_prestige_level+1}! ... and gained x{1+((user_prestige_level+1)*0.30):.2f} cash boost!!")
                        
                        game_mode = "easy"
                        general_interval_level = 0
                        general_interval_factor = 2.75 * (general_interval_level * 0.25)
                        loss_stop_level = 0
                        loss_stop_level_factor = 1 - loss_stop_level * 0.03
                        eb_upgrade_level = 0
                        extra_bucks_upgrade_value = 48.7*(eb_upgrade_level)**2
                        easy_times_won = 0
                        quadruple_times_won = 0
                        madness_times_won = 0
                        easy_times_won_multiplier = easy_times_won * 1.00
                        quadruple_times_won_multiplier = quadruple_times_won * 22.00
                        madness_times_won_multiplier = madness_times_won * 955.00
                        owns_autofarm = False
                        user_prestige_level = 0
                        
                        easy_odds_upgrade_level = 0
                        quadruple_odds_upgrade_level = 0
                        madness_odds_upgrade_level = 0
                        user_balance = 100.00
                        autofarm_on = False
                        acc_key = "Y"
                        dec_key = "N"

                        save_data_to_savefile()
                        time.sleep(6)
                        return
                    
                    elif str_input.upper() == "N":
                        return
                    
                    else:
                        print("❌ Invalid input.")
                        time.sleep(1.5)
                        continue
            else:
                print("❌ Not enough money. ❌")
                time.sleep(1.5)
                os.system("cls")
                continue
        # Return to main menu:
        if str_input == "7":
            return
        # Invalid input:
        else:
            print("❌ Invalid input.")
            time.sleep(1.0)
            continue


def change_game_settings():
    global game_mode
    global autofarm_on

    while True:
        os.system("cls")
        print("💖 Python Slot Machine Settings 🏆\n\n\t⭐ [1] -- Set gamemode\n\t⚡ [2] -- Autofarm\n\t⏪ [3] -- Return")
        str_input = input()
        if str_input.upper() == "1":
            os.system("cls")
            print(f"\n🔥 Currect gamemode: {game_mode.upper()} 🔥\n")
            print("🎭 Set gamemode:\n\n\t[1] - Easy\n\t[2] - Quadruple\n\t[3] - Madness\n")
            str_input = input()

            if str_input == "1":
                game_mode = "easy"
                print("✅ Gamemode set to Easy!")
                time.sleep(1.5)
                os.system("cls")
                break
            elif str_input == "2":
                game_mode = "quadruple"
                print("✅ Gamemode set to Quadruple!!")
                time.sleep(1.5)
                os.system("cls")
                break
            elif str_input == "3":
                game_mode = "madness"
                print("✅ Gamemode set to Madness!!!")
                time.sleep(1.5)
                os.system("cls")
                break
            else:
                print("❌ Invalid Input.")
                time.sleep(2)
                os.system("cls")
                continue
        elif str_input.upper() == "2":
            while True:
                if owns_autofarm == True:
                    os.system("cls")
                    str_input = input(f"\n💎 Would you like to enable Autofarm Module? ({acc_key}/{dec_key}): ")

                    if str_input.upper() == "Y":
                        autofarm_on = True
                        print("\n✅ Autofarm ENABLED!!!")
                        time.sleep(1.2)
                        return
                    elif str_input.upper() == "N":
                        autofarm_on = False
                        print("\n❌ Autofarm DISABLED!")
                        time.sleep(0.5)
                        return
                    else:
                        print("\n❌ Invalid input.")
                        time.sleep(1.0)
                        continue
                else:
                    print(f"❌ You don't own an autofarm yet! You can purchse one in the Upgrade Shop!")
                    time.sleep(3.0)
                    return
        elif str_input.upper() == "3":
            return
        else:
            print("❌ Invalid input.\n\n")
            time.sleep(0.75)
            os.system("cls")
            continue

    return


def spin():
    global user_balance

    global slot_contents
    global slot_range
    global slot_rolled
    global game_mode
    
    global easy_times_won
    global quadruple_times_won
    global madness_times_won
    global easy_times_won_multiplier
    global quadruple_times_won_multiplier
    global madness_times_won_multiplier

    global general_interval_level
    global general_interval_factor

    global loss_stop_level
    global loss_stop_level_factor
    
    global eb_upgrade_level
    global extra_bucks_upgrade_value
    
    global user_prestige_level

    global owns_autofarm
    global autofarm_on


    def get_user_input_with_timeout(timeout=0.75):
        print("\n>>> ", end='', flush=True)
        start_time = time.time()

        while time.time() - start_time < timeout:
            if msvcrt.kbhit():
                return msvcrt.getch().decode('utf-8')

        print("\n\n⏳ Time's over!!")
        return None


    while True:
        os.system("cls")
        gambled_right = 0

        # Remove a defined amount of slots from the set:
        if game_mode == "madness":

            if madness_odds_upgrade_level == 1:
                slot_contents.remove(pref_removed_slot1)
                # print("m1:", slot_contents)
                # time.sleep(2)
                
            elif madness_odds_upgrade_level == 2:
                slot_contents.remove(pref_removed_slot1)
                slot_contents.remove(pref_removed_slot2)
                # print("m2:", slot_contents)
                # time.sleep(2)

        if game_mode == "quadruple":

            if quadruple_odds_upgrade_level == 1:
                slot_contents.remove(pref_removed_slot1)
                # print("q1:", slot_contents)
                # time.sleep(2)

            elif quadruple_odds_upgrade_level == 2:
                slot_contents.remove(pref_removed_slot1)
                slot_contents.remove(pref_removed_slot2)
                # print("q2:", slot_contents)
                # time.sleep(2)

        if game_mode == "easy":

            if easy_odds_upgrade_level == 1:
                slot_contents.remove(pref_removed_slot1)
                # print("e1:", slot_contents)
                # time.sleep(2)

            elif easy_odds_upgrade_level == 2:
                slot_contents.remove(pref_removed_slot1)
                slot_contents.remove(pref_removed_slot2)
                # print("e2:", slot_contents)
                # time.sleep(2)

        # Pick the random slots rolled:
        for x in range(slot_range):
            slot_rolled.append(ran.choice(slot_contents))

        # Print out rolled elements:
        print("| ", end="")
        for x in range(slot_range):
            print(f"{slot_rolled[x]} | ", end="")
        print("\n")

        # Reset slot_contents for set flexibility functionality:
        slot_contents[:] = ["🍪", "🍇", "🍄", "🍒", "🍍"]

        # Check if user actually won:
        for element in slot_rolled:

            if (element == slot_rolled[0]):
                gambled_right += 1

            else:
                print("❌ You lost! ❌")
                slot_rolled.clear()
                gambled_right = 0

                if slot_range == 3:
                    user_balance -= 2.50 * loss_stop_level_factor

                elif slot_range == 4:
                    user_balance -= 6.75 * loss_stop_level_factor

                elif slot_range == 5:
                    user_balance -= 12.50 * loss_stop_level_factor

                else:
                    print(f"Gamemode variable: {game_mode} was corrupted during runtime. Check for grammatical spelling mistakes in the source code.")

                print(f"Loser! Better luck next time. Balance: ${user_balance:.2f}")

                if user_balance <= 0.00:
                    time.sleep(4)
                    can_roll = ran.randint(0, 100)
                    if can_roll <= 80:
                        recover_chance_sequence()
                    else:
                        gameloss()

                time.sleep(general_interval_factor)
                os.system("cls")

        if gambled_right == slot_range:
            print("🏆 You win! 🏆")

            if slot_range == 3:
                earned_money = (135.00 + (extra_bucks_upgrade_value * 1.00) + easy_times_won_multiplier) * prestige_multipliers.get(user_prestige_level)
                print(f"Amount of ${earned_money:.2f} has been added to your balance!")
                easy_times_won += 1
                easy_times_won_multiplier = easy_times_won * 0.15
                user_balance += earned_money
                time.sleep(general_interval_factor)
                os.system("cls")
                show_balance(just_won=True)
                time.sleep(1)

            elif slot_range == 4:
                earned_money = (615.00 + (extra_bucks_upgrade_value * 15.00) + quadruple_times_won_multiplier) * prestige_multipliers.get(user_prestige_level)
                print(f"Amount of ${earned_money:.2f} has been added to your balance!!")
                quadruple_times_won += 1
                quadruple_times_won_multiplier = quadruple_times_won * 4.00
                user_balance += earned_money
                time.sleep(general_interval_factor)
                os.system("cls")
                show_balance(just_won=True)
                time.sleep(1)

            elif slot_range == 5:
                earned_money = (2435.00 + (extra_bucks_upgrade_value * 35.00) + madness_times_won_multiplier) * prestige_multipliers.get(user_prestige_level)
                print(f"Amount of ${earned_money:.2f} has been added to your balance!!!")
                madness_times_won += 1
                madness_times_won_multiplier = madness_times_won * 22.00
                user_balance += earned_money
                time.sleep(general_interval_factor)
                os.system("cls")
                show_balance(just_won=True)
                time.sleep(1)

            else:
                print(f"Game_mode: {game_mode}, variable corrupted. No cash was awarded.")
                exit()

        if autofarm_on and owns_autofarm:
            disable_autofarm_input = get_user_input_with_timeout(0.75)
            if disable_autofarm_input is None:
                continue
            else:
                break
        else:
            break

    return


def game_setup():
    global slot_rolled
    global game_mode
    global slot_range
    global display_main_menu
    global slot_contents

    display_main_menu = False

    # Set range for given game_mode
    if game_mode == "madness":
        slot_range = 5
        spin()

    elif game_mode == "quadruple":
        slot_range = 4    
        spin()

    elif game_mode == "easy":
        slot_range = 3
        spin()

    else:
        print(f"Gamemode variable: {game_mode} was corrupted during runtime. Please check for errors or grammatical errors.")

    return


signal.signal(signal.SIGINT, save_on_exit)   # CTRL+C in terminal
signal.signal(signal.SIGTERM, save_on_exit)  # Kill <PID>
atexit.register(save_on_exit)                # Standard exit    


def main():
    global display_main_menu
    global user_balance
    global game_mode

    while True:
        
        # For unrepetitive sentences, misleading variable name, that should be "mainmenudisplay" countering the "spin again?" prompt:
        if display_main_menu:
            os.system("cls")
            print("\n⭐ Python Slot Machine ⭐\n")
            str_input = input(f"\n💡 Pick an action:\n\n\t🌟 [1] -> Play\n\t🏓 [2] -> Minigame\n\t😎 [3] -> Upgrade\n\t👿 [4] -> Difficulty & Modules\n\t💵 [5] -> Balance\n\t🍏 [6] -> Saving & Settings\n\t⏪ [7] -> Exit\n\n")

            if str_input.upper() == "1":
                game_setup()
            
            elif str_input.upper() == "2":
                init_key_minigame(about_to_lose = False)
                
            elif str_input.upper() == "3":
                display_upgrade_shop()

            elif str_input.upper() == "4":
                change_game_settings()

            elif str_input.upper() == "5":
                show_balance(just_won=False)

            elif str_input.upper() == "6":
                client_settings()

            elif str_input.upper() == "7":
                print("💛 Have a nice day! 💸")
                save_data_to_savefile()
                exit()

            # elif str_input.upper() == "8":
            #     DEBUG_VARIABLEDUMP()
            #     continue

            # elif str_input.upper() == "9":
            #     DEBUG_ADDCASH()
            #     str_input = input("Added $1000.00, press to continue.")
            #     continue

            else:
                print("❌ Invalid input.\n\n")
                time.sleep(0.75)
                os.system("cls")
                continue

        else:
            str_input = input(f"\n💯 Spin again? ({acc_key}/{dec_key}): ")

            if str_input.upper() == "Y":
                game_setup()

            elif str_input.upper() == "N":
                display_main_menu = True
                os.system("cls")
                continue

            else:
                print("❌ Invalid input. ({acc_key}/{dec_key})\n\n")
                time.sleep(1)
                os.system("cls")


if __name__ == "__main__":
    try:
        with open("savefile.txt") as savefile:
            pass

    except FileNotFoundError:
        overwrite_savefile_with_default_data()
        begin_tutorial()

    read_data_from_savefile()
    main()