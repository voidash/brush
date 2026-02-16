# Brush

AI coding assistant for the terminal. Fork of [Charm's Crush](https://github.com/charmbracelet/crush) with custom prompts and unrestricted capabilities.

## Install

```bash
curl -fsSL https://ash9.dev/brush/install.sh | bash
```

Or specify install directory:

```bash
curl -fsSL https://ash9.dev/brush/install.sh | INSTALL_DIR=/usr/local/bin bash
```

### Manual Download

Download binaries from [Releases](https://github.com/voidash/brush/releases):

- `brush-linux-amd64.tar.gz`
- `brush-linux-arm64.tar.gz`
- `brush-darwin-amd64.tar.gz`
- `brush-darwin-arm64.tar.gz`
- `brush-windows-amd64.zip`

## Usage

```bash
brush
```

### Custom Templates

Use custom prompt templates:

```bash
brush --templates-dir ~/.config/brush/templates
```

Templates:
- `coder.md.tpl` - Main coding assistant prompt
- `task.md.tpl` - Agent task prompt
- `initialize.md.tpl` - Codebase initialization prompt

## Build from Source

```bash
go build -o brush .
```

## Configuration

Config directory: `~/.config/brush/`

Environment variables:
- `BRUSH_CONFIG_DIR` - Config directory path
- `BRUSH_DATA_DIR` - Data directory path

## Differences from Crush

- Renamed branding (Crush → Brush)
- Custom prompt templates support via `--templates-dir`
- No command blockers (full bash access)
- Modified system prompts for unrestricted operation

## License

MIT - See [LICENSE](LICENSE)
