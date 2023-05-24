from typing import BinaryIO

from os import fstat


class Response:
    HTTP_OK = 200
    HTTP_BAD_REQUEST = 400
    HTTP_NOT_FOUND = 404
    HTTP_INTERNAL_SERVER_ERROR = 500

    MESSAGES = {
        HTTP_OK: 'OK',
        HTTP_BAD_REQUEST: 'Bad Request',
        HTTP_NOT_FOUND: 'Not Found',
        HTTP_INTERNAL_SERVER_ERROR: 'Internal Server Error'
    }

    PROTOCOL = 'HTTP/1.1'

    def __init__(self, file: BinaryIO) -> None:
        self.file = file
        self.__status = self.HTTP_OK
        self.__headers: list[dict] = []
        self.body = None
        self.file_body = None

    def set_status(self, new_status: int) -> None:
        self.__status = new_status

    def set_body(self, body: str) -> None:
        self.body = body.encode()
        self.add_header('Content-Type', str(len(self.body)))

    def set_file_body(self, file: BinaryIO) -> None:
        self.file_body = file
        size = fstat(file.fileno()).st_size
        self.add_header('Content-Length', str(size))

    def add_header(self, name: str, value: str) -> None:
        self.__headers.append({name: value})

    def __get_status_line(self) -> str:
        message = self.MESSAGES[self.__status]
        return f'{self.PROTOCOL} {self.__status} {message}'

    def __get_response_head(self) -> bytes:
        status_line = self.__get_status_line()

        # for example
        # headers = [': '.join(list(*header.items())) for header in self.__headers]
        # print(headers)
        # /for example

        headers: list[str] = []
        for header in self.__headers:
            k, v = list(*header.items())
            headers.append(f'{k}: {v}')

        head_str = '\r\n'.join([status_line] + headers)
        head_str += '\r\n\r\n'

        return head_str.encode()

    def __write_file_body(self) -> None:
        # Chunk load
        while True:
            data = self.file_body.read(1024)
            if not data:
                break

            self.file.write(data)

    def send(self):
        head = self.__get_response_head()
        self.file.write(head)

        if self.body:
            self.file.write(self.body)
        elif self.file_body:
            self.__write_file_body()
