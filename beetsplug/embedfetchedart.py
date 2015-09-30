# This file is part of beets.
# Copyright 2012, Steven Armstrong
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.

"""Allows beets to embed album art into file metadata."""
import logging
import os
import imghdr

from beets.plugins import BeetsPlugin
from beets import mediafile
from beets import ui
from beets.ui import decargs
from beets.util import syspath, normpath

from beetsplug import embedart

log = logging.getLogger('beets')


class EmbedFetchedArtPlugin(BeetsPlugin):
    """Allows already fetched albumart to be embedded into the actual files."""

    def commands(self):
        # Embed command.
        cmd = ui.Subcommand('embedfetchedart',
            help='embed already fetched images into file metadata')
        cmd.parser.add_option('-r', '--remove', dest='remove',
                              action='store_true', default=False,
                              help='remove artwork image file after embedding')

        def func(lib, config, opts, args):
            embed_fetched_art(lib, lib.albums(ui.decargs(args)), opts.remove)
        cmd.func = func

        return [cmd]

# "embedfetchedart" command.
def embed_fetched_art(lib, albums, remove):
    for album in albums:
        log.info(u'{0} - {1}'.format(album.albumartist, album.album))
        if album.artpath:
            log.info(u'  has album art, embedding')
            embedart._embed(album.artpath, album.items())
            if remove:
                log.info(u'  removing art from db and file system')
                os.remove(album.artpath)
                album.artpath = ''
        else:
            log.info(u'  no art found')
