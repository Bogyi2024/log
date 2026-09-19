"""
cm720-next.py  -  multi-host downloader for the H2S / CM pipeline.

What changed vs. the version embedded (base64) in directcm720customdual2-next.bat:

  1. POLITENESS.  aria2 now opens 2 connections per server instead of 16 and
     only 1 file at a time.  The old "--split=16 --max-connection-per-server=16"
     burst is what made megadl.boats answer HTTP 429 and drop episodes 2-4.

  2. RETRIES WITH REAL BACK-OFF.  Each URL gets up to DOWNLOAD_ATTEMPTS outer
     attempts, waiting 45s, 90s, 180s ... between them, on top of aria2's own
     --max-tries/--retry-wait.  A 429 needs time to clear; retrying instantly
     with the same settings can never succeed.

  3. VERIFICATION.  Every URL must finish successfully.  If any link failed the
     script prints a summary and exits with status 1, so the GitHub job goes RED
     instead of quietly emailing a partial batch (that is how 1 of 4 episodes
     was delivered last time).

  4. Useful logging: per-URL result, files added, and a final recap.

Environment (all optional, sensible defaults):
    LINKS_CONTENT            newline separated links (required)
    OUTPUT_PATH              download dir                     (default source/)
    DOWNLOAD_ATTEMPTS        outer attempts per URL           (default 4)
    DOWNLOAD_BACKOFF_START   seconds before first retry       (default 45)
    DOWNLOAD_BACKOFF_FACTOR  back-off multiplier              (default 2)
    DOWNLOAD_DELAY_SECONDS   pause between two URLs           (default 20)
    ARIA2_CONNECTIONS        connections per server          (default 2)
    ARIA2_SPLIT              aria2 split count               (default 2)
"""

import os
import re
import subprocess
import sys
import time

import gdown
import mediafire_dl

OUTPUT_PATH = os.getenv("OUTPUT_PATH", "source/")

OUTER_ATTEMPTS = int(os.getenv("DOWNLOAD_ATTEMPTS", "4"))
BACKOFF_START = int(os.getenv("DOWNLOAD_BACKOFF_START", "45"))
BACKOFF_FACTOR = float(os.getenv("DOWNLOAD_BACKOFF_FACTOR", "2"))
DELAY_BETWEEN_FILES = int(os.getenv("DOWNLOAD_DELAY_SECONDS", "20"))

ARIA2_CONNECTIONS = int(os.getenv("ARIA2_CONNECTIONS", "2"))
ARIA2_SPLIT = int(os.getenv("ARIA2_SPLIT", "2"))
ARIA2_MIN_SPLIT = os.getenv("ARIA2_MIN_SPLIT_SIZE", "5M")

# Some free file hosts reject their own hosting nodes when the client claims to
# be "aria2/..." . A browser UA avoids that class of refusal.
USER_AGENT = os.getenv(
    "DOWNLOAD_USER_AGENT",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/125.0 Safari/537.36",
)

MEDIA_EXTENSIONS = (
    ".mp4", ".mkv", ".m4v", ".avi", ".mov", ".ts", ".webm", ".flv", ".wmv",
    ".rar", ".zip", ".7z", ".srt", ".ass", ".vtt",
)


def extract_google_drive_id(url):
    """Extract a Google Drive file or folder ID from the usual URL shapes."""
    pattern = re.compile(
        r"drive.google.com/.*?(?:file/d/|drive/folders/|open\?id=|uc\?id=)([^/&?]+)"
    )
    match = pattern.search(url)
    return match.group(1) if match else None


def snapshot(folder):
    """Set of finished files in `folder` (aria2 .aria2 control files excluded)."""
    try:
        return {n for n in os.listdir(folder) if not n.endswith(".aria2")}
    except OSError:
        return set()


def report_added(before):
    """Log files that appeared since `before`. Purely informational."""
    added = sorted(snapshot(OUTPUT_PATH) - before)
    if added:
        print("  -> added: " + ", ".join(added))
    return added


def leftover_control_files(folder):
    try:
        return [n for n in os.listdir(folder) if n.endswith(".aria2")]
    except OSError:
        return []


def aria2_executable():
    """aria2c.exe sits next to this script (the .bat downloads it there)."""
    here = os.path.dirname(os.path.abspath(__file__))
    for candidate in (
        os.path.join(here, "aria2c.exe"),
        os.path.join(os.getcwd(), "aria2c.exe"),
        "aria2c.exe",
    ):
        if os.path.isfile(candidate) or candidate == "aria2c.exe":
            return candidate
    return "aria2c.exe"


def run_aria2(url):
    """One aria2 attempt. Returns True when the transfer really finished."""
    os.makedirs(OUTPUT_PATH, exist_ok=True)
    before = snapshot(OUTPUT_PATH)

    command = [
        aria2_executable(),
        "--continue=true",
        "--content-disposition=true",
        "--dir=" + OUTPUT_PATH,
        "--max-connection-per-server=%d" % ARIA2_CONNECTIONS,
        "--split=%d" % ARIA2_SPLIT,
        "--min-split-size=" + ARIA2_MIN_SPLIT,
        "--max-concurrent-downloads=1",
        "--max-tries=10",
        "--retry-wait=20",
        "--timeout=60",
        "--connect-timeout=30",
        "--user-agent=" + USER_AGENT,
        "--console-log-level=warn",
        "--summary-interval=0",
        url,
    ]
    print("  aria2c: " + " ".join(command))
    result = subprocess.run(command)
    report_added(before)

    if result.returncode != 0:
        print("  -> aria2c exit code %d" % result.returncode)
        return False

    controls = leftover_control_files(OUTPUT_PATH)
    if controls:
        print("  -> incomplete transfer, control file(s) left: " + ", ".join(controls))
        return False

    return True


