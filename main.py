from flask import Flask, request, g,Response
import httpx
import sys

import string

app = Flask(__name__)
if len(sys.argv) > 1:
    app.config['SERVER_NAME'] = sys.argv[1]
    print(f"SERVER_NAME set to: {app.config['SERVER_NAME']}")
else:
    app.config['SERVER_NAME'] = "localhost"  # or some default/fallback
    print("No SERVER_NAME provided; using default.")



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
    host = request.host.split(':')[0]  # Remove port if present
    domain_parts = host.split('.')

    # Identify base domain (you could make this more flexible if needed)
    base_domain_parts = len(app.config['SERVER_NAME'].split('.'))  # Example: 'example.com' or 'koyeb.app'
    
    if len(domain_parts) <= base_domain_parts:
        g.origin = None
        g.url_sub = None
        return

    subdomains = domain_parts[:-base_domain_parts]
    print(f"Subdomains extracted: {subdomains}")

    try:
        if len(subdomains) >= 2:
            g.origin = decodex(subdomains[0])
            g.url_sub = decodex(subdomains[1])
        elif len(subdomains) == 1:
            g.origin = None
            g.url_sub = decodex(subdomains[0])
            if g.url_sub == "check":
                g.url_sub == "https://render-production-e2cd.up.railway.app/f22raptor"
        else:
            g.origin = None
            g.url_sub = None
    except Exception as e:
        print(f"Error decoding: {e}")
        g.origin = None
        g.url_sub = None



