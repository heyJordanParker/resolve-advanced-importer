# Davinci Resolve Advanced Importer

Tool for automatically syncing a directory to a DaVinci Resolve bin.

## Why

Resolve is an amazing NLE but lacks a lot of the basic functionality and polish that can enable quick production. I created this to fix those gaps and speed up my YouTube workflow.

## How to use:

I'll update this later

## How to develop:

Test with:
```
nodemon .\resolveAdvancedImporter.py 
```

Create installer with:
```
pyinstaller -F  --noconsole .\resolveAdvancedImporter.py && copy config.json dist\config.json
```