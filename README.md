# See — let your AI look at pictures and PDFs

Point the agent at any image or PDF on your computer and it tells you
what is in it.

## What you need (all free)

1. **Python** — download it from python.org. On Windows, tick the box
   "Add python.exe to PATH" during installation. Nothing else to install.
2. **A free API key** — this tool looks at pictures through your OpenCode
   account:
   1. In OpenCode, run the `/connect` command and get a Zen or Go key.
   2. Save it by running (replace with your key):

      ```sh
      setx ZEN_API_KEY "paste your key here"
      ```

   3. Close the terminal and open it again.

## Setup (about 2 minutes)

1. Copy these 3 files into your OpenCode tools folder:
   - `see.py`, `see.ts`, `see.json`
   - Windows: `C:\Users\YOUR-NAME\.config\opencode\tools\`
   - Mac/Linux: `~/.config/opencode/tools/`
2. Restart OpenCode.

## How to use

Just point at a file, for example:

- "What is in this screenshot?"
- "Describe `C:\Pictures\photo.png` for me."
- "Summarize this document: `C:\Docs\report.pdf`."

## If something goes wrong

- **Message about the key not being set** → redo step 2 above.
- **File not found** → use the complete path, e.g.
  `C:\Users\YOUR-NAME\Pictures\photo.png`.

## License

MIT — free for everyone, see `LICENSE`.
