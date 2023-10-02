"""
Script for transforming a .csv file into a number of FoundryVTT PF2e deity files.

To import your new JSON(s), create a deity item in Foundry. Then right-click -> Import Data.
If something should go wrong when importing, press F12 to open
the console and check the error message.

My use-case is that I'm "storing" deity information on my MediaWiki-based campaign
setting website using Semantic MediaWiki properties. A download button appears
both on individual deity pages, as well as on the page with an overview of all
deities, letting me export the information on my wiki as a .csv file.
This script bridges the gap between my campaign setting site and FoundryVTT.

Q: Why not just use Adventure Documents?
A: Yes, I recommend you do that.

Author: github.com/lfknudsen
"""
import json
import csv

#=====================#
# Configuration start #

schema_version = 0.385 # check the PF2e settings for this. 0.385 is correct as of PF2e version 4.10.3
system_version = "4.10.3" # might not matter
foundry_version = "10.291" # might not matter
icon_path = "aeranis/deities/" # directory of the icon, relative to <user>/AppData/Local/FoundryVTT/Data/
input_filename = "result.csv" # relative path
output_filename_prefix = "deity-" # before the slug. Make sure any subdirectories are already created.
output_filename_postfix = "" # after the slug (but before .json, which is included automatically)
change_image_filetype = True # Set to True if the image text doesn't include filetype, or you'd like to change it.
new_image_filetype = ".webp" # Note that Foundry doesn't support .png transparency.

# Replace with the header names of your .csv. Or numbers (untested) if you've no header row.
Image = "Image"
Name = "Name"
Description = "Description"
GM_Notes = "GM Notes"
Source = "Source"
Category = "Belief Category"
Alignment_Own = "Alignment"
Alignment_Flw = "Follower Alignments"
Domains = "DomainsPF"
Domains_Alt = "Alt DomainsPF"
Font = "Divine Font"
Ability = "Divine Ability"
Skill = "Divine Skill"
Weapons = "Favoured Weapon"
Spell_Levels = "Spell Levels"
Spell_IDs = "Cleric Spell IDs"

# Configuration end #
#===================#

# Transform "Chaotic Neutral" -> "CN" and so on. Needed for deity's own alignment, but not followers'
# If already using initialisms, does nothing.
def initials(input_string):
    if len(input_string) <= 2:
        return input_string.upper()

    split_string = input_string.split(" ")
    output = ""
    for substring in split_string:
        output += substring[0]
    return output.upper()

# Abbreviate skill names
def skill_abbr(skill):
    match skill:
        case "intimidation":
            return "itm"
        case _:
            return skill[0:3:1]

# Make a dictionary with { spell level : spell ID }
def spells(levels, ids):
    levels_split = levels.split(", ")
    ids_split = ids.split(", ")
    if len(levels_split) != 0 and len(levels_split) != len(ids_split):
        return None

    spell_list = dict()
    for i in range(0, len(levels_split)):
        spell_list[levels_split[i]] = ids_split[i]
    return spell_list

# Remove everything after last period, replace with new filetype.
def adjust_filename(filename):
    if (change_image_filetype):
        return filename.rsplit(".", 1)[0] + new_image_filetype
    else:
        return filename

# Avoid adding ".json" to filename if user already specified in postfix text.
def add_json(filename):
    filename_split = filename.rsplit(".", 1)
    if (len(filename_split) == 2 and filename_split[1] == "json"):
        return filename
    else:
        return filename + ".json"

#===============#
# Program start #
#===============#
with open(input_filename, mode='r') as file:
    read = csv.DictReader(file)

    for row in read:
        slug = row[Name].lower().replace(" ", "-")

        new_dict = {
            "img": icon_path + adjust_filename(row[Image]),
            "name": row[Name],
            "system":
            {
                "description": {
                    "gm": row[GM_Notes],
                    "value": row[Description]
                },
                "source": { "value": row[Source] },
                "rules": [],
                "slug": slug,
                "schema": {
                    "version": schema_version,
                    "lastMigration": None
                },
                "category": row[Category].lower(),
                "alignment": {
                    "own": initials(row[Alignment_Own]),
                    "follower": row[Alignment_Flw].split(", ")
                },
                "domains": {
                    "primary": row[Domains].lower().split(", "),
                    "alternate": row[Domains_Alt].lower().split(", ")
                },
                "font": row[Font].lower().split(", "),
                "ability": row[Ability].lower().split(", "),
                "skill": skill_abbr(row[Skill].lower()),
                "weapons": row[Weapons].lower().replace(" ", "-").split(",-"),
                "spells": spells(row[Spell_Levels], row[Spell_IDs])
            },
            "type": "deity",
            "flags": {
                "core": {
                    "sourceId": ""
                },
                "exportSource" : {
                    "world": "",
                    "system": "",
                    "coreVersion": "",
                    "systemVersion": ""
                }
            },
            "effects": [],
            "_stats": {
                "systemId": "pf2e",
                "systemVersion": system_version,
                "coreVersion": foundry_version,
                "createdTime": 1680732257613,
                "modifiedTime": 1681422745476,
                "lastModifiedBy": ""
            }
        }
        output = json.dumps(new_dict, indent=4)
        output_filename = add_json(output_filename_prefix + slug + output_filename_postfix)
        with open(output_filename, "w") as outfile:
            outfile.write(output)