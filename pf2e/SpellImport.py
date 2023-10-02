"""
Converts a directory of FoundryVTT-compatible spells in JSON format into a single Lua file.
Messy, but it works, and it's much quicker than I expected or needed it to be.

The resulting Lua file is /just/ small enough to allow MediaWiki upload without changing
php.ini settings.

Author: github.com/lfknudsen
"""

import json
import glob
import re

change_image_filetype = True
new_image_filetype = ".png"

files = glob.glob("C:\\Users\\louis\\repos\\pf2e\\packs\\data\\spells.db\\*.json")
data = "return {\n"
count_found = 0
count_done = 0
count_failed = 0

# Remove everything after last period, replace with new filetype.
def adjust_filename(filename):
    if (change_image_filetype):
        return filename.rsplit(".", 1)[0] + new_image_filetype
    else:
        return filename

# Formats the input string so it can be added to the overarching string.
def format_value(input_string, key):
    output_string = ""
    if (input_string != "" and input_string != None):
        output_string = '        [\"' + key + '\"] = \"' + input_string + "\",\n"
    return output_string

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

# The lua "traits" key will include everything from the "traits" list and the "school" string
def format_traits(traits, school):
    output_text = "        [\"traits\"] = \"<table class=\\\"traits\\\"><tr></tr>"
    for i in traits:
        output_text += "<td><table class=\\\"trait\\\"><tr></tr><td>" + i.capitalize() + "</td></table></td>"
    output_text += "<td><table class=\\\"trait\\\"><tr></tr><td>" + school.capitalize() + "</td></table></td></table>\",\n"
    return output_text

def remove_trailing_comma(input_string):
    return input_string.rsplit(",", 1)[0]

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

# Formats the new list of components; not every (or any) component is necessarily present.
def format_components(components):
    output_text = ""
    if components["material"] == True:
        output_text += "material, "
    if components["somatic"] == True:
        output_text += "somatic, "
    if components["verbal"] == True:
        output_text += "verbal"
    output_text = output_text.strip()
    if (output_text != "" and output_text[len(output_text)-1] == ","):
        output_text = output_text[0:len(output_text)-1]
    return output_text

# Remove anything in between [ and ] inclusive.
def remove_links(input_string):
    return re.sub('\[.*?\]', '', input_string)

# Remove anything in between <h2 and h2> inclusive.
def remove_headers(input_string):
    return re.sub('<h2.*?h2>', '', input_string)

# Start the program itself, looping through each .json file in the directory,
# opening it, and then parsing the data within, formatting it into a Python-string
# which is finally added to one, overarching "data" string.
for filename in files:
    with open(filename, mode="r") as file:
        count_found += 1
        try:
            obj = json.load(file)
        except:
            print(filename + " could not decode.")
            count_failed += 1
        if (obj["type"] == "spell"): # If the file isn't a spell, skip it. Fail-safe.
            data += '    [\"' + obj["name"] + '\"] = {\n'
            data += '        [\"id\"] = \"' + obj["_id"] + '\",\n'
            data += '        [\"slug\"] = \"' + obj["name"].lower().replace(" ", "-") + "\",\n"
            data += '        [\"image\"] = \"' + adjust_filename(obj["img"].rsplit("/", 1)[1]) + "\",\n"

            system_dict = obj["system"]
            if (system_dict["area"] != None):
                area_type = system_dict["area"]["type"]
                area_range = system_dict["area"]["value"]
            category = system_dict["category"]["value"].capitalize()
            components = system_dict["components"]
            cost = system_dict["cost"]["value"]
            description = system_dict["description"]["value"]
            duration = system_dict["duration"]["value"]
            level = system_dict["level"]["value"]
            materials = system_dict["materials"]["value"]
            spell_range = system_dict["range"]["value"]
            school = system_dict["school"]["value"]
            source = system_dict["source"]["value"]
            target = system_dict["target"]["value"]
            time = system_dict["time"]["value"]
            traditions = system_dict["traditions"]["value"]
            rarity = system_dict["traits"]["rarity"]
            traits = system_dict["traits"]["value"]

            if (system_dict["area"] != None):
                data += format_value(area_type, "area_type")
                data += format_value(str(area_range), "area_range")
            data += format_value(category, "category")
            data += format_value(format_components(components), "components")
            data += format_value(cost, "cost")
            data += description_format(description)
            data += format_value(duration, "duration")
            data += format_value(str(level), "level")
            data += format_value(materials, "materials")
            data += format_value(spell_range, "range")
            data += format_value(source, "source")
            data += format_value(target, "target")
            data += format_value(time, "time")
            data += format_list(traditions, "traditions")
            data += format_traits(traits, school)
            data = remove_trailing_comma(data)
            data += """\n    },\n"""
            count_done += 1
data = remove_trailing_comma(data)
data += "\n}"
with open("spells.lua", "w") as new_file:
    new_file.write(data)
print("Successfully parsed " + str(count_done) + " fitting files. Found " + str(count_found) + " .json files in total, " + str(count_failed) + " of which failed to decode.")