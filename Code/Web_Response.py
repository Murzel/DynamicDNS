from datetime import datetime
import platform

class HTTP_Response():
    def __version(self) -> str:
        return "0.0.1"
    @property 
    def version(self) -> str:
        return self.__version()

    def __server(self) -> str:
        return 'Response/' + self.__version() + ' (' + platform.system() + ')'
    @property
    def server(self) -> str:
        return self.__server()

    @property
    def date(self) -> str:
        return datetime.now().strftime("%a, %d %b %Y %H:%M:%S GMT")

    @property
    def base_header(self) -> dict:
        return self.__base_header

    def __init__(self, connection="close"):
        self.__base_header = {
            "Date": self.date,
            "Server": self.server
        }

    def MIME_text_html(self, data : str, charset : str = "UTF-8") -> bytes:
        http = "HTTP/1.0 200 OK\r\n"

        header = {
            "Connection": "keep-alive",
            "Content-Type": "text/html" + ("; charset=" + charset if charset else "")
            }

        if data:    
            header["Content-Length"] = str(len(data.encode()))
        else:
            raise ValueError("data have to contain a message")

        header.update(self.base_header)

        for key, value in header.items():
            http += key + ": " + value + "\r\n"

        return (http + "\r\n" + (data if data else "")).encode()

    def MIME_image_favicon(self, ico):
        http = "HTTP/1.0 200 OK\r\n"

        header = {
            "Connection": "close",
            "Accept-Ranges": "bytes",
            "Content-Type": "image/x-icon"
            }

        # This will throw an error if the path of the ico is not found. -- desired behavior
        with open(ico, "rb") as f:
            icon = f.read()

        header["Content-Length"] = str(len(icon))

        header.update(self.base_header)

        for key, value in header.items():
            http += key + ": " + value + "\r\n"

        return (http + "\r\n").encode() + icon

    def MIME_image_png(self, png):
        http = "HTTP/1.0 200 OK\r\n"

        header = {
            "Connection": "close",
            "Accept-Ranges": "bytes",
            "Content-Type": "image/png"
            }

        # This will throw an error if the path of the png is not found. -- desired behavior
        with open(png, "rb") as f:
            png = f.read()

        header["Content-Length"] = str(len(png))

        header.update(self.base_header)

        for key, value in header.items():
            http += key + ": " + value + "\r\n"

        return (http + "\r\n").encode() + png

    def STATUS_not_found(self) -> bytes:
        """The requested resource could not be found but may be available in the future. Subsequent requests by the client are permissible.

        Returns:
            bytes: 404 HTTP Not Found Response
        """
        http = "HTTP/1.0 404 Not Found\r\n"
        
        header = {
            "Connection": "close"
        }

        header.update(self.base_header)

        for key, value in header.items():
            http += key + ": " + value + "\r\n"

        return (http + "\r\n").encode()
    
    def STATUS_no_content(self) -> bytes:
        """The server successfully processed the request, and is not returning any content.

        Returns:
            bytes: HTTP 204 No Content Response
        """
        http = "HTTP/1.0 204 No Content\r\n"

        header = {
            "Connection": "close"
        }

        header.update(self.base_header)

        for key, value in header.items():
            http += key + ": " + value + "\r\n"

        return (http + "\r\n").encode()