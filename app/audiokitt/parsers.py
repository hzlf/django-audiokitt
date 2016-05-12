from rest_framework.parsers import FileUploadParser, MultiPartParser, FormParser, JSONParser

class MultiPartFileUploadParser(MultiPartParser, FileUploadParser, FormParser):

    pass