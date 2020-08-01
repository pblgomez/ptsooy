import argparse
import opml
import os

import subprocess
import urllib
import sys
import yaml
import re
import feedparser as fp
import youtube_dl
from youtube_dl.utils import DateRange
import datetime
import time


channels = "channels.yaml"


def delete_old():
    if keep_newer_than > 1:
        from glob import glob
        result = [y for x in os.walk("Videos") for y in glob(os.path.join(x[0], '*'))]
        now = time.time()
        for f in result:
            if os.stat(f).st_mtime < now - keep_newer_than * 86400:
                if os.path.isfile(f):
                    print("Deleting: " + f)
                    os.remove(f)


def download_videos():
    with open(channels, "r") as f:
        all_feeds = yaml.load(f, Loader=yaml.FullLoader)
        subs = len(all_feeds)
        # print(subs)
        urls = list(all_feeds.values())
        # print(urls)

        i = 0
        while i < subs:

            # parse YouTube feed
            rss = fp.parse(urls[i])

            create_rss(rss.feed.author, rss.feed.link)
            i += 1

            y = 0
            for item in rss.entries:
                if y < vids_count:
                    ydl_opts = {
                        # "simulate": True,
                        "format": "best",  # "bestvideo+bestaudio"
                        "outtmpl": "Videos/%(uploader)s/%(title)s.%(ext)s",
                        # "restrictfilenames": "True",
                        "ignoreerrors": True,
                        "download_archive": "Videos/archive.txt",
                        "daterange": DateRange(date_after),
                    }
                    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(item["link"], download=True)
                        filename = ydl.prepare_filename(info)
                        filename = str(filename)
                        filename = filename.replace("Videos/", "")
                        video_thumbnail = info.get("thumbnail", None)

                    fill_rss(
                        item["author"],
                        item["title"],
                        item["link"],
                        filename,
                        item["published"][0:16],
                        item["summary"],
                        video_thumbnail,
                    )

                    y += 1
            finish_rss(rss.feed.author)


def create_rss(author, link):
    now = datetime.datetime.now()
    now = (
        now.strftime("%a")
        + ","
        + now.strftime("%d")
        + " "
        + now.strftime("%b")
        + " "
        + now.strftime("%Y")
        + " "
        + now.strftime("%X")
    )

    # Contenido inicial
    rss_create_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd">
  <channel>
    <title>{author}</title>
    <link>{link}</link>
    <description>Podcast version of {author}</description>
    <lastBuildDate>{now}</lastBuildDate>
    <itunes:author>{author}</itunes:author>"""

    # Write the initial file
    rss_file = "Videos/" + author + "/rss.xml"
    os.makedirs(os.path.dirname(rss_file), exist_ok=True)
    with open(rss_file, "w") as rss_out:
        rss_out.write(rss_create_content)


def fill_rss(author, title, link_orig, link, published, summary, thumb_vid):
    # from variables import host, port
    # print("El link es: " + link)
    title = title.replace("&", "&#38;")

    summary = summary.replace("&", "&#38;")

    # Check if file exist
    if os.path.isfile("Videos/" + link):
        # if os.path.isfile(link):
        duration, file_size = get_info(link)

        # fix link name in for web
        link = urllib.parse.quote(link)

        rss_fill_content = f"""
      <item>
        <guid>"{link}"</guid>
        <title>{title}</title>
        <link>{link_orig}</link>
        <description>{summary}</description>
        <pubDate>{published}</pubDate>
        <enclosure url="{host}:{port}/{link}" length="{file_size}" type="video/mp4"></enclosure>
        <itunes:author>{author}</itunes:author>
        <itunes:subtitle>{title}</itunes:subtitle>
        <itunes:summary>{summary}</itunes:summary>
        <itunes:image href="{thumb_vid}"></itunes:image>
        <itunes:duration>{duration}</itunes:duration>
      </item>
  """

        rss_file = "Videos/" + author + "/rss.xml"
        with open(rss_file, "a") as rss_out:
            rss_out.write(rss_fill_content)


# Def to get the lenght of the videos
def get_length(filename):
    from subprocess import check_output

    # For Linux
    a = str(
        check_output('ffprobe -i  "' + filename + '" 2>&1 |grep "Duration"', shell=True)
    )
    a = a.split(",")[0].split("Duration:")[1].strip()
    h, m, s = a.split(":")
    duration = int(h) * 3600 + int(m) * 60 + float(s)
    return float(duration)


def get_info(filename):
    filename = "Videos/" + filename
    # Get lenght of video
    duration = get_length(filename)
    duration = str(datetime.timedelta(seconds=duration))[:7]
    # Get filesize
    # file_size = os.path.getsize("Videos/" + filename)
    file_size = os.path.getsize(filename)
    return (duration, file_size)


def finish_rss(author):
    rss_finish_content = """  </channel>
