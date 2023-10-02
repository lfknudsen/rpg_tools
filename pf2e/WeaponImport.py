"""
Converts a directory of FoundryVTT-compatible domains in JSON format into a single Lua file.
Messy, but it works, and it's much quicker than I expected or needed it to be.

Author: github.com/lfknudsen
"""

import json
import glob
import re

change_image_filetype = True
new_image_filetype = ".png"

files = glob.glob("C:\\Users\\louis\\repos\\pf2e\\packs\\data\\equipment.db\\*.json")
check_additional_folder = True
additional_files = glob.glob("*.json") # For homebrew items that you do not want erased by Pathfinder 2e system updates.
data = "return {\n"
count_found = count_done = count_failed = 0

def format_value(input_string, key):
    return '        [\"' + key + '\"] = \"' + input_string + '\",\n'

def format_list(input_list, key):
    if (len(input_list) == 0):
        return ""
    output = '        [\"' + key + '\"] = \"<table class=\\\"traits\\\"><tr></tr>'
    for i in input_list:
        output += '<td><table class=\\\"trait\\\"><tr></tr><td>' + i.replace("-"," ").title() + '</td></table></td>'
    output += '</table>\",\n'
    return output

# Remove everything after last period, replace with new filetype.
def adjust_filetype(filename):
    if (change_image_filetype):
        return filename.rsplit(".", 1)[0] + new_image_filetype
    else:
        return filename

def remove_trailing_comma(input_string):
    return input_string.rsplit(",", 1)[0]

def format_name(filename):
    output = filename
    if (filename.find("\\") != -1): # in case a relative path is used
        output = output.rsplit("\\",1)[1]
    return output.rsplit(".",1)[0].rsplit("-",1)[0]

# Remove anything in between [ and ] inclusive.
def remove_links(input_string):
    return re.sub('\[.*?\]', '', input_string)

# Remove anything in between <h2 and h2> inclusive.
def remove_headers(input_string):
    return re.sub('<h2.*?h2>', '', input_string)

# Descriptions are littered with HTML tags that need to be removed or replaced.
def description_format(input_string):
    output_string = remove_links(input_string)
    output_string = remove_headers(output_string)
    output_string = output_string.replace("<thead>", "")
    output_string = output_string.replace("</thead>", "")
    output_string = output_string.replace("<tbody>", "")
    output_string = output_string.replace("</tbody>", "")
    output_string = output_string.replace("[", "")
    output_string = output_string.replace("]", "")
    output_string = output_string.replace('class="pf2-table"', 'class="rollable-table"')
    output_string = "        [\"description\"] = [[" + output_string
    output_string = output_string.replace("@UUID", "")
    output_string = output_string.replace("{", "\'\'")
    output_string = output_string.replace("}", "\'\'")
    output_string = output_string.replace("<p>", "")
    output_string = output_string.replace("</p>", "")
    output_string = output_string.replace("<hr />", "----")
    output_string = output_string.replace("<strong>", "\n\'\'\'")
    output_string = output_string.replace("</strong>", ":\'\'\'")
    output_string += "]],\n"
    return output_string

def format_usage(input_string):
    return "1" if input_string.find("one") != -1 else "2"

def format_reload(input_string):
    return "-" if input_string == "" else input_string

def add_information(obj):
    text = ""
    if (obj["type"] == "weapon" and obj["system"]["baseItem"] == obj["name"].lower().replace (" ", "-")):
        text += '    [\"' + obj["name"] + '\"] = {\n'
        try:
            text += '        [\"id\"] = \"' + obj["_id"] + '\",\n'
        except:
            1
        text += '        [\"slug\"] = \"' + obj["name"].lower().replace(" ", "-") + "\",\n"
        content = obj["system"]
        damage = content["damage"]
        text += format_value(str(damage["dice"]) + damage["die"] + " " + damage["damageType"], "damage")
        text += format_list(content["traits"]["value"], "traits")
        text += format_value(format_usage(content["usage"]["value"]), "usage")
        text += format_value(content["category"].capitalize(), "category")
        text += format_value(adjust_filetype(obj["img"]), "image")
        text += description_format(content["description"]["value"])
        text += format_value(content["group"].capitalize(), "group")
        try:
            text += format_value(str(content["range"]), "range")
        except:
            1
        try:
            text += format_value(str(format_reload(content["reload"]["value"])), "reload")
        except:
            1
        text += format_value(str(content["weight"]["value"]), "weight")
        text += format_value(content["source"]["value"], "source")
        text = remove_trailing_comma(text)
        text += """\n    },\n"""
    return text

# Start the program itself, looping through each .json file in the directory,
# opening it, and then parsing the data within, formatting it into a Python-string
# which is finally added to one, overarching "data" string.
def build_text_from_directory(directory):
    found = failed = done = 0
    output_string = ""
    for filename in directory:
        with open(filename, mode="r") as file:
            found += 1
            try:
                obj = json.load(file)
            except:
                print(filename + " could not decode.")
                failed += 1
            new_weapon = add_information(obj)
            if (new_weapon != ""):
                output_string += new_weapon
                done += 1
    return output_string, found, failed, done

build_return = build_text_from_directory(files)
data += build_return[0]
count_found += build_return[1]
count_failed += build_return[2]
count_done += build_return[3]
if (check_additional_folder == True):
    build_return = build_text_from_directory(additional_files)
    data += build_return[0]
    count_found += build_return[1]
    count_failed += build_return[2]
    count_done += build_return[3]
data = remove_trailing_comma(data)
data += "\n}"
with open("weapons.lua", "w") as new_file:
    new_file.write(data)
print("Successfully parsed " + str(count_done) + " fitting files. Found " + str(count_found) + " .json file(s) in total, " + str(count_failed) + " of which failed to decode.")