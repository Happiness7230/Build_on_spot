from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
import os

class SimpleCalcServer(BaseHTTPRequestHandler):
    
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open("calculator.html", "r", encoding="utf-8") as f:
                html = f.read().replace("{{ result }}", "Waiting for input...")
                self.wfile.write(bytes(html, "utf-8"))

    def do_POST(self):
        if self.path == '/calculate':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            fields = urllib.parse.parse_qs(post_data)
            
            try:
                # 1. Force strings from HTML to become STRICT integers
                num1 = int(fields.get('num1'))
                num2 = int(fields.get('num2'))
                operation = fields.get('operation')
                
                # 2. --- ARITHMETIC CORE (INTEGERS ONLY) ---
                if operation == 'add':
                    result = num1 + num2
                elif operation == 'subtract':
                    result = num1 - num2
                elif operation == 'multiply':
                    result = num1 * num2
                elif operation == 'divide':
                    if num2 == 0:
                        result = "Error (Cannot divide by zero)"
                    else:
                        # Use // for Floor Division to ensure an integer answer
                        # Example: 5 // 2 will equal 2 instead of 2.5
                        result = num1 // num2 
                else:
                    result = "Unknown error"
            except (TypeError, ValueError, IndexError):
                result = "Invalid Input (Integers only)"

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            with open("calculator.html", "r", encoding="utf-8") as f:
                html = f.read().replace("{{ result }}", str(result))
                self.wfile.write(bytes(html, "utf-8"))

if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    server = HTTPServer(('localhost', 8000), SimpleCalcServer)
    print("Integer-only Calculator running at http://localhost:8000")
    server.serve_forever()
  
