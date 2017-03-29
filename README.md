#Purpose

Often latex sources contain useless files or temporary comments.

The purpose of this script is to prepare files for a submission to arXiv.
- It strips comments and collect only useful files from a master file.
- Copy the <master_file>.bbl file if it exists.

In case you need to add other files (styles), there is a global variable that can be modified.

Be sure to have a backup of your files before running this script.

#Usage

axivify.py <master_file>
Should be launched from <master_file> directory.
