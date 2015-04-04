#!/usr/bin/env python3.4

import sys
import argparse

from emonoda import tfile

from emonoda.apps import init
from emonoda.apps import get_configured_log
from emonoda.apps import get_configured_client
from emonoda import tfile


# ===== Main =====
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
            log_stdout.print("%s", (client,))
            t = tfile.Torrent(path="/home/goblinqueen/emonoda-rss/test.torrent")
            print(t)
            client.load_torrent(t, '/media/Elements/Anime')


if __name__ == "__main__":
    main()
