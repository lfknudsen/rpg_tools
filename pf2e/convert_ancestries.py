"""
Converts a directory of Pathfinder 2e ancestries, each in a separate JSON file,
into markdown files. Based on https://github.com/Pf2eToolsOrg/Pf2eTools.git format.
I'm specifically using it with Obsidian.MD alongside TTRPG-Convert-CLI
(https://github.com/ebullient/ttrpg-convert-cli), which does not import ancestries.

Author: github.com/lfknudsen
"""

import json
import glob
import re

files = glob.glob("D:\\TTRPGs\\ttrpg-convert-cli-2.2.3-windows-x86_64\\bin\Pf2eTools\\data\\ancestries\\ancestry-*.json")

def format_entry(input_text):
    output_text = input_text.replace("\u2014", " - ")
    return output_text

for file in files:
    data = "---\nobsidianUImode: preview\ncssclasses: pf2e,pf2e-ancestry\ntags:\n- compendium/src/pf2e/"
    with open(file, mode="r") as opened_file:
        try:
            obj = json.load(opened_file)
        except:
            print(file + " could not decode.")

        anc = obj["ancestry"][0]
        data += anc["source"].lower()
        data += "\naliases: [\""
        data += anc["name"]
        data += "\"]\n---\n# "
        data += anc["name"]
        data += "\n"
        data += format_entry(str(anc["info"][0])) + "\n\n"
        data += "### HP\n" + str(anc["hp"]) + "\n"
        data += "### Size\n" + anc["size"][0] + "\n"
        data += "### Speed\n" + str(anc["speed"]["walk"]) + "\n"
        data += "### Boosts\n"
        for b in anc["boosts"]:
            data += b + "\n"
        try:
            flaw = anc["flaw"][0]
            data += "### Flaw\n" + flaw + "\n"
        except:
            pass
        data += "### Languages\n"
        for l in anc["languages"]:
            l_edit = l.replace("{@language ", "*")
            l_edit = l_edit.replace("{@filter ", "")
            l_edit = re.sub("\|[a-zA-Z_0-9]*}", "*", l_edit)
            l_edit = l_edit.replace("|languages||Type=Common}", "")
            l_edit = l_edit.replace("}", "*")
            data += l_edit + "\n"
        data += "### Traits\n"
        for t in anc["traits"]:
            data += t + "\n"
        with open("ancestries\\anc-" + anc["name"].lower() + ".md", "w") as new_file:
            new_file.write(data)