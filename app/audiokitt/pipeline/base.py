import os

import magic


def fileinfo(path, audio):
    mime = magic.from_file(path, mime=True)
    size = os.path.getsize(path)

    data = {
        'fileinfo': {
            'size': size,
            'mime': '{}'.format(mime.decode()),
        }
    }

    return data
