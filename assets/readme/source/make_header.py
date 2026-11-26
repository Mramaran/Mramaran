"""Generate the profile header SVG (dark + light) from one layout.

Right side: a terminal window listing the merged upstream commits.
Hashes are the real landed commits (checked on GitHub 2026-11-26), newest first.

Usage (from the repository root):
    python3 assets/readme/source/make_header.py assets/readme

To add a newly merged PR, put its landed short SHA at the top of COMMITS and rerun.
Keep summaries to about 23 characters so lines fit inside the terminal window.
"""
import sys
from pathlib import Path

W, H = 1200, 420

THEMES = {
    "dark": dict(bg="#0a0b0d", fg="#f2f0ea", muted="#a7acb4", accent="#ffb020", edge="#2b2f36",
                 term="#111317", bar="#181b20", dim="#6b7079"),
    "light": dict(bg="#f2efe8", fg="#16140f", muted="#4a463d", accent="#c2410c", edge="#cbc4b6",
                  term="#faf8f3", bar="#e9e5dc", dim="#8a8478"),
}

SANS = "'IBM Plex Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"
MONO = "'IBM Plex Mono', ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"

# (short sha, repo, summary) — real landed commits, newest first
COMMITS = [
    ("39d75a7", "quest", "wait for socat port"),
    ("3bc4339", "pytorch", "from_file byte-0 fix"),
    ("b9ff439", "pytorch", "avg_pool2d value check"),
    ("62e0c9f", "brevitas", "LSTM ONNX dynamo export"),
    ("d0eb5d2", "vllm", "--sleep-mode-backend"),
    ("18c5583", "tensorflow", "set_seed lazy-init docs"),
    ("6435cb8", "aider", "bash tree-sitter tags"),
]

TX, TY, TW, TH = 616, 34, 540, 352   # terminal window
FS, LH = 18, 33                        # mono size, line height
CH = FS * 0.6                          # approx mono advance


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def render(t):
    out = []
    a = out.append
    a(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
      f'role="img" aria-labelledby="title desc">')
    a('<title id="title">Thirumaran S L — AI/ML developer</title>')
    a('<desc id="desc">Thirumaran S L fixes bugs in the ML frameworks he uses. A terminal window lists his seven '
      'merged upstream commits: quest, two in PyTorch, Brevitas, vLLM, TensorFlow and Aider.</desc>')
    a(f'<rect width="{W}" height="{H}" rx="22" fill="{t["bg"]}"/>')

    a('<g id="title-block" transform="translate(64 0)">')
    a(f'<rect x="0" y="86" width="12" height="12" fill="{t["accent"]}"/>')
    a(f'<text x="24" y="98" font-family="{MONO}" font-size="20" fill="{t["accent"]}">ai/ml developer · coimbatore</text>')
    a(f'<text x="-3" y="172" font-family="{SANS}" font-size="66" font-weight="700" fill="{t["fg"]}" '
      f'letter-spacing="-1.5">Thirumaran S L</text>')
    a(f'<text x="0" y="226" font-family="{SANS}" font-size="25" fill="{t["fg"]}">I fix bugs in the ML frameworks I use.</text>')
    a(f'<text x="0" y="262" font-family="{SANS}" font-size="25" fill="{t["muted"]}">A few of those fixes now ship in</text>')
    a(f'<text x="0" y="298" font-family="{SANS}" font-size="25" fill="{t["muted"]}">PyTorch, vLLM and TensorFlow.</text>')
    a(f'<line x1="0" y1="338" x2="480" y2="338" stroke="{t["edge"]}" stroke-width="1.5"/>')
    a(f'<text x="0" y="370" font-family="{MONO}" font-size="19" fill="{t["muted"]}">'
      f'<tspan fill="{t["accent"]}">7</tspan> merged upstream PRs  ·  intern @ ChainAim</text>')
    a('</g>')

    a(f'<g id="terminal" transform="translate({TX} {TY})">')
    a(f'<rect width="{TW}" height="{TH}" rx="14" fill="{t["term"]}" stroke="{t["edge"]}" stroke-width="1.5"/>')
    a(f'<path d="M0 14 A14 14 0 0 1 14 0 H{TW - 14} A14 14 0 0 1 {TW} 14 V40 H0 Z" fill="{t["bar"]}"/>')
    a(f'<line x1="0" y1="40" x2="{TW}" y2="40" stroke="{t["edge"]}" stroke-width="1.2"/>')
    for i in range(3):
        a(f'<circle cx="{24 + i * 20}" cy="20" r="6" fill="{t["edge"]}"/>')
    a(f'<text x="{TW / 2}" y="26" text-anchor="middle" font-family="{MONO}" font-size="16" fill="{t["dim"]}">~/upstream — merged</text>')

    px = 24
    y = 40 + 36
    a(f'<text x="{px}" y="{y}" font-family="{MONO}" font-size="{FS}" fill="{t["muted"]}">'
      f'<tspan fill="{t["accent"]}">$</tspan> git log --oneline --author=mramaran</text>')
    repo_x = px + CH * 9
    msg_x = repo_x + CH * 12
    for sha, repo, msg in COMMITS:
        y += LH
        a(f'<text x="{px}" y="{y}" font-family="{MONO}" font-size="{FS}" fill="{t["accent"]}">{sha}</text>')
        a(f'<text x="{repo_x:.1f}" y="{y}" font-family="{MONO}" font-size="{FS}" font-weight="600" fill="{t["fg"]}">{esc(repo)}</text>')
        a(f'<text x="{msg_x:.1f}" y="{y}" font-family="{MONO}" font-size="{FS}" fill="{t["muted"]}">{esc(msg)}</text>')
    y += LH
    a(f'<text x="{px}" y="{y}" font-family="{MONO}" font-size="{FS}" fill="{t["accent"]}">$</text>')
    a(f'<rect x="{px + CH * 2:.1f}" y="{y - FS + 3}" width="{CH:.1f}" height="{FS + 1}" fill="{t["accent"]}"/>')
    a('</g>')
    a('</svg>')
    return "\n".join(out) + "\n"


def main():
    out_dir = Path(sys.argv[1])
    out_dir.mkdir(parents=True, exist_ok=True)
    for name, theme in THEMES.items():
        (out_dir / f"header-{name}.svg").write_text(render(theme), encoding="utf-8")


if __name__ == "__main__":
    main()
