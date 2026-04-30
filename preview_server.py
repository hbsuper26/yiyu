import http.server
import socketserver
import os

PORT = 8081
DIRECTORY = "dist"

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def guess_type(self, path):
        # 如果文件没有扩展名，强制将其识别为 HTML 网页
        # 解决 Vercel/GitHub Pages 等正式服务器支持的无后缀路由，在本地 http.server 变下载的问题
        base, ext = os.path.splitext(path)
        if not ext:
            return 'text/html'
        return super().guess_type(path)

# 切换工作目录，防止找不到 dist 文件夹
os.chdir(os.path.dirname(os.path.abspath(__file__)))

with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
    print(f"本地预览服务器已启动：http://localhost:{PORT}")
    httpd.serve_forever()