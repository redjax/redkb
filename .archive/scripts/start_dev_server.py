import socket
import sys
import subprocess

import logging
from logging import basicConfig

log = logging.getLogger("start_dev_server.py")


def find_free_port(start_port=8000) -> int:
    """Find a free port starting from a specific port number."""
    port = start_port
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            try:
                sock.bind(("0.0.0.0", port))

                return port
            except socket.error:
                log.info(f"Port {port} is in use, trying the next port.")
                port += 1

def run_mkdocs_serve(port: int = 8000, livereload:  bool = True):
    cmd = [
        "mkdocs",
        "serve",
        "--dev-addr",
        f"0.0.0.0:{port}",
    ]

    if livereload:
        cmd.append("--livereload")

    log.info(f"Running: {' '.join(cmd)}\n")
    log.info("Press Ctrl+C to stop the server.\n")

    try:
        ## This streams stdout/stderr directly to your terminal
        subprocess.run(cmd, check=False)
    except KeyboardInterrupt:
        log.info("\nMkDocs development server stopped by user.")


def main(livereload: bool = True):
    _port = find_free_port()
    run_mkdocs_serve(port=_port, livereload=livereload)


if __name__ == "__main__":
    logging.basicConfig(level="DEBUG", format="%(asctime)s|%(levelname)s|%(name)s :: %(message)s")

    try:
        main()
    except KeyboardInterrupt:
        log.info("User cancelled the operation")
    except Exception as exc:
        log.error(f"Failure running MkDocs development server: {exc}")
        sys.exit(1)
