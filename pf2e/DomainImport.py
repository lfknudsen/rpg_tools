"""
Converts a directory of FoundryVTT-compatible domains in JSON format into a single Lua file.
Messy, but it works, and it's much quicker than I expected or needed it to be.

Author: github.com/lfknudsen
"""

import json
import glob

change_image_filetype = True
new_image_filetype = ".png"

directories = [
    "C:\\Users\\louis\\repos\\pf2e\\packs\\data\\domains.db\\",
    ""
]
data = "return {\n"

def remove_trailing_comma(input_string):
    return input_string.rsplit(",", 1)[0]

def format_name(filename):
    output = filename
    if (filename.find("\\") != -1): # in case a relative path is used
        output = output.rsplit("\\",1)[1]
    return output.rsplit(".",1)[0].rsplit("-",1)[0]

# Start the program itself, looping through each .json file in the directory,
# opening it, and then parsing the data within, formatting it into a Python-string
# which is finally added to one, overarching "data" string.
def build_text_from_directory(directories):
    found = failed = done = 0
    output_string = ""
    for d in directories:
        path = glob.glob(d + "*.json")
        for filename in path:
            with open(filename, mode="r") as file:
                found += 1
                try:
                    obj = json.load(file)
                except:
                    print(filename + " could not decode.")
                    failed += 1

                new_string = convert_contents(filename, obj)
                if (new_string != ""):
                    output_string += new_string
                    done += 1
    return output_string, found, failed, done

def convert_contents(filename, obj):
    output_string = '    [\"' + obj["name"].replace(" Domain", "") + '\"] = {\n'
    output_string += '        [\"id\"] = \"' + obj["_id"] + '\",\n'
    output_string += '        [\"slug\"] = \"' + format_name(filename).lower().replace(" ", "-") + "\",\n"

    content = obj["content"]
    extra_nl = 1 if obj["name"] == "Introspection Domain" else 0
    split_content = content.rsplit("\n")
    split_content[2 + extra_nl] = split_content[2 + extra_nl].replace("<p>", "")
    split_content[2 + extra_nl] = split_content[2 + extra_nl].replace("</p>", "").replace("-", " - ")
    output_string += '        ["description"] = "' + split_content[2 + extra_nl] + '",\n'
    split_spells = split_content[1].split("{")
    end_index = split_spells[1].find("}")
    output_string += '        ["spell"] = "' + split_spells[1][:end_index] + '",\n'
    end_index = split_spells[2].find("}")
    output_string += '        ["adv_spell"] = "' + split_spells[2][:end_index] + '",\n'

    output_string = remove_trailing_comma(output_string)
    output_string += """\n    },\n"""
    #print("Finished " + filename)
    return output_string

build_return = build_text_from_directory(directories)
data += build_return[0]
data = remove_trailing_comma(data)
data += "\n}"
with open("domains.lua", "w") as new_file:
    new_file.write(data)
print("Successfully parsed " + str(build_return[3]) + " fitting files. Found " + str(build_return[1]) + " .json file(s) in total, " + str(build_return[2]) + " of which failed to decode.")