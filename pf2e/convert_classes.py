"""
Converts a directory of Pathfinder 2e classes, each in a separate JSON file,
into markdown files. Based on https://github.com/Pf2eToolsOrg/Pf2eTools.git format.
I'm specifically using it with Obsidian.MD alongside TTRPG-Convert-CLI
(https://github.com/ebullient/ttrpg-convert-cli), which does not import classes.

Author: github.com/lfknudsen
"""

import json
import glob

files = glob.glob("D:\\TTRPGs\\ttrpg-convert-cli-2.2.3-windows-x86_64\\bin\Pf2eTools\\data\\class\\class-*.json")
file_count = 0

def remove_trailing_comma(input_string):
    return input_string.rsplit(",", 1)[0]

def format_entry(input_text):
    output_text = input_text.replace("\u2014", " - ")
    return output_text

def convert_prof_initial(initial):
    match initial:
        case "U":
            return "Untrained in "
        case "T":
            return "Trained in "
        case "E":
            return "Expert in "
        case "M":
            return "Master in "
        case "L":
            return "Legendary in "

def format_adv_lvl_list(key):
    advancement_lvls = adv[key]
    lvl_list = ""
    for level in advancement_lvls:
        lvl_list += str(level) + ", "
    return remove_trailing_comma(lvl_list) + "\n"

for file in files:
    data = "---\nobsidianUImode: preview\ncssclasses: pf2e,pf2e-class\ntags:\n- compendium/src/pf2e/"
    with open(file, mode="r") as opened_file:
        try:
            obj = json.load(opened_file)
        except:
            print(file + " could not decode.")

        pf_class = obj["class"][0]
        data += pf_class["source"].lower()
        data += "\naliases: [\""
        data += pf_class["name"]
        data += "\"]\n---\n# "
        data += pf_class["name"]
        data += "\n"
        data += format_entry(str(pf_class["flavor"][0])) + "\n\n"
        data += "## HP\n" + str(pf_class["hp"]) + " + CON modifier\n"
        data += "## Key Ability\n" + pf_class["keyAbility"] + "\n"
        data += "## Proficiencies\n"
        profs = pf_class["initialProficiencies"]
        data += "### Perception\n"
        data += convert_prof_initial(profs["perception"]) + "Perception\n"
        data += "### Saving Throws\n"
        data += convert_prof_initial(profs["fort"]) + "Fortitude\n"
        data += convert_prof_initial(profs["ref"]) + "Reflex\n"
        data += convert_prof_initial(profs["will"]) + "Will\n"
        skills = profs["skills"]
        data += "### Skills\n"
        try:
            trained_skills = skills["t"]
            for skill_obj in trained_skills:
                try:
                    entry = skill_obj["entry"]
                    data += "Trained in " + entry + "\n"
                except:
                    if len(skill_obj["skill"]) == 1:
                        data += "Trained in " + skill_obj["skill"][0] + "\n"
                    else:
                        data += "Trained in your choice of either:\n"
                        for choice in skill_obj["skill"]:
                            data += "    " + choice + "\n"
        except:
            pass
        try:
            expert_skills = skills["e"]
            for skill_obj in expert_skills:
                data += "Expert in " + skill_obj["skill"][0] + "\n"
        except:
            pass
        try:
            add = skills["add"]
            data += "Trained in an additional " + str(add) + " + INT modifier\n"
        except:
            pass

        data += "### Attacks\n"
        attacks = profs["attacks"]
        try:
            t_array = attacks["t"]
            for t_obj in t_array:
                data += "Trained in " + t_obj + "\n"
        except:
            pass

        try:
            e_array = attacks["e"]
            for e_obj in e_array:
                data += "Expert in " + e_obj + "\n"
        except:
            pass

        data += "### Defenses\n"
        defenses = profs["defenses"]
        try:
            t_array = defenses["t"]
            for t_obj in t_array:
                data += "Trained in " + t_obj + "\n"
        except:
            pass

        try:
            e_array = defenses["e"]
            for e_obj in e_array:
                data += "Expert in " + e_obj + "\n"
        except:
            pass

        try:
            class_dc = profs["classDc"]["entry"]
            data += "### Class DC\n" + class_dc + "\n"
        except:
            pass

        try:
            spells = profs["spells"]
            t_arr = spells["t"]
            data += "### Spells\n"
            for t_obj in t_arr:
                data += "Trained in " + t_obj + "\n"
        except:
            pass

        data += "## Advancement\n"
        adv = pf_class["advancement"]

        data += "### Class Feats\n"
        data += format_adv_lvl_list("classFeats")

        data += "### Skill Feats\n"
        data += format_adv_lvl_list("skillFeats")

        data += "### Ancestry Feats\n"
        data += format_adv_lvl_list("ancestryFeats")

        data += "### Skill Increases\n"
        data += format_adv_lvl_list("skillIncrease")

        data += "### Ability Boosts\n"
        data += format_adv_lvl_list("abilityBoosts")

        data += "## Subclasses\n"
        subclasses = pf_class["subclasses"]
        if len(subclasses) > 0:
            for sub in subclasses:
                data += sub["name"] + ", " + sub["source"] + " p. " + str(sub["page"]) + "\n"
        else:
            data += "N/A\n"

        with open("D:\\Users\\louis\\OneDrive\\Documents\\aeranis\\dm_pf2e\\classes\\class-" + pf_class["name"].lower() + ".md", "w") as new_file:
            new_file.write(data)
            file_count += 1

print(file_count)