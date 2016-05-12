import hashlib

def md5_for_file(file):

    md5 = hashlib.md5()
    for chunk in file.chunks():
        md5.update(chunk)

    return md5.hexdigest()