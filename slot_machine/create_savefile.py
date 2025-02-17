# Create a starter savefile for testing, can be done via game menu:
with open("slot_machine/savefile.txt", "w") as savefile:
    savefile.write(f"100.00\n0\n0\n0\n0\n0\n0\n0\n0\n0\n0\n1\n2\n0")

# For emojis (at 12,13):
    # [1] = grape
    # [2] = cookie
    # [3] = cherries
    # [4] = pineapple
    # [5] = mushroom

# SAVEFILE FORMULA:
# <user_balance>                    (user cash)[pos0]
# <easy_times_won>                  (how many times user won on easy)[pos2]
# <quadruple_times_won>             (how many times on quadruple)[pos3]
# <madness_times_won>               (how many times on madness)[pos4]
# <general_interval_level>          (general interval decrease lvl)[pos5]
# <loss_step_level>                 (loss stop lvl)[pos6]
# <am_upgrade_level>                (bonus money for wins lvl)[pos7]
# <user_prestige_level>             (prestige lvl)[pos8]
# <easy_odds_upgrade_level>         (odds upgrade for easy)[pos9]
# <quadruple_odds_upgrade_level>    (odds upgrade for quadruple)[pos10]
# <madness_odds_upgrade_level>      (odds upgrade for madness)[pos11]
# <prefslot1_tosave>                (PREFERRED REMOVED EMOJI FOR UPGRADE 1)[pos12]
# <prefslot2_tosave>                (PREFERRED REMOVED EMOJI FOR UPGRADE 2)[os13]
# <autofarm_tosave>                 (owns autofarm? 0/1)[pos14]
