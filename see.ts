import { tool } from "@opencode-ai/plugin";
import { z } from "zod";
import { spawn } from "child_process";
import path from "path";

const seeTool = tool({
  description:
    "Read an existing image or PDF file and describe it using MiMo-V2.5 vision via OpenCode Zen/Go. Use when you need to see what is in a file.",
  args: {
    file: z.string().describe("Absolute path to the image or PDF file"),
    prompt: z
      .string()
      .default("Describe this image in detail")
      .describe("Optional instruction for the vision model"),
  },
  async execute(args, context) {
    const { file, prompt } = args;

    const pythonScriptPath = path.join(
      process.env.APPDATA ?? "",
      "..",
      "..",
      ".config",
      "opencode",
      "tools",
      "see.py"
    );

    const inputJson = JSON.stringify({ file, prompt });

    return new Promise((resolve) => {
      const child = spawn("python", [pythonScriptPath], {
        windowsHide: true,
      });
      let stdout = "";
      let stderr = "";
      child.stdout.on("data", (d) => (stdout += d));
      child.stderr.on("data", (d) => (stderr += d));
      child.on("close", () => {
        try {
          const parsed = JSON.parse(stdout.trim());
          resolve(parsed.text ?? parsed.message ?? stdout.trim());
        } catch {
          resolve((stdout.trim() || stderr.trim()) || "No output from see.");
        }
      });
      child.stdin.write(inputJson);
      child.stdin.end();
    });
  },
});

export default seeTool;