@app.route('/')
def index():
    origin = g.origin if g.origin else ""
    url = g.url_sub
    if not url:
        return '''
            <!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Checkmate by Velocrypt</title>
  <style>
    body {
      margin: 0;
      font-family: 'Segoe UI', sans-serif;
      background: #121212;
      color: white;
    }

    .tabs-header {
      display: flex;
      background: #1e1e1e;
      padding: 0.5em;
      border-bottom: 1px solid #333;
    }

    .tab, .new-tab-btn, .games-btn {
      padding: 0.5em 1em;
      background: #2a2a2a;
      margin-right: 0.25em;
      border-radius: 8px;
      cursor: pointer;
      transition: background 0.3s ease;
    }

    .tab.active, .tab:hover, .new-tab-btn:hover, .games-btn:hover {
      background: #3f3f3f;
    }

    .tab-close {
      margin-left: 0.5em;
      cursor: pointer;
      color: red;
    }

    .tab-content {
      position: relative;
      height: calc(100vh - 80px);
    }

    .object-container {
      position: absolute;
      top: 0; left: 0; right: 0; bottom: 0;
      transition: opacity 0.3s ease;
    }

    .object-container object {
      width: 100%;
      height: 100%;
      border: none;
    }

    .loading {
      position: absolute;
      top: 50%; left: 50%;
      transform: translate(-50%, -50%);
      display: flex;
      align-items: center;
      justify-content: center;
    }

    .loading-spinner {
      width: 24px;
      height: 24px;
      border: 4px solid #888;
      border-top-color: #fff;
      border-radius: 50%;
      animation: spin 1s linear infinite;
    }

    @keyframes spin {
      to { transform: rotate(360deg); }
    }

    .url-bar {
      background: #1a1a1a;
      padding: 0.5em;
      display: flex;
      gap: 0.5em;
      border-bottom: 1px solid #333;
    }

    #url-input {
      flex: 1;
      padding: 0.4em 0.6em;
      border-radius: 6px;
      border: none;
    }

    #submit-url-btn {
      background: #444;
      border: none;
      padding: 0.4em 0.8em;
      color: white;
      cursor: pointer;
      border-radius: 6px;
      transition: background 0.2s ease;
    }

    #submit-url-btn:hover {
      background: #666;
    }
  </style>
</head>
<body>
  <div class="tabs-header">
    <button class="games-btn" onclick="window.location.href='636865636b.velocrypt.site'">Games</button>
    <div class="new-tab-btn">+</div>
  </div>
  <div class="url-bar">
    <input type="text" id="url-input" placeholder="Enter a URL or search term" />
    <button id="submit-url-btn">Go</button>
  </div>
  <div class="tab-content"></div>

  <script>
    document.addEventListener('DOMContentLoaded', function () {
      const tabsHeader = document.querySelector('.tabs-header');
      const tabContentContainer = document.querySelector('.tab-content');
      const newTabButton = document.querySelector('.new-tab-btn');
      const tabs = [];
      let activeTabId = null;

      function generateTabId() {
        return 'tab-' + Date.now() + '-' + Math.floor(Math.random() * 1000);
      }

      function createTab(url = null) {
        const tabId = generateTabId();

        const tabElement = document.createElement('div');
        tabElement.className = 'tab';
        tabElement.dataset.tabId = tabId;
        tabElement.innerHTML = `<span class="tab-title">New Tab</span><span class="tab-close">×</span>`;
        tabsHeader.insertBefore(tabElement, newTabButton);

        const objectContainer = document.createElement('div');
        objectContainer.className = 'object-container';
        objectContainer.id = `object-container-${tabId}`;
        objectContainer.style.display = 'none';

        const objectTag = document.createElement('object');
        objectTag.type = 'text/html';

        const loadingIndicator = document.createElement('div');
        loadingIndicator.className = 'loading';
        loadingIndicator.innerHTML = '<div class="loading-spinner"></div>';

        objectContainer.appendChild(objectTag);
        objectContainer.appendChild(loadingIndicator);
        tabContentContainer.appendChild(objectContainer);

        objectTag.data = url || 'https://eldest-cicily-velocrypt-e670e25b.koyeb.app//x35';

        tabs.push({
          id: tabId,
          element: tabElement,
          objectContainer,
          objectTag,
          loadingIndicator,
          title: 'New Tab',
          url: objectTag.data
        });

        objectTag.addEventListener('load', () => {
          let title = 'New Tab';
          try {
            if (objectTag.contentDocument?.title) {
              title = objectTag.contentDocument.title;
            } else {
              const parsedUrl = new URL(objectTag.data);
              title = parsedUrl.hostname;
            }
          } catch {}
          const tab = tabs.find(t => t.id === tabId);
          if (tab) {
            tab.title = title;
            tab.element.querySelector('.tab-title').textContent = title;
            tab.loadingIndicator.style.display = 'none';
          }
        });

        objectTag.addEventListener('error', () => {
          const tab = tabs.find(t => t.id === tabId);
          if (tab) {
            tab.title = 'Page Error';
            tab.element.querySelector('.tab-title').textContent = 'Page Error';
            tab.loadingIndicator.style.display = 'none';
          }
        });

        tabElement.addEventListener('click', e => {
          if (!e.target.classList.contains('tab-close')) activateTab(tabId);
        });

        tabElement.querySelector('.tab-close').addEventListener('click', e => {
          e.stopPropagation();
          closeTab(tabId);
        });

        activateTab(tabId);
        return tabId;
      }

      function activateTab(tabId) {
        tabs.forEach(tab => {
          tab.element.classList.remove('active');
          tab.objectContainer.style.display = 'none';
        });

        const tab = tabs.find(t => t.id === tabId);
        if (tab) {
          tab.element.classList.add('active');
          tab.objectContainer.style.display = 'block';
          activeTabId = tabId;

          const urlInput = document.getElementById('url-input');
          try {
            const urlMatch = tab.url.match(/url=([^&]+)/);
            urlInput.value = urlMatch ? decodeURIComponent(urlMatch[1]) : '';
          } catch {
            urlInput.value = '';
          }
        }
      }

      function closeTab(tabId) {
        const index = tabs.findIndex(t => t.id === tabId);
        if (index === -1) return;
        const tab = tabs[index];
        tab.element.remove();
        tab.objectContainer.remove();
        tabs.splice(index, 1);

        if (activeTabId === tabId) {
          if (tabs.length > 0) {
            const newActive = Math.min(index, tabs.length - 1);
            activateTab(tabs[newActive].id);
          } else {
            createTab();
          }
        }
      }

      const urlInput = document.getElementById('url-input');
      const submitUrlBtn = document.getElementById('submit-url-btn');

      function loadUrl() {
        let inputUrl = urlInput.value.trim();
        if (!inputUrl) return;

        if (!inputUrl.startsWith('http') && inputUrl.includes('.')) {
          inputUrl = 'https://' + inputUrl;
        } else if (!inputUrl.includes('.')) {
          inputUrl = 'https://www.google.com/search?q=' + encodeURIComponent(inputUrl);
        }

        try {
          const validatedUrl = new URL(inputUrl);
          const proxyUrl = `/xorcipher?url=${encodeURIComponent(validatedUrl.href)}`;
          if (activeTabId) {
            const tab = tabs.find(t => t.id === activeTabId);
            if (tab) {
              tab.loadingIndicator.style.display = 'flex';
              tab.objectTag.data = proxyUrl;
              tab.url = proxyUrl;
            }
          }
        } catch {
          alert('Please enter a valid URL.');
        }
      }

      submitUrlBtn.addEventListener('click', loadUrl);
      urlInput.addEventListener('keydown', e => {
        if (e.key === 'Enter') loadUrl();
      });

      document.addEventListener('keydown', e => {
        if (e.ctrlKey && e.key === 't') {
          e.preventDefault();
          createTab();
        }
      });

      createTab(); // initial tab
    });
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
def main():
    app.run(debug=True, host='0.0.0.0', port=5000)
if __name__ == '__main__':
    main()
