#!/usr/bin/env python

import os
from firefox_env_handler import IniHandler
from fabric.api import local
from outlawg import Outlawg
from fftool import DIR_TEMP_BROWSERS as BASE_DIR, OS_CONFIG as env
from subprocess import Popen, PIPE

out = Outlawg()


def install(channel):
    if channel == 'ALL':
        install_all()
        return

    install_dir = env.get(channel, 'PATH_FIREFOX_APP')
    filename = env.get(channel, 'DOWNLOAD_FILENAME')
    installer = os.path.join(BASE_DIR, filename)

    if IniHandler.is_linux():
        local('tar -jxf {0} && mv firefox {1}'.format(installer, install_dir))  # NOQA

    elif IniHandler.is_windows():
        # TODO: this needs improvement
        local('chmod +x {0}'.format(installer))
        local('{0} -ms'.format(installer))

        if channel == 'beta':
            # Since Beta and General Release channels install
            # to the same directory, install Beta first then
            # rename the directory.
            gr_install_dir = env.config.get('release', 'PATH_FIREFOX_APP')
            local('mv {0} {1}'.format(gr_install_dir, install_dir))

    elif IniHandler.is_mac():
        from hdiutil import extract_dmg

        app_src_filename = env.get(channel, "APP_SRC_FILENAME")
        app_dest_filename = env.get(channel, "APP_DEST_FILENAME")

        extract_dmg(installer, app_src_filename, app_dest_filename, channel)
    try:
        firefox_version = get_firefox_version(channel)
    except:
        print("YOU FAIL")

    out.header("Installed {0} ({1})".format(firefox_version, channel))


def get_firefox_version(channel):
    path_firefox_bin = env.get(channel, "PATH_FIREFOX_BIN_ENV")
    # PATH_FIREFOX_BIN_ENV = 'C:/Program Files/Nightly/firefox.exe'
    # PATH_FIREFOX_BIN_ENV = '/cygdrive/c/Program\ Files/Nightly/firefox.exe'
    # path_firefox_bin = env.get(channel, "PATH_FIREFOX_BIN_ENV")
    # path_firefox_bin = PATH_FIREFOX_BIN_ENV
    # cmd = "{0} --version".format(path_firefox_bin)
    output = Popen([path_firefox_bin, "--version"], stdout=PIPE, shell=True)
    return output.stdout.read().strip()
    # return local(cmd, capture=True)


def install_all():
    for channel in env.sections():
        install(channel)


def main():
    install_all()


if __name__ == '__main__':
    main()
