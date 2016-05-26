from rest_framework.parsers import FileUploadParser, MultiPartParser, FormParser


class MultiPartFileUploadParser(MultiPartParser, FileUploadParser, FormParser):
    pass
