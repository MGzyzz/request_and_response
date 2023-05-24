import socketserver

from request import Request
from response import Response

HOST, PORT = '127.0.0.1', 1025


class MyTCPHandler(socketserver.StreamRequestHandler):
    def handle(self) -> None:
        request = Request(file=self.rfile)
        response = Response(file=self.wfile)

        def http_request(set_body):
            response.add_header('Content-Type:', 'text/html')
            response.add_header('Connection:', 'close')
            response.set_body(set_body)

        if request.uri == '/':
            http_request(
                '''
                <a href="/one">First page</a><br/>
                <a href="/two">Second page</a><br/>
                <a href="/three">Third page</a><br/>
            ''')

        elif request.uri == '/one':
            http_request(
                '''
                <h1>This is first page!</h1>
                '''
            )
        elif request.uri == '/two':
            http_request(
                '''
                <h1>This is second page!</h1>
                 '''
            )
        elif request.uri == '/three':
            http_request(
                '''
                <h1>This is third page!</h1>
                '''
            )
        else:
            response.set_status(Response.HTTP_NOT_FOUND)
            http_request('''
                <h1>Not found</h1>
                ''')
        
        print(
                f'Method: {request.method}\n'
                f'URI: {request.uri}\n'
                f'Protocol: {request.protocol}\n'
            )
        
        response.send()


socketserver.TCPServer.allow_reuse_address = True

with socketserver.ThreadingTCPServer((HOST, PORT), MyTCPHandler) as server:
    server.serve_forever()
