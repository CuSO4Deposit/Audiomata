import configparser
from pathlib import Path
from datetime import date
from yt_dlp import YoutubeDL
from yt_dlp.utils import DateRange

config_path = Path("./config.ini")
config = configparser.ConfigParser()
config.read(config_path)

base_path = Path(config["meta"]["BasePath"])
base_path.mkdir(exist_ok=True)
ffmpeg_path = config["meta"]["FFmpegPath"]

ydl_opts = {
    "extract_flat": "discard_in_playlist",
    "ffmpeg_location": ffmpeg_path,
    "final_ext": "mp3",
    "format": "bestaudio/best",
    "fragment_retries": 10,
    "trim_file_name": 250,
    "ignoreerrors": "only_download",
    "outtmpl": {
        "default": "%(title)s [%(id)s]/%(title)s [%(id)s].%(ext)s",
        "subtitle": "%(title)s [%(id)s]/%(title)s [%(id)s].%(ext)s",
        "thumbnail": "%(title)s [%(id)s]/%(title)s [%(id)s].%(ext)s",
    },
    "paths": {
        "home": base_path,
    },
    "postprocessors": [
        {"format": "lrc", "key": "FFmpegSubtitlesConvertor", "when": "before_dl"},
        {"format": "png", "key": "FFmpegThumbnailsConvertor", "when": "before_dl"},
        {
            "key": "FFmpegExtractAudio",
            "nopostoverwrites": False,
            "preferredcodec": "mp3",
            "preferredquality": "5",
        },
        {"key": "FFmpegConcat", "only_multi_video": True, "when": "playlist"},
    ],
    "retries": 10,
    "subtitleslangs": ["ja"],
    "updatetime": False,
    "writesubtitles": True,
    "writethumbnail": True,
}

sections = config.sections()
for i in sections:
    if i == "meta":
        continue
    target = config[i]["Target"]
    output_path = base_path
    try:
        sub_dir = config[i]["SubDir"]
        output_path = output_path / sub_dir
        output_path.mkdir(exist_ok=True)
    except:
        pass
    output_path = output_path / i
    output_path.mkdir(exist_ok=True)
    dateafter = config[i]["DateAfter"]
    ydl_opts["paths"] = {
        "home": str(output_path),
    }
    ydl_opts["daterange"] = DateRange(dateafter, "99991231")
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([target])
    config[i]["DateAfter"] = date.today().strftime("%Y%m%d")

with config_path.open("w") as f:
    config.write(f)
