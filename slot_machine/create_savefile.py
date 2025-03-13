# Create a starter savefile for testing, can be done via game menu:
with open("savefile.txt", "w") as savefile:
    savefile.write(f"100.00\n0\n0\n0\n0\n0\n0\n0\n0\n0\n0\n1\n2\n0\nY\nN")

# For emojis (at #12, #13):
    # "1" = grape
    # "2" = cookie
    # "3" = cherries
    # "4" = pineapple
    # "5" = mushroom

# SAVEFILE FORMULA:
# <user_balance>                    [pos1](user's cash)

# <easy_times_won>                  [pos2](how many times user won on easy)
# <quadruple_times_won>             [pos3](how many times on quadruple)
# <madness_times_won>               [pos4](how many times on madness)

# <eb_upgrade_level>                [pos7](bonus money for wins lvl)
# <loss_step_level>                 [pos6](loss stop lvl)
# <general_interval_level>          [pos5](general interval decrease lvl)

# <user_prestige_level>             [pos8](prestige lvl)

# <easy_odds_upgrade_level>         [pos9](odds upgrade lvl for easy)
# <quadruple_odds_upgrade_level>    [pos10](odds upgrade lvl for quadruple)
# <madness_odds_upgrade_level>      [pos11](odds upgrade lvl for madness)

# <prefslot1_tosave>                [pos12](preferred removed emoji from the slot machine at upgrade #1)
# <prefslot2_tosave>                [pos13](preferred removed emoji from the slot machine at upgrade #2)

# <autofarm_tosave>                 [pos14](owns autofarm? 0/1)

# <acc_key>                         [pos15](accept key in the y/n prompts)
# <dec_key>                         [pos16](decline key in the y/n prompts)
