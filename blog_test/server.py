import wsgiref.simple_server
import controller

server = wsgiref.simple_server.make_server('', 8000, controller.App)
server.serve_forever()
