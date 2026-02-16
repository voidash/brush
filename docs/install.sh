#!/bin/bash
set -e

REPO="voidash/brush"
INSTALL_DIR="${INSTALL_DIR:-$HOME/.local/bin}"

# Detect OS
OS=$(uname -s | tr '[:upper:]' '[:lower:]')
case "$OS" in
    linux*)  OS="linux" ;;
    darwin*) OS="darwin" ;;
    mingw*|msys*|cygwin*) OS="windows" ;;
    *) echo "Unsupported OS: $OS"; exit 1 ;;
esac

# Detect architecture
ARCH=$(uname -m)
case "$ARCH" in
    x86_64|amd64) ARCH="amd64" ;;
    arm64|aarch64) ARCH="arm64" ;;
    *) echo "Unsupported architecture: $ARCH"; exit 1 ;;
esac

# Windows only supports amd64
if [ "$OS" = "windows" ] && [ "$ARCH" = "arm64" ]; then
    echo "Windows arm64 not supported, falling back to amd64"
    ARCH="amd64"
fi

echo "Detected: $OS-$ARCH"

# Get latest release tag
echo "Fetching latest release..."
LATEST=$(curl -sL "https://api.github.com/repos/$REPO/releases/latest" | grep '"tag_name"' | sed -E 's/.*"([^"]+)".*/\1/')

if [ -z "$LATEST" ]; then
    echo "Failed to fetch latest release. Check https://github.com/$REPO/releases"
    exit 1
fi

echo "Latest version: $LATEST"

# Determine archive name and extension
if [ "$OS" = "windows" ]; then
    ARCHIVE="brush-${OS}-${ARCH}.zip"
else
    ARCHIVE="brush-${OS}-${ARCH}.tar.gz"
fi

DOWNLOAD_URL="https://github.com/$REPO/releases/download/$LATEST/$ARCHIVE"

# Create temp directory
TMP_DIR=$(mktemp -d)
trap "rm -rf $TMP_DIR" EXIT

echo "Downloading $DOWNLOAD_URL..."
curl -sL "$DOWNLOAD_URL" -o "$TMP_DIR/$ARCHIVE"

# Extract
cd "$TMP_DIR"
if [ "$OS" = "windows" ]; then
    unzip -q "$ARCHIVE"
    BINARY="brush.exe"
else
    tar -xzf "$ARCHIVE"
    BINARY="brush"
fi

# Install
mkdir -p "$INSTALL_DIR"
mv "$BINARY" "$INSTALL_DIR/"
chmod +x "$INSTALL_DIR/$BINARY"

echo ""
echo "Installed brush to $INSTALL_DIR/$BINARY"

# Check if in PATH
if ! echo "$PATH" | grep -q "$INSTALL_DIR"; then
    echo ""
    echo "Add to your PATH:"
    echo "  export PATH=\"$INSTALL_DIR:\$PATH\""
fi

echo ""
echo "Run 'brush --help' to get started"
