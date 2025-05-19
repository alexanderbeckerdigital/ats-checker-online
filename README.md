# ats-checker-online 🚦🤖

A super-fast, modular, and extendable ATS checker for job application URLs –  
built as a Flask web app. Instantly reveals which Applicant Tracking System (ATS) is behind any job posting.

---

## 🚀 Features

- **String-Matching:** Instantly detects ATS from the URL itself
- **Deep-Scan:** Analyzes the live HTML source to find hidden ATS markers
- **Grouped Output:** All checked URLs are grouped by ATS system
- **Special Warnings** for "annoying" systems like SAP or Workwise ☠️
- **Clear All:** Quickly reset input and results with one click
- **Runs 100% locally** – nothing is stored or sent externally

---

## 🛠 Installation

**Requirements:** Python 3.x

```bash
git clone https://github.com/YOURUSERNAME/ats-checker-online.git
cd ats-checker-online
python3 -m venv venv
source venv/bin/activate
pip install flask requests beautifulsoup4

