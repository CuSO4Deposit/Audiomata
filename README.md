# Audiomata

Python script to download and update music archive, based on yt-dlp.

## config.ini

This script read config from `./config.ini`.

`[meta]` sections specifies ffmpeg location and download dir.

For each youtube url to download, create a new section `[SectionName]`, default `DateAfter` value should be `00010101`.

## crontab

An example crontab task:

```
0 1 * * * cd /path/to/project/; date +"[\%Y-\%m-\%d]" >> /path/to/project/crontab.log; /path/to/project/AudiomataVenv/bin/python /path/to/project/Audiomata.py >> /path/to/project/crontab.log 2>&1
```