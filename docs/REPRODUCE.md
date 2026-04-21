# Reproducing the analysis

1. Clone the repo and install dependencies (see README).
2. Ensure network access (scripts 01, 03 fetch from the web).
3. Run scripts in numeric order (01 through 22).
4. Expect ~30 min end-to-end on a modern laptop.

## Troubleshooting

- **UnicodeEncodeError on Windows**: each script uses `sys.stdout.reconfigure`
  but if you run via `python -X utf8 script.py` it is even safer.
- **hdbscan wheel fails on Python 3.14**: the pipeline uses KMeans instead
  (not HDBSCAN). If you want HDBSCAN, downgrade to Python 3.12.
- **OpenAlex rate limit**: the default 8 threads stay below the polite
  pool; if you get 429s, reduce `max_workers` in `03_fetch_apis.py`.
- **Scholar CAPTCHA**: `06_scholar_sample.py` stops on detection; run it
  from a residential IP, not a cloud VM.
