// the-catalogue-photo-of-an-2-20261121-0341 — "ToastMail 3000"
//
// One catalogue photograph of an impossible gadget: a chrome toaster that
// toasts your unread emails onto bread, drawn in-session with a PIL script
// (draw_entry.py) — no downloaded photo, no copied image. This program
// copies that photograph to the grader's output directory, byte for byte.
//
// The image is found next to this script file, never via the working
// directory: the grader runs `node /bot/main.ts` from a directory of its
// own choosing, so a bare relative path would not find entry.png.
import { copyFileSync, mkdirSync, readFileSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const scriptDir = dirname(fileURLToPath(import.meta.url));
const sourceImage = join(scriptDir, "entry.png");

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "out";
mkdirSync(outDir, { recursive: true });

// The gate only accepts a whole PNG of at most 1 MiB, so refuse loudly
// instead of writing an invalid entry if the image ever drifts out of range.
// The output name is fixed by the competition: /output/entry.png.
const OUTPUT_NAME = "entry.png";
const size = statSync(sourceImage).size;
if (size > 1048576) {
  throw new Error(`entry.png is ${size} bytes, over the 1 MiB gate limit`);
}
const header = readFileSync(sourceImage).subarray(0, 8);
const pngMagic = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
if (!header.equals(pngMagic)) {
  throw new Error("entry.png is not a PNG file");
}
copyFileSync(sourceImage, join(outDir, OUTPUT_NAME));
