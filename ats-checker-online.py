# -*- coding: utf-8 -*-
from flask import Flask, render_template_string, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

ATS_LIST = {
    "Greenhouse": ["greenhouse.io"],
    "SAP SuccessFactors ☠️": ["successfactors", "jobs.sap.com"],
    "Workwise ☠️": ["workwise.io"],
    "SmartRecruiters": ["smartrecruiters.com"],
    "Workday": ["myworkdayjobs.com", "workday.com"],
}

def detect_ats_url(url):
    for ats, patterns in ATS_LIST.items():
        for pattern in patterns:
            if pattern in url:
                return ats
    return None

def deep_scan(url):
    try:
        print(f"Starte Scan für: {url}")
        resp = requests.get(url, timeout=10)
        html = resp.text
        soup = BeautifulSoup(html, "html.parser")
        scripts_and_links = []
        for tag in soup.find_all(["script", "link"]):
            if tag.has_attr('src'):
                scripts_and_links.append(tag['src'])
            if tag.has_attr('href'):
                scripts_and_links.append(tag['href'])
            if tag.string:
                scripts_and_links.append(tag.string)
        scripts_and_links = [s for s in scripts_and_links if s]

        metas = []
        for tag in soup.find_all("meta"):
            if tag.has_attr('content'):
                metas.append(tag['content'])
        metas = [m for m in metas if m]

        candidates = scripts_and_links + metas + [html]

        for ats, patterns in ATS_LIST.items():
            for pattern in patterns:
                for c in candidates:
                    if c and pattern in c:
                        print(f"Fertig: {url} → {ats}")
                        return ats
        print(f"Fertig: {url} → Unbekannt")
        return "Unbekannt"
    except Exception as e:
        print(f"Fehler bei {url}: {e}")
        return f"Fehler: {e}"

@app.route('/', methods=['GET', 'POST'])
def index():
    urls = ""
    grouped = {}
    deep_scan_mode = False
    if request.method == 'POST':
        if 'clear' in request.form:
            urls = ""
            grouped = {}
        else:
            urls = request.form.get('urls', '')
            lines = [u.strip() for u in urls.splitlines() if u.strip()]
            if 'deep' in request.form:
                deep_scan_mode = True
                for url in lines:
                    ats = detect_ats_url(url)
                    if not ats:
                        ats = deep_scan(url)
                    grouped.setdefault(ats, []).append(url)
            else:
                for url in lines:
                    ats = detect_ats_url(url)
                    if not ats:
                        ats = "Unbekannt"
                    grouped.setdefault(ats, []).append(url)
    return render_template_string("""
    <html>
    <head>
        <title>ATS-Checker (Deep-Scan)</title>
        <style>
            body { font-family: Arial; margin: 40px; }
            .container { display: flex; gap: 40px; }
            textarea { width: 400px; height: 400px; }
            .output { border: 1px solid #ccc; padding: 20px; min-width: 350px; }
            .ats-title { margin-top: 20px; font-size: 1.2em; }
            .ats-bad { color: red; }
        </style>
    </head>
    <body>
        <h2>ATS-Checker – Deep-Scan (URLs werden live analysiert)</h2>
        <form method="post" id="atsform" onsubmit="showSpinner()">
            <div class="container">
                <div>
                    <b>URL-Eingabe (jede Zeile eine URL):</b><br>
                    <textarea name="urls" placeholder="https://...">{{urls}}</textarea><br>
                    <button type="submit">String-Matching</button>
                    <button type="submit" name="deep" value="1">Deep-Scan</button>
                    <button type="submit" name="clear" value="1">Clear All</button>
                </div>
                <div class="output">
                    {% if grouped %}
                        <b>Ergebnis ({{'Deep-Scan' if deep_scan_mode else 'String-Matching'}}):</b>
                        {% for ats, urls in grouped.items() %}
                            <div class="ats-title {% if '☠️' in ats %}ats-bad{% endif %}">{{ats}}</div>
                            <ul>
                                {% for url in urls %}
                                    <li>{{url}}</li>
                                {% endfor %}
                            </ul>
                        {% endfor %}
                    {% else %}
                        <i>Hier erscheinen die gruppierten Ergebnisse.</i>
                    {% endif %}
                </div>
            </div>
        </form>
        <div id="spinner" style="display:none; font-size:1.3em; color:#1a73e8;">
            <b>🔄 Scan läuft... Bitte warten...</b>
        </div>
        <script>
        function showSpinner() {
            document.getElementById('spinner').style.display = 'block';
        }
        </script>
    </body>
    </html>
    """, urls=urls, grouped=grouped, deep_scan_mode=deep_scan_mode)

if __name__ == "__main__":
    app.run(debug=True)
