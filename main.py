#!/usr/bin/env python3.4

import sys
import os
import yaml
import argparse
import feedparser

from emonoda import tfile

from emonoda.apps import init
from emonoda.apps import get_configured_log
from emonoda.apps import get_configured_client
from emonoda.plugins.fetchers import read_url, build_opener

# import confetti


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
            with open('nyaa.yaml', 'r') as f:
                rss_list = yaml.load(f)
            dest_prefix = rss_list['dest_prefix']
            for feed_conf in rss_list['feeds']:
                rss_url = feed_conf['url']
                dest_path = dest_prefix + feed_conf['anime_name']
                feed = feedparser.parse(rss_url)
                log_stdout.print("Loaded %s feed for %s", ( feed['feed']['title'], feed_conf['anime_name'] ))
                os.makedirs(dest_path, exist_ok=True)
                for entry in feed['entries']:
                    torrent_url = entry['link']
                    t = tfile.Torrent(data=read_url(build_opener(), torrent_url), path='/dev/null')
                    log_stdout.print("Checking %s", entry['title'])
                    if not t.get_hash() in client.get_hashes():
                        client.load_torrent(t, dest_path)
                        log_stdout.print("Torrent loaded to %s", dest_path)
#                       confetti.notify(feed_conf['anime_name'], entry['title_detail']['value'])


if __name__ == "__main__":
    main()
