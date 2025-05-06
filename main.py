from flask import Flask, request, g,Response
import httpx
import string

app = Flask(__name__)
app.config['SERVER_NAME'] = 'eldest-cicily-velocrypt-e670e25b.koyeb.app'


def decodex(hex_str):
    try:
        # Convert hex string to bytes
        bytes_data = bytes.fromhex(hex_str)

        # Convert bytes to string (UTF-8 decoding)
        decoded_string = bytes_data.decode('utf-8', errors='ignore')

        return decoded_string
    except ValueError as e:
        return f"Error decoding hex: {e}"

@app.before_request
def extract_subdomains():
    print("Processing request...")
    host = request.host.split(':')[0]  # Split off the port number if present
    parts = host.split('.')  # Split by dot to get subdomains
    subdomains = parts[:-3]  # Subdomains are all parts except the last two (domain and TLD)

    print(f"Subdomains extracted: {subdomains}")

    try:
        if len(subdomains) == 2:
            print("Decoding two subdomains...")
            g.origin = decodex(subdomains[0])  # Decode the first subdomain
            g.url_sub = decodex(subdomains[1])  # Decode the second subdomain
        elif len(subdomains) == 1:
            print("Decoding one subdomain...")
            g.origin = None
            g.url_sub = decodex(subdomains[0])  # Decode the first subdomain
        else:
            g.origin = None
            g.url_sub = None
            print("No subdomains found.")
    except Exception as e:
        g.origin = None
        g.url_sub = None
        print(f"Error decoding subdomains: {e}")


@app.route('/')
def index():
    origin = g.origin if g.origin else ""
    url = g.url_sub
    if not url:
        return '''
            <!DOCTYPE html>
            <html>
            <head>
                <title>Hex Proxy Launcher</title>
                <style>
                    body { font-family: Arial, sans-serif; padding: 2rem; }
                    input, button { padding: 0.5rem; width: 100%; margin: 0.5rem 0; }
                    iframe { width: 100%; height: 600px; border: 1px solid #ccc; margin-top: 1rem; }
                    pre { background: #eee; padding: 0.5rem; overflow-x: auto; }
                </style>
            </head>
            <body>
                <h1>Hex-Encoded Subdomain Proxy</h1>
                <p>Enter a URL to encode it twice and load via iframe from <code>*.mything.com</code></p>

                <input type="text" id="urlInput" placeholder="e.g., zombsroyale.io">
                <button onclick="loadIframe()">Launch</button>

                <h3>Encoded Subdomain</h3>
                <pre id="encodedResult"></pre>

                <h3>iframe Output</h3>
                <iframe id="proxyFrame" src=""></iframe>

                <script>
                function stringToHex(input) {
                    let hexStr = '';
                    for (let i = 0; i < input.length; i++) {
                        hexStr += input.charCodeAt(i).toString(16);
                    }
                    return hexStr;
                }

                function loadIframe() {
                    let userInput = document.getElementById("urlInput").value.trim();

                    if (!userInput) {
                        alert("Please enter a URL");
                        return;
                    }

                    if (!userInput.startsWith("https://")) {
                        userInput = "https://" + userInput;
                    }

                    const encoded = stringToHex(userInput);
                    const doubleEncoded = encoded;

                    const subdomain = `${encoded}.${doubleEncoded}.eldest-cicily-velocrypt-e670e25b.koyeb.app/`;

                    // For viewing the generated object
                    const data = {
                        url: subdomain
                    };

                    document.getElementById("encodedResult").textContent = JSON.stringify(data, null, 2);

                    // Update iframe
                    document.getElementById("proxyFrame").src = "http://" + subdomain + "/";
                }
                </script>
            </body>
            </html>
            '''
    headers = {
        "Origin": origin,
        "Accept-Encoding": "identity"
    }

    resp = httpx.request(url=url, method=request.method, headers=headers)

    excluded_headers = {
        'content-encoding', 'transfer-encoding', 'connection',
        'content-length', 'x-frame-options', 'server',
        'set-cookie', 'date', 'alt-svc', 'cf-cache-status',
        'cf-ray', 'nel', 'report-to', 'server-timing'
    }

    fixed_headers = {
        k: v for k, v in resp.headers.items()
        if k.lower() not in excluded_headers
    }

    return Response(
        resp.content,
        status=resp.status_code,
        headers=fixed_headers,
        mimetype=resp.headers.get("Content-Type")
    )
@app.route('/<path:path>')
def indexs(path):
    origin = g.origin if g.origin else ""
    url = g.url_sub + f"/{path}"
    headers = {
        "Origin": origin,
        "Accept-Encoding": "identity"
    }

    resp = httpx.request(url=url, method=request.method, headers=headers)

    excluded_headers = {
        'content-encoding', 'transfer-encoding', 'connection',
        'content-length', 'x-frame-options', 'server',
        'set-cookie', 'date', 'alt-svc', 'cf-cache-status',
        'cf-ray', 'nel', 'report-to', 'server-timing'
    }

    fixed_headers = {
        k: v for k, v in resp.headers.items()
        if k.lower() not in excluded_headers
    }

    return Response(
        resp.content,
        status=resp.status_code,
        headers=fixed_headers,
        mimetype=resp.headers.get("Content-Type")
    )
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
