# Davinci Resolve Advanced Importer

Tool for automatically syncing a directory to a DaVinci Resolve bin.

## Why

Resolve is an amazing NLE but lacks a lot of the basic functionality and polish that can enable quick production. I created this to fix those gaps and speed up my YouTube workflow.

## How to use:

I'll update this later

## How to develop:

Test with ("npm i nodemon" first):
```
nodemon .\resolveAdvancedImporter.py --ignore *json
```

Create Windows exe with:
```
pyinstaller -F --noconsole --icon=resolveImporter.ico .\resolveAdvancedImporter.py && copy config.json dist\config.json && ren dist "Resolve Advanced Importer"
```

Create OSX app with:
```
pyinstaller -F --noconsole --icon=resolveImporter.ico ./resolveAdvancedImporter.py && cp config.json dist/resolveAdvancedImporter.app/Contents/MacOS/config.json && mv dist "Resolve Advanced Importer"
```