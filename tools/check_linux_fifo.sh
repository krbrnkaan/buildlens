#!/bin/sh
# Keep a native Linux filesystem inside the checkout and a private mount namespace.
set -eu
cd "$(dirname "$0")/.."
mkdir -p .tmp/fifo-fs
exec unshare --user --map-root-user --mount --propagation private -- sh -eu -c '
    mount -t tmpfs -o size=16m,nodev,nosuid,noexec tmpfs .tmp/fifo-fs
    trap "umount .tmp/fifo-fs" EXIT
    "$1" -m pytest tests/test_hardening.py tests/test_release.py -q -rs \
        -k "fifo or replaced_descriptor or symlink" \
        --basetemp=.tmp/fifo-fs/pytest -o cache_dir=.tmp/fifo-cache
' sh "${1:-.venv-linux/bin/python}"