def run_wget(url):
    os.makedirs(OUTPUT_PATH, exist_ok=True)
    before = snapshot(OUTPUT_PATH)
    result = subprocess.run(["wget", "-P", OUTPUT_PATH, url])
    report_added(before)
    if result.returncode != 0:
        print("  -> wget exit code %d" % result.returncode)
        return False
    return True


def run_curl(url):
    os.makedirs(OUTPUT_PATH, exist_ok=True)
    before = snapshot(OUTPUT_PATH)
    result = subprocess.run(["curl", "-fL", "-O", "-J", "--create-dirs", url],
                            cwd=OUTPUT_PATH)
    report_added(before)
    if result.returncode != 0:
        print("  -> curl exit code %d" % result.returncode)
        return False
    return True


def run_gdown(file_id):
    os.makedirs(OUTPUT_PATH, exist_ok=True)
    before = snapshot(OUTPUT_PATH)
    try:
        gdown.download(id=file_id, output=OUTPUT_PATH, quiet=False)
    except Exception as error:                                  # noqa: BLE001
        print("  gdown file download failed (%s). Trying as folder..." % error)
        try:
            gdown.download_folder(id=file_id, output=OUTPUT_PATH, quiet=False,
                                  resume=True)
        except Exception as folder_error:                       # noqa: BLE001
            print("  gdown folder download failed: %s" % folder_error)
            return False
    report_added(before)
    return True


def run_mediafire(url):
    os.makedirs(OUTPUT_PATH, exist_ok=True)
    before = snapshot(OUTPUT_PATH)

    target = url
    if url.startswith("https://download"):
        parts = url.split("/")
        if len(parts) < 6:
            print("  MediaFire raw link format not recognised.")
            return False
        target = "https://www.mediafire.com/file/%s/%s" % (parts[-2], parts[-1])
    elif "mediafire.com" not in url:
        return False

    previous_dir = os.getcwd()
    try:
        os.chdir(OUTPUT_PATH)
        mediafire_dl.download(target, quiet=False)
    except Exception as error:                                  # noqa: BLE001
        print("  MediaFire download failed: %s" % error)
        return False
    finally:
        os.chdir(previous_dir)

    report_added(before)
    return True


def attempt_once(url):
    """Route one URL to the right tool. True = file really arrived."""
    file_id = extract_google_drive_id(url)
    try:
        if file_id:
            print("  host: Google Drive (%s)" % file_id)
            return run_gdown(file_id)
        if "msubb2.net" in url:
            print("  host: msubb2.net (wget)")
            return run_wget(url)
        if "workers" in url:
            print("  host: workers (curl)")
            return run_curl(url)
        if url.startswith("https://download") or "mediafire.com" in url:
            print("  host: MediaFire")
            return run_mediafire(url)

        print("  host: generic direct link (aria2c)")
        return run_aria2(url)
    except FileNotFoundError as error:
        print("  required tool not found: %s" % error)
        return False
    except Exception as error:                                  # noqa: BLE001
        print("  unexpected error: %s" % error)
        return False


def main():
    links_content = os.getenv("LINKS_CONTENT") or ""
    links = [line.strip() for line in links_content.splitlines() if line.strip()]

    if not links:
        print("ERROR: LINKS_CONTENT environment variable is missing or empty.")
        return 1
    print("Loaded %d links from environment variable." % len(links))

    os.makedirs(OUTPUT_PATH, exist_ok=True)

    failed = []
    for index, url in enumerate(links, start=1):
        print("\n--- [%d/%d] Processing URL: %s ---" % (index, len(links), url))

        delay = BACKOFF_START
        for attempt in range(1, OUTER_ATTEMPTS + 1):
            print("Attempt %d/%d" % (attempt, OUTER_ATTEMPTS))
            if attempt_once(url):
                print("OK: download finished.")
                break

            if attempt == OUTER_ATTEMPTS:
                print("FAILED after %d attempts: %s" % (OUTER_ATTEMPTS, url))
                failed.append(url)
                break

            print("Retrying in %ds (the host may be rate limiting us)..."
                  % delay)
            time.sleep(delay)
            delay = int(delay * BACKOFF_FACTOR)

        if index < len(links) and DELAY_BETWEEN_FILES:
            print("Pausing %ds before the next link..." % DELAY_BETWEEN_FILES)
            time.sleep(DELAY_BETWEEN_FILES)

    files = sorted(snapshot(OUTPUT_PATH))
    print("\n================ DOWNLOAD SUMMARY ================")
    print("Links requested : %d" % len(links))
    print("Links failed    : %d" % len(failed))
    for url in failed:
        print("   FAILED  %s" % url)
    print("Files in %s:" % OUTPUT_PATH)
    for name in files:
        print("   %s" % name)
    print("=================================================")

    if failed:
        print("\nERROR: %d of %d downloads failed - refusing to continue with a "
              "partial batch." % (len(failed), len(links)))
        return 1

    print("\nDownload script finished - all %d links are complete." % len(links))
    return 0


if __name__ == "__main__":
    sys.exit(main())
