import threading
import time
import subprocess
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
CLAUDE_PATH = r"C:\Users\mrudu\AppData\Local\Microsoft\WinGet\Packages\Anthropic.ClaudeCode_Microsoft.Winget.Source_8wekyb3d8bbwe\claude.exe"

WATCH_DIR = "src"          # folder to watch
TEST_DIR = "tests"       # where test files go
IGNORE = {"watch_and_test.py", "agent_generate_tests.py"}

class PyFileHandler(FileSystemEventHandler):
    def __init__(self):
        self._running = set()  # track files currently being processed
        self._lock = threading.Lock()

    def on_modified(self, event):
        self.handle(event)

    def on_created(self, event):
        self.handle(event)

    def handle(self, event):
        path = event.src_path

        # Skip if already processing this file
        with self._lock:
            if path in self._running:
                return
            self._running.add(path)

        # Only act on .py files, skip test files and ignored files
        if not path.endswith(".py"):
            return
        if os.path.basename(path).startswith("test_"):
            return
        if os.path.basename(path) in IGNORE:
            return
        if path.startswith(f".{os.sep}{TEST_DIR}"):
            return

        filename = os.path.basename(path)
        test_filename = f"test_{filename}"
        test_path = os.path.join(TEST_DIR, test_filename)

        print(f"\n🔍 Change detected in: {filename}")
        print(f"🤖 Asking Claude to update: {test_path}")

        # Read the source file ourselves and pass it in the prompt
        with open(path, "r") as f:
            source_code = f.read()

        prompt = (
            f"You are a Python testing expert. "
            f"Read the following Python source code and generate comprehensive pytest unit tests.\n"
            f"Rules:\n"
            f"- Use pytest style (no unittest classes)\n"
            f"- Cover normal cases, edge cases, and error/exception cases\n"
            f"- Use descriptive test function names\n"
            f"- Add this import at the top: import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))\n"
            f"- Import from src.{filename[:-3]}\n"
            f"- Output ONLY raw Python code, no markdown, no explanation\n\n"
            f"Source code:\n{source_code}"
        )

        result = subprocess.run(
            [CLAUDE_PATH, "--print", prompt],
            capture_output=True,
            text=True,
            shell=False
        )

        if result.returncode == 0 and result.stdout.strip():
            # Strip markdown fences if Claude includes them
            output = result.stdout.strip()
            if output.startswith("```"):
                output = "\n".join(output.split("\n")[1:])  # remove first line
            if output.endswith("```"):
                output = "\n".join(output.split("\n")[:-1])  # remove last line

            with open(test_path, "w") as f:
                f.write(output)
            print(f"✅ Tests written to {test_path}")

            # Auto-run the tests immediately
            print(f"🧪 Running tests...")
            test_result = subprocess.run(
                ["pytest", test_path, "-v"],
                capture_output=False
            )
        else:
            print(f"❌ Claude returned no output or errored:")
            print(f"   stdout: {result.stdout[:200]}")
            print(f"   stderr: {result.stderr[:200]}")

         # Always release when done, even if it errored
        with self._lock:
            self._running.discard(path)

if __name__ == "__main__":
    os.makedirs(TEST_DIR, exist_ok=True)
    print(f"👀 Watching for changes in '{WATCH_DIR}'...")
    print("   Save any .py file to auto-generate its tests. Ctrl+C to stop.\n")

    observer = Observer()
    observer.schedule(PyFileHandler(), path=WATCH_DIR, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()