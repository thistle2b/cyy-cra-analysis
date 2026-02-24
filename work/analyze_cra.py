#!/usr/bin/env python3
"""
Analyze the EU Cyber Resilience Act (CRA) - Regulation (EU) 2024/2847.

Parses the markdown conversion of the CRA and extracts:
- Document structure (chapters, articles, annexes)
- Article titles and summaries
- Key definitions
- Obligations for economic operators
- Timeline / entry-into-force dates

Usage:
    python3 analyze_cra.py <markdown_file> [--output <output_file>]
"""

import argparse
import re
import sys
from pathlib import Path


def read_file(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")


def extract_chapters(text: str) -> list[dict]:
    """Extract chapter numbers and titles from the CRA text."""
    chapters = []
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        match = re.match(r"^CHAPTER\s+([IVXLC]+)$", line)
        if match:
            chapter_num = match.group(1)
            # Collect the next several lines and join to handle multi-line titles
            block = " ".join(
                lines[j].strip() for j in range(i + 1, min(i + 10, len(lines)))
            )
            title_match = re.search(r"\[(.+?)\]\{\.oj-bold\}", block)
            title = title_match.group(1) if title_match else ""
            # Normalize whitespace in title
            title = " ".join(title.split())
            chapters.append({"number": chapter_num, "title": title})
        i += 1
    return chapters


def extract_articles(text: str) -> list[dict]:
    """Extract article numbers and titles from the CRA text."""
    articles = []
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        match = re.match(r"^Article\s+(\d+)$", line)
        if match:
            art_num = int(match.group(1))
            # Look ahead for the title in the next few lines
            title = ""
            for j in range(i + 1, min(i + 6, len(lines))):
                candidate = lines[j].strip()
                if candidate and not candidate.startswith(":::") and not candidate.startswith("{"):
                    if not candidate.startswith("|"):
                        title = candidate
                        # If next non-empty line continues the title, append it
                        for k in range(j + 1, min(j + 3, len(lines))):
                            next_line = lines[k].strip()
                            if next_line and not next_line.startswith(":::") and not next_line.startswith("{") and not next_line.startswith("|"):
                                title += " " + next_line
                            else:
                                break
                        break
            articles.append({"number": art_num, "title": title, "line": i + 1})
        i += 1
    return articles


def extract_definitions(text: str) -> list[dict]:
    """Extract key definitions from Article 3."""
    definitions = []
    lines = text.splitlines()
    in_article_3 = False
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if re.match(r"^Article\s+3$", line):
            in_article_3 = True
            i += 1
            continue
        if in_article_3 and re.match(r"^Article\s+4$", line):
            break
        if in_article_3:
            # Definitions are typically formatted as: 'term' means ...
            def_match = re.search(r"'([^']+)'\s+means\s+(.+)", line)
            if def_match:
                term = def_match.group(1)
                definition_start = def_match.group(2).rstrip(";").strip()
                # Remove trailing table pipe characters
                definition_start = re.sub(r"\s*\|$", "", definition_start).strip()
                definitions.append({"term": term, "definition": definition_start})
        i += 1
    return definitions


def extract_annexes(text: str) -> list[dict]:
    """Extract annex references from the CRA text."""
    annexes = []
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        match = re.match(r"^ANNEX\s+([IVXLC]+)$", line)
        if match:
            annex_num = match.group(1)
            # Look ahead for title
            title = ""
            for j in range(i + 1, min(i + 10, len(lines))):
                candidate = lines[j].strip()
                if candidate and not candidate.startswith(":::") and not candidate.startswith("{"):
                    title = candidate
                    break
            annexes.append({"number": annex_num, "title": title})
        i += 1
    return annexes


def extract_timeline(text: str) -> list[dict]:
    """Extract key dates and timelines from the CRA text."""
    dates = []
    lines = text.splitlines()
    for i, line in enumerate(lines):
        # Look for date patterns with months
        date_matches = re.finditer(
            r"(\d{1,2}\s+(?:January|February|March|April|May|June|July|"
            r"August|September|October|November|December)\s+\d{4})",
            line,
        )
        for m in date_matches:
            context = line.strip()
            # Trim table formatting
            context = re.sub(r"^\|.*?\|", "", context).strip()
            context = re.sub(r"\|$", "", context).strip()
            if context:
                # Truncate at word boundary
                if len(context) > 200:
                    context = context[:200].rsplit(" ", 1)[0] + "…"
                dates.append({"date": m.group(1), "context": context, "line": i + 1})
    # Deduplicate by date
    seen = set()
    unique_dates = []
    for d in dates:
        if d["date"] not in seen:
            seen.add(d["date"])
            unique_dates.append(d)
    return unique_dates


def format_analysis(
    chapters: list[dict],
    articles: list[dict],
    definitions: list[dict],
    annexes: list[dict],
    timeline: list[dict],
) -> str:
    """Format the analysis results as a markdown document."""
    out = []
    out.append("# EU Cyber Resilience Act (CRA) — Analysis")
    out.append("")
    out.append("**Regulation (EU) 2024/2847** of the European Parliament and of the Council")
    out.append("")
    out.append("---")
    out.append("")

    # Summary statistics
    out.append("## Summary Statistics")
    out.append("")
    out.append(f"- **Chapters:** {len(chapters)}")
    out.append(f"- **Articles:** {len(articles)}")
    out.append(f"- **Definitions (Article 3):** {len(definitions)}")
    out.append(f"- **Annexes:** {len(annexes)}")
    out.append("")

    # Chapters
    out.append("## Document Structure — Chapters")
    out.append("")
    out.append("| Chapter | Title |")
    out.append("|---------|-------|")
    for ch in chapters:
        out.append(f"| {ch['number']} | {ch['title']} |")
    out.append("")

    # Articles
    out.append("## Articles")
    out.append("")
    out.append("| # | Title |")
    out.append("|---|-------|")
    for art in articles:
        out.append(f"| {art['number']} | {art['title']} |")
    out.append("")

    # Definitions
    out.append("## Key Definitions (Article 3)")
    out.append("")
    for d in definitions:
        out.append(f"- **{d['term']}**: {d['definition']}")
    out.append("")

    # Annexes
    out.append("## Annexes")
    out.append("")
    out.append("| Annex | Title |")
    out.append("|-------|-------|")
    for anx in annexes:
        out.append(f"| {anx['number']} | {anx['title']} |")
    out.append("")

    # Timeline
    out.append("## Key Dates")
    out.append("")
    for t in timeline:
        out.append(f"- **{t['date']}** — {t['context']}")
    out.append("")

    return "\n".join(out)


def main():
    parser = argparse.ArgumentParser(
        description="Analyze the EU Cyber Resilience Act (CRA) markdown document."
    )
    parser.add_argument("input", help="Path to the CRA markdown file")
    parser.add_argument(
        "--output",
        "-o",
        default="cra_analysis.md",
        help="Output file path (default: cra_analysis.md)",
    )
    args = parser.parse_args()

    text = read_file(args.input)

    chapters = extract_chapters(text)
    articles = extract_articles(text)
    definitions = extract_definitions(text)
    annexes = extract_annexes(text)
    timeline = extract_timeline(text)

    result = format_analysis(chapters, articles, definitions, annexes, timeline)
    Path(args.output).write_text(result, encoding="utf-8")

    print(f"Analysis written to {args.output}")
    print(f"  Chapters:    {len(chapters)}")
    print(f"  Articles:    {len(articles)}")
    print(f"  Definitions: {len(definitions)}")
    print(f"  Annexes:     {len(annexes)}")
    print(f"  Key dates:   {len(timeline)}")


if __name__ == "__main__":
    main()
