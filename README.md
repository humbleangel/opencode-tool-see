# opencode-tool-see

OpenCode custom tool: give the agent eyes. Reads a local image or PDF file and returns a MiMo-V2.5 vision description (via OpenCode Zen, fallback OpenCode Go).

## Files

- `see.py` — reads `{file, prompt}` JSON from stdin, sends base64 data-URI to an OpenAI-compatible chat endpoint, prints `{success, text}` JSON
- `see.ts` — OpenCode plugin wrapper (spawns `python see.py`)
- `see.json` — tool manifest

## Params

- `file`: absolute path to the image or PDF (required)
- `prompt`: instruction for the vision model (default `Describe this image in detail`)

## Requirements

- Python 3 (stdlib only — no pip packages)
- One API key in env: `GO_API_KEY` (tried first, model `mimo-v2.5`) or `ZEN_API_KEY` (fallback, model `mimo-v2.5-free`)
- No secrets are stored in this repo — keys come from the environment only

## Usage

```json
{ "file": "C:/path/to/image.png", "prompt": "What is in this screenshot?" }
```

```sh
echo '{"file":"C:/path/to/image.png"}' | python see.py
```

## First interaction

Pairs with `speak`/`hear` (see `opencode-tool-speak`, `opencode-tool-hear`): the agent announces on its first reply that it can speak, listen, and see.

## License

MIT — free for anyone to use, see `LICENSE`.
