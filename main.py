#!/usr/bin/env python3.4

import sys
import os
import argparse
import feedparser

from emonoda import tfile

from emonoda.apps import init
from emonoda.apps import get_configured_log
from emonoda.apps import get_configured_client
from emonoda.plugins.fetchers import read_url, build_opener


#torrent_url = "http://www.nyaa.se/?page=download&tid=674041"
rss_url = "http://www.nyaa.se/?page=rss&term=%5BHorribleSubs%5D+World+Trigger+720"
dest_prefix = "/media/Elements/Anime/"
anime_name = "World Trigger"

dest_path = dest_prefix + anime_name

def main():
    (parent_parser, argv, config) = init()
    args_parser = argparse.ArgumentParser(
        prog="example",
        description="Example program",
        parents=[parent_parser],
    )
    args_parser.add_argument("-v", "--verbose", action="store_true")
    options = args_parser.parse_args(argv[1:])

    with get_configured_log(config, False, sys.stdout) as log_stdout:
        with get_configured_log(config, (not options.verbose), sys.stderr) as log_stderr:
            client = get_configured_client(
                config=config,
                required=True,
                with_customs=False,
                log=log_stderr,
            )
            log_stdout.print("Torrent client initialised: %s", (client,))
            hashes = client.get_hashes()
            feed = feedparser.parse(rss_url)
            log_stdout.print("Loaded %s feed", feed['feed']['title'])
            os.makedirs(dest_path, exist_ok=True)
            for entry in feed['entries']:
                torrent_url = entry['link']
                t = tfile.Torrent(data=read_url(build_opener(), torrent_url), path='/dev/null')
                log_stdout.print("Checking %s", entry['title'])
                if not t.get_hash() in hashes:
                    client.load_torrent(t, dest_path)
                    log_stdout.print("Torrent loaded to %s", dest_path)


if __name__ == "__main__":
    main()
