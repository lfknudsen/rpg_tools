# What's here?
Small utilities for TTRPGs and cross-platform use of SRD resources. Feel free to contribute.

Note: This repository does not and will never contain any content which it does not have usage rights to. Please support the writers, artists, designers, playtesters, and more who work hard to make our favourite TTRPGs by buying the books.

## My use-case
My campaign setting is laid out on a MediaWiki website (https://world.aeranis.com).
To have access to the PF2e SRD data I have used the official FoundryVTT module's
JSON files, available at https://github.com/foundryvtt/pf2e. These files are pretty inconsistent and occassionally contain special characters, but for now it works fine.

Many of the scripts look in a folder and open each JSON file in turn, parse
and extract the relevant information within, and save everything to a single
.lua file which can then be uploaded to MediaWiki.
The source code for the wiki can be found... on the wiki. Feel free to peruse it. It is based in large part on (... and uses code directly lifted from) the League of Legends Fandom wiki, which uses a lot of Lua code to do interesting things.

I have technically begun work on similar utilities for 5e, but as data for this is less readily available (and given the much-restricted license of use), there are fewer scripts for this.