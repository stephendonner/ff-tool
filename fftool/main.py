#!/usr/bin/env python

from ff_cli import ff_cli

from firefox_download import download
from firefox_profile import create_mozprofile
from firefox_run import launch_firefox


def main():
    options = ff_cli()

    # DOWNLOAD/INSTALL
    download(options.channel)

    # If user specified `--install-only`, then just download/install specified
    # channel(s) and exit early.
    if (options.install_only):
        return

    # PROFILE
    if not options.no_profile:
        profile_path = create_mozprofile(
            options.profile,
            application=options.app,
            test_type=options.test_type,
            env=options.env
        )

    # LAUNCH
    if not options.no_launch:
        launch_firefox(profile_path, channel=options.channel)


if __name__ == '__main__':
    main()
