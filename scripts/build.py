#!/usr/bin/env python3
"""Build multilingual preview pages from one HTML template and locale JSON files.

Outputs are deliberately written under _build/ and are NOT published by GitHub Pages.
Only the introductory section is currently translated; do not deploy yet.
"""
from __future__ import annotations

import argparse
import html
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "src" / "index.html"
LOCALES = ("en", "ja", "zh-TW", "ko")
TOKEN = re.compile(r"\{\{([A-Za-z][A-Za-z0-9_.-]*)\}\}")


def render(template: str, translations: dict[str, str], locale: str) -> str:
    values = {"locale": locale, **translations}
    missing = set(TOKEN.findall(template)) - set(values)
    if missing:
        raise ValueError(f"Missing translations for {locale}: {', '.join(sorted(missing))}")
    result = TOKEN.sub(lambda m: html.escape(values[m.group(1)], quote=True), template)

    # The preview lives at _build/<locale>/index.html, two levels below
    # the original index.html. Rewrite existing relative paths accordingly.
    # Do not rewrite /absolute paths, #fragments, or external HTTPS links.
    result = re.sub(
        r'(?P<quote>["\x27])(?P<path>images/[^"\x27]*)',
        lambda m: m.group("quote") + "../../" + m.group("path"),
        result,
    )
    result = result.replace('href="ticket-helper.html"', 'href="../../ticket-helper.html"')
    result = result.replace("href='ticket-helper.html'", "href='../../ticket-helper.html'")

    # The remaining sections and navigation have not been translated yet.
    # Block search indexing until every section is localized and reviewed.
    result = result.replace(
        "<head>",
        '<head>\n  <meta name="robots" content="noindex, nofollow">',
        1,
    )
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "_build",
        help="Output directory for preview pages (default: _build/)",
    )
    args = parser.parse_args()
    output = args.output.resolve()
    if output == ROOT or ROOT in output.parents and output == ROOT / "src":
        parser.error("Output cannot overwrite the source directory or repository root")
    source = TEMPLATE.read_text(encoding="utf-8")
    keys = set(TOKEN.findall(source)) - {"locale"}
    for locale in LOCALES:
        json_file = ROOT / "locales" / f"{locale}.json"
        data = json.loads(json_file.read_text(encoding="utf-8"))
        if not isinstance(data, dict) or any(not isinstance(v, str) for v in data.values()):
            raise ValueError(f"{json_file} must contain string key/value pairs")
        if keys - data.keys():
            raise ValueError(f"{json_file} missing: {sorted(keys - data.keys())}")
        page = render(source, data, locale)
        destination = output / locale / "index.html"
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(page, encoding="utf-8")
        print(f"Built {destination.relative_to(ROOT) if destination.is_relative_to(ROOT) else destination}")
    # This landing page is the entry point for returning visitors. Explicit
    # language URLs remain authoritative and are never force-redirected.
    entry = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="robots" content="noindex, nofollow">
  <title>KATTOBASE | Choose language</title>
</head>
<body>
  <p>Opening your preferred language... <a href="en/">English</a></p>
  <script>
  (() => {
    const valid = ['en', 'ja', 'zh-TW', 'ko'];
    let preferred = 'en';
    try {
      const saved = localStorage.getItem('kattobase.preferredLanguage');
      if (valid.includes(saved)) preferred = saved;
    } catch (_) {}
    // Preserve section anchors when entering through the locale chooser.
    location.replace(preferred + '/' + location.hash);
  })();
  </script>
</body>
</html>
"""
    (output / "index.html").write_text(entry, encoding="utf-8")
    print(f"Built {output / 'index.html'} (saved-language entry point)")
    print("Preview only: original index.html was not modified.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
