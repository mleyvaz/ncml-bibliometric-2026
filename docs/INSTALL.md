# Installation

```bash
# Clone
git clone https://github.com/mleyvaz/ncml-bibliometric-2026.git
cd ncml-bibliometric-2026

# Virtual environment
python -m venv venv
source venv/bin/activate    # Linux/Mac
venv\Scripts\activate      # Windows

# Install dependencies
pip install -r requirements.txt
```

Tested on: Python 3.11, 3.12, 3.14 (Windows 11, Ubuntu 22.04, macOS 14).

Python 3.14 quirks: `hdbscan` wheels may be missing. The pipeline already
uses KMeans by default, so no action needed; if you want HDBSCAN topic
modeling, use Python 3.12 and `pip install bertopic`.
