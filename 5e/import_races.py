"""
Converts a list of D&D 5e races in a JSON file into a Lua file.

Author: github.com/lfknudsen
"""

import json
import glob

# filename = glob.glob("C:\\Users\\louis\\repos\\5e Tools\\packs\\data\\races.json")
filename = "races.json"
data = "return {\n"

blocked_books = ["UA", "AI", "DMG"]

# Used to filter out all non-player races.
def player_race(x):
    try:
        if ("NPC Race" in x["traitTags"]): return False # remove NPC races
    except:
        pass
    for book in blocked_books:
        if (x["source"].find(book) != -1): return False # remove all blacklisted races
    else: return True

# Formats the input string so it can be added to the overarching string.
def format_value(input_string, key):
    output_string = ""
    if (input_string != "" and input_string != None):
        output_string = '        [\"' + key + '\"] = \"' + input_string + "\",\n"
    return output_string

def remove_trailing_comma(input_string):
    return input_string.rsplit(",", 1)[0]

# Formats a list of strings so it can be added to the overarching string.
def format_list(input_list, key):
    if (len(input_list) == 0):
        return ""
    output_text = "        [\"" + key + "\"] = \""
    for i in input_list:
        output_text += i.capitalize() + ", "
    output_text = remove_trailing_comma(output_text)
    output_text += "\",\n"
    return output_text

# Formats a list of strings so it can be added to the overarching string.
def format_chosen_abils(input_dict):
    if (len(input_dict) == 0):
        return ""
    output_text = ""
    output_text += "        [\"abilities_choose_count\"] = \""
    output_text += str(input_dict["count"])
    output_text += "\",\n"
    output_text += "        [\"abilities_choose\"] = \""
    for i in input_dict["from"]:
        output_text += i.capitalize() + ", "
    output_text = remove_trailing_comma(output_text)
    output_text += "\",\n"
    return output_text

def format_dict(input_dict, key):
    output_text = "        [\"" + key + "\"] = {"
    for k,v in input_dict.items():
        if (k == "choose"): continue
        else:
            output_text += "[\"" + k + "\"] = \""
            output_text += str(v)
            output_text += "\", "
    output_text = remove_trailing_comma(output_text)
    output_text += "},\n"
    return output_text

def format_speed_dict(input_dict, key):
    output_text = "        [\"" + key + "\"] = {"
    if (type(input_dict) == int):
        output_text += "[\"walk\"] = \"" + str(input_dict) + "\""
    else:
        for k,v in input_dict.items():
            output_text += "[\"" + k + "\"] = \""
            if (str(v) == "True"):
                output_text += str(input_dict["walk"])
            else:
                output_text += str(v)
            output_text += "\", "
    output_text = remove_trailing_comma(output_text)
    output_text += "},\n"
    return output_text

default_abilities = '        [\"abilities\"] = \"Choose one of: (a) Choose any +2; choose any other +1 (b) Choose three different +1\",\n'

def format_entry(input_text):
    output_text = input_text.replace("{@Skill ", "")
    output_text = output_text.replace("{@skill ", "")
    output_text = output_text.replace("{@Spell ", "")
    output_text = output_text.replace("{@spell ", "")
    output_text = output_text.replace("{@Damage ", "")
    output_text = output_text.replace("{@damage ", "")
    output_text = output_text.replace("{@Condition ", "")
    output_text = output_text.replace("{@condition ", "")
    output_text = output_text.replace("{@Dice ", "")
    output_text = output_text.replace("{@dice ", "")
    output_text = output_text.replace("{@Item ", "")
    output_text = output_text.replace("{@item ", "")
    output_text = output_text.replace("{@Creature ", "")
    output_text = output_text.replace("{@creature ", "")
    output_text = output_text.replace("{@Book ", "")
    output_text = output_text.replace("{@book ", "")
    output_text = output_text.replace("{@Action ", "")
    output_text = output_text.replace("{@action ", "")
    output_text = output_text.replace("{@Filter ", "")
    output_text = output_text.replace("{@filter ", "")
    output_text = output_text.replace("{@5etools ", "")
    output_text = output_text.replace("|feats.html ", "")
    output_text = output_text.replace("|feats.html", "")
    output_text = output_text.replace("|phb", "")
    output_text = output_text.replace("|xge", "")
    output_text = output_text.replace("blowgun needle|blowgun needles", "blowgun needle(s)")
    output_text = output_text.replace("dart|darts", "dart(s)")
    output_text = output_text.replace("|5|tools", "")
    output_text = output_text.replace("||null", "")
    output_text = output_text.replace("|items|source=phb|category=basic|type=martial weapon", "")
    output_text = output_text.replace("|items|source=phb|miscellaneous=mundane|type=artisan's tools", "")
    output_text = output_text.replace("|PHB ", "")
    output_text = output_text.replace("|PHB", "")
    output_text = output_text.replace("}", "")
    output_text = output_text.replace("\u2014", " - ")
    return output_text

def format_entries(input_list):
    output_text = "        [\"entries\"] = {\n"
    for e in input_list:
        formatted_entry = format_entry(e["entries"][0])
        output_text += "            [\"" + e["name"] + "\"] = [[" + formatted_entry + "]],\n"
    output_text = remove_trailing_comma(output_text)
    output_text += "},\n"
    return output_text

with open(filename, mode="r") as file:
    try:
        obj = json.load(file)
    except:
        print(filename + " could not decode.")

    race = obj["race"]
    races = filter(player_race, race)
    print(type(races))
    for r in races:
        data += '    [\"' + r["name"] + '\"] = {\n'
        data += format_value(r["source"], "source")
        data += format_value(str(r["page"]), "page")
        try: data += format_list(r["size"], "size")
        except: pass
        try: data += format_speed_dict(r["speed"], "speed")
        except: pass
        try: data += format_list(r["traitTags"], "traits")
        except: pass
        try:
            skill_lst = r["skillProficiencies"][0]["choose"]
            data += format_list(skill_lst["from"], "skills")
            try:
                data += format_value(str(skill_lst["count"]), "skills_count")
            except: pass
        except:
            try:
                skill_dict = r["skillProficiencies"][0]
                data += format_dict(skill_dict, "skills")
            except: pass
        try: data += format_value(r["darkvision"], "darkvision")
        except: pass
        try: data += format_chosen_abils(r["ability"][0]["choose"])
        except: pass
        try: data += format_dict(r["ability"][0], "abilities")
        except: data += default_abilities
        try: data += format_dict(r["age"], "age")
        except: pass
        try: data += format_dict(r["languageProficiencies"][0], "languages")
        except: pass
        try: data += format_entries(r["entries"])
        except: pass

        data = remove_trailing_comma(data)
        data += """\n    },\n"""

data = remove_trailing_comma(data)
data += "\n}"
with open("races.lua", "w") as new_file:
    new_file.write(data)