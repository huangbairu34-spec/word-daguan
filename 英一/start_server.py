import http.server
import socketserver
import socket
import os
import webbrowser

PORT = 8081
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

def get_lan_ips():
    ips = []
    try:
        hostname = socket.gethostname()
        for ip in socket.gethostbyname_ex(hostname)[2]:
            if not ip.startswith('127.') and not ip.startswith('169.254.') and not ip.startswith('192.168.56.'):
                ips.append(ip)
    except Exception:
        pass
    return ips

lan_ips = get_lan_ips()

print("=" * 60)
print("  🚀 《英一单词大观》手机背诵服务已启动！")
print("=" * 60)
print("\n📱 请确保手机与电脑连接在【同一个 Wi-Fi】下：")
for ip in lan_ips:
    print(f"   👉 手机浏览器直接打开: http://{ip}:{PORT}/index.html")

print(f"\n💻 电脑本机直接打开: http://127.0.0.1:{PORT}/index.html")
print("\n💡 提示：按 Ctrl+C 可停止服务。")
print("=" * 60)

qr_urls = [f"http://{ip}:{PORT}/index.html" for ip in lan_ips]
primary_url = qr_urls[0] if qr_urls else f"http://127.0.0.1:{PORT}/index.html"

qr_html = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>手机扫码直接看 · 英一单词大观</title>
  <style>
    body {{ font-family: -apple-system, sans-serif; text-align: center; padding: 40px 20px; background: #f8fafc; color: #1e293b; }}
    .card {{ max-width: 460px; margin: 0 auto; background: white; padding: 30px; border-radius: 20px; box-shadow: 0 10px 25px rgba(0,0,0,0.08); }}
    h1 {{ color: #05683b; font-size: 22px; margin-bottom: 8px; }}
    p {{ color: #64748b; font-size: 14px; margin-bottom: 20px; }}
    img {{ width: 220px; height: 220px; margin: 10px 0; border: 1px solid #e2e8f0; border-radius: 12px; }}
    .url-box {{ background: #f1f5f9; padding: 12px; border-radius: 10px; font-family: monospace; font-size: 14px; color: #0f172a; word-break: break-all; margin-top: 15px; }}
  </style>
</head>
<body>
  <div class="card">
    <h1>📱 手机微信/相机扫码即开（英一）</h1>
    <p>请确保手机与电脑连接同一 Wi-Fi 无线网</p>
    <img src="https://api.qrserver.com/v1/create-qr-code/?size=240x240&data={primary_url}" alt="扫码打开">
    <div class="url-box">{primary_url}</div>
    <p style="margin-top: 20px; font-size: 13px;">也可以直接在手机自带浏览器中输入上方链接访问</p>
  </div>
</body>
</html>"""

with open(os.path.join(DIRECTORY, "手机扫码访问.html"), "w", encoding="utf-8") as f:
    f.write(qr_html)

try:
    webbrowser.open(f"http://127.0.0.1:{PORT}/手机扫码访问.html")
except Exception:
    pass

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n服务已安全退出。")