</rss>"""
    rss_file = "Videos/" + author + "/rss.xml"
    with open(rss_file, "a") as rss_out:
        rss_out.write(rss_finish_content)


def ToYaml(feeds):
    if os.path.isfile(channels):
        with open(channels, "r") as f:
            all_feeds = yaml.load(f, Loader=yaml.FullLoader)
            all_feeds = {**all_feeds, **feeds}  # merge new and old
            sorted_feeds = dict(sorted(all_feeds.items()))
            with open(channels, "w") as f:
                f.write("---\n")
                f.write(yaml.dump(sorted_feeds))
    else:
        with open(channels, "w") as f:
            f.write("---\n")
            f.write(yaml.dump(feeds))


def substract_opml_subs(inputfile):
    nested = opml.parse(inputfile)
    subs = len(nested[0])

    feeds = {}
    i = 0
    while i < subs:
        title = nested[0][i].text
        # Remove special characters
        # title = re.sub(r"[^A-Za-z0-9]+", "", title)
        url = nested[0][i].xmlUrl
        i += 1
        feeds[title] = url
    return feeds


def myParser():
    # Arguments
    parser = argparse.ArgumentParser(
        description="Converts youtube subscriptions opml to rss podcasts"
    )
    parser.add_argument(
        "-i",
        "--input",
        required=False,
        help="filepath for new/add subscriptions",
        type=str,
        dest="inputfile",
    )
    parser.add_argument(
        "-d",
        "--date-after",
        required=False,
        help="Download only videos after YYYYMMDD",
        type=str,
        dest="date_after",
    )
    parser.add_argument(
        "-v",
        "--vids_count",
        required=False,
        help="Download only X videos from each subscription",
        type=str,
        dest="vids_count",
    )
    parser.add_argument(
        "-H",
        "--host",
        required=False,
        help="name of the host for the rss ex: https://feeds.example.org",
        type=str,
        dest="host",
    )
    parser.add_argument(
        "-p",
        "--port",
        required=False,
        help="Port of the host for the rss feed if not 80",
        type=str,
        dest="port",
    )
    parser.add_argument(
        "-k",
        "--keep_newer_than",
        required=False,
        help="Keep newer than X days",
        type=str,
        dest="keep_newer_than",
    )
    args = parser.parse_args()
    return args, parser


def main():

    args, parser = myParser()
    global date_after, vids_count, host, port, keep_newer_than

    if "date_after" in os.environ:
        date_after = os.environ["date_after"]
    elif args.date_after:
        date_after = args.date_after
    else:
        date_after = "20200731"

    if "vids_count" in os.environ:
        vids_count = os.environ["vids_count"]
    elif args.vids_count:
        vids_count = args.vids_count
    else:
        vids_count = 3

    if "host" in os.environ:
        host = os.environ["host"]
    elif args.host:
        host = args.host
    else:
        host = "http://localhost"

    if "port" in os.environ:
        port = os.environ["port"]
    elif args.port:
        port = args.port
    else:
        port = 80

    if "keep_newer_than" in os.environ:
        keep_newer_than = os.environ["keep_newer_than"]
    elif args.keep_newer_than:
        keep_newer_than = int(args.keep_newer_than)
    else:
        keep_newer_than = 7

    delete_old()



    if args.inputfile:
        inputfile = args.inputfile
        if os.path.isfile(inputfile):
            feeds = substract_opml_subs(inputfile)
            ToYaml(feeds)
            download_videos()
    else:
        if os.path.isfile("subscription_manager"):
            feeds = substract_opml_subs("subscription_manager")
            ToYaml(feeds)
            download_videos()
        elif os.path.isfile("channels.yaml"):
            download_videos()
        else:
            parser.print_help()
            print("Could't find channels.yaml use -i for a subscription_manager file")
            sys.exit(0)



while True:
    main()
    time.sleep(3*3600)