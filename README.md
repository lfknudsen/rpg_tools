# RPG-Tools
Small utilities for TTRPGs and cross-platform use of SRD resources. Feel free to contribute.

Note: This repository does not and will never contain any content which it does not have usage rights to. Please support the writers, artists, designers, playtesters, and more who work hard to make our favourite TTRPGs by buying the books, and make sure only to use the content which you own.

## Use-cases
There are two different (but related) utility categories/use-cases currently.

### Wiki
My campaign setting is laid out publically on a MediaWiki website (https://world.aeranis.com).
To have access to the PF2e SRD data I have used the official FoundryVTT module's
JSON files, available at https://github.com/foundryvtt/pf2e. These files are pretty inconsistent and occassionally contain special characters, but for now it works fine.

Many of the scripts look in a directory of JSON files, open each file in turn, parse
and extract the relevant information within, and save everything to a single
.lua file which can then be uploaded to MediaWiki. They're essentially JSON -> LUA converters, for many-to-one specifically.
The source code for the wiki can be found... on the wiki. Feel free to peruse it. It is based in large part on (... and uses code directly lifted from) the League of Legends Fandom wiki, which uses a lot of Lua code to do interesting things.

I have technically begun work on similar utilities for 5e, but given the Wizards of the Coast's heavily restrictive license, and that I've been trying out PF2e lately, there is only one script for this (so far?).

### Obsidian.MD
In experimenting with Obsidian.MD (https://github.com/obsidianmd) as a tool for campaign management,
I convert ancestries in JSON format from https://github.com/Pf2eToolsOrg/Pf2eTools.git to markdown format in order
to link directly to them in my notes.

This is intended to be used alongside TTRPG-Convert-CLI (https://github.com/ebullient/ttrpg-convert-cli), which does not work with ancestries and classes. Since that tool uses PF2eTools.git, this script does the same (so as to only require one download of the source).