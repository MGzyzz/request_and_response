from typing import BinaryIO


class Request:
    def __init__(self, file: BinaryIO) -> None:
        self.file = file
        self.body = self.method = self.uri = self.protocol = ''
        self.headers = {}

        self.parse_request_line()
        self.parse_headers()
        self.parse_body()

    def readline(self):
        return self.file.readline().decode().strip()

    def parse_request_line(self) -> None:
        request_line = self.readline()

        self.method, self.uri, self.protocol = request_line.split()

    def parse_headers(self) -> None:
        while True:
            header = self.readline()

            if not header:
                break

            header_name, header_value = header.split(': ')
            self.headers[header_name] = header_value

    def parse_body(self) -> None:
        if 'Content-Length' in self.headers:
            content_length = int(self.headers['Content-Length'])
            self.body = self.file.read(content_length)
