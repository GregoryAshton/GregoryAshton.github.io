## Autobib

This program will search for `bibtex` keys in all `.tex` files for a given directory.
The code assumes the `.tex` files are using either [INSPIREs](https://inspirehep.net/) keys or [NASA/ADS](https://ui.adsabs.harvard.edu/) (i.e., the keys given by default by these websites).
It will then lookup bibtex entries using the source key and write it to a file.
Download the file and save as `autobib.py` then check 

```
$ python autobib.py --help
```
for options on how to use it.


```python
#!/usr/bin/env python3
import re
import requests
from pathlib import Path
import argparse


def extract_cite_keys(tex_file):
    """Extract all citation keys from a LaTeX file.

    Returns a tuple of (keys, warnings) where keys is a list of valid citation keys
    and warnings is a list of warning messages for invalid keys.
    """
    with open(tex_file, "r", encoding="utf-8") as f:
        content = f.read()
    # Match all citation commands: \cite{}, \citep{}, \citet{}, \citealt{}, \citealp{},
    # \citeauthor{}, \citeyear{}, \Citep{}, \Citet{}, etc.
    # Also handles optional arguments like \citep[e.g.][]{key}
    pattern = r"\\[Cc]ite[a-zA-Z]*(?:\[[^\]]*\])*\{([^}]+)\}"
    matches = re.findall(pattern, content)
    # Split multiple keys in single cite command
    keys = []
    warnings = []
    for match in matches:
        for key in match.split(","):
            key = key.strip()
            if not key:
                warnings.append(f"{tex_file}: Empty citation key found")
            elif ":" not in key:
                warnings.append(f"{tex_file}: Skipping key '{key}' (not an INSPIRE/ADS key)")
            else:
                keys.append(key)
    return keys, warnings


def get_inspire_bibtex(key):
    """Fetch BibTeX directly from INSPIRE for a given INSPIRE key."""
    url = f"https://inspirehep.net/api/literature?q=texkeys:{key}"
    headers = {"Accept": "application/x-bibtex"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200 and response.text.strip():
        return response.text.strip()
    return None


def get_ads_info_from_inspire(key):
    """Fetch ADS bibcode and arXiv ID from INSPIRE for a given INSPIRE key.

    Returns a tuple of (ads_bibcode, arxiv_id), either may be None.
    """
    # Use texkeys field to avoid colon being interpreted as field operator
    url = f"https://inspirehep.net/api/literature?q=texkeys:{key}"
    headers = {"Accept": "application/json"}
    response = requests.get(url, headers=headers)

    ads_bibcode = None
    arxiv_id = None

    if response.status_code == 200:
        data = response.json()
        hits = data.get("hits", {}).get("hits", [])
        if hits:
            metadata = hits[0].get("metadata", {})

            # Try to get ADS bibcode
            external_ids = metadata.get("external_system_identifiers", [])
            for ext_id in external_ids:
                if ext_id.get("schema") == "ADS":
                    ads_bibcode = ext_id.get("value")
                    break

            # Get arXiv ID as fallback
            arxiv_eprints = metadata.get("arxiv_eprints", [])
            if arxiv_eprints:
                arxiv_id = arxiv_eprints[0].get("value")

    return ads_bibcode, arxiv_id


def search_ads_by_arxiv(arxiv_id, api_key):
    """Search ADS for a paper by arXiv ID and return its bibcode."""
    url = "https://api.adsabs.harvard.edu/v1/search/query"
    headers = {"Authorization": f"Bearer {api_key}"}
    params = {"q": f"arXiv:{arxiv_id}", "fl": "bibcode"}
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        result = response.json()
        docs = result.get("response", {}).get("docs", [])
        if docs:
            return docs[0].get("bibcode")
    return None


def get_ads_bibtex(bibcode, api_key):
    """Fetch BibTeX from ADS for a given bibcode."""
    url = "https://api.adsabs.harvard.edu/v1/export/bibtex"
    headers = {"Authorization": f"Bearer {api_key}"}
    data = {"bibcode": [bibcode]}
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        result = response.json()
        export = result.get("export", "").strip()
        if export and not export.startswith("No records"):
            return export
    return None


def extract_existing_bib_keys(bib_file):
    """Extract citation keys from an existing BibTeX file."""
    if not bib_file.exists():
        return set()
    with open(bib_file, "r", encoding="utf-8") as f:
        content = f.read()
    # Match @type{key,
    pattern = r"@\w+\s*\{\s*([^,\s]+)\s*,"
    return set(re.findall(pattern, content))


def replace_bibtex_key(bibtex, new_key):
    """Replace the citation key in a BibTeX entry with a new key."""
    # Match the entry type and key: @article{old_key,
    pattern = r"(@\w+\s*\{)\s*([^,\s]+)\s*,"
    return re.sub(pattern, rf"\1{new_key},", bibtex, count=1)


def truncate_authors(bibtex, max_authors):
    """Truncate the author list in a BibTeX entry to max_authors.

    If there are more than max_authors, keep the first max_authors and add "and others".
    If max_authors is None or 0, no truncation is performed.
    """
    if not max_authors:
        return bibtex

    # Match the author field (handles multiline author fields)
    author_pattern = r"(\s*author\s*=\s*\{)(.+?)(\},?\s*\n)"
    match = re.search(author_pattern, bibtex, re.IGNORECASE | re.DOTALL)

    if not match:
        return bibtex

    prefix = match.group(1)
    authors_str = match.group(2)
    suffix = match.group(3)

    # Split authors by " and " (BibTeX standard separator)
    authors = [a.strip() for a in re.split(r"\s+and\s+", authors_str)]

    if len(authors) <= max_authors:
        return bibtex

    # Keep first max_authors and add "others"
    truncated_authors = authors[:max_authors] + ["others"]
    new_authors_str = " and ".join(truncated_authors)

    # Replace the author field
    new_author_field = f"{prefix}{new_authors_str}{suffix}"
    return bibtex[: match.start()] + new_author_field + bibtex[match.end() :]


def is_ads_bibcode(key):
    """Check if a key looks like an ADS bibcode (e.g., 2016PhRvL.116f1102A)."""
    # ADS bibcodes are typically 19 characters: 4-digit year + journal code + volume + page + author initial
    # Pattern: YYYYJJJJJVVVVMPPPPA where Y=year, J=journal, V=volume, M=section, P=page, A=author
    ads_pattern = r"^\d{4}[A-Za-z&.]+\..*[A-Z]$"
    return bool(re.match(ads_pattern, key)) and len(key) >= 15


def is_inspire_key(key):
    """Check if a key looks like an INSPIRE texkey (e.g., Author:2020abc)."""
    # INSPIRE keys are typically Author:YYYYxxx where xxx is 2-3 lowercase letters
    inspire_pattern = r"^[A-Za-z][A-Za-z0-9-]+:\d{4}[a-z]{2,3}$"
    return bool(re.match(inspire_pattern, key))


def fetch_bibtex_ads_preferred(key, api_key):
    """Fetch BibTeX preferring ADS, with INSPIRE as fallback."""
    # First check if it's already an ADS bibcode
    if is_ads_bibcode(key):
        bibtex = get_ads_bibtex(key, api_key)
        if bibtex:
            return bibtex, "ADS (direct)"

    # Try to get ADS bibcode or arXiv ID from INSPIRE
    ads_bibcode, arxiv_id = get_ads_info_from_inspire(key)

    # Try ADS bibcode first
    if ads_bibcode:
        bibtex = get_ads_bibtex(ads_bibcode, api_key)
        if bibtex:
            return bibtex, f"ADS via INSPIRE ({ads_bibcode})"

    # Fall back to arXiv ID search on ADS
    if arxiv_id:
        ads_bibcode = search_ads_by_arxiv(arxiv_id, api_key)
        if ads_bibcode:
            bibtex = get_ads_bibtex(ads_bibcode, api_key)
            if bibtex:
                return bibtex, f"ADS via arXiv ({arxiv_id})"

    # Try the key directly as ADS bibcode
    bibtex = get_ads_bibtex(key, api_key)
    if bibtex:
        return bibtex, "ADS (direct fallback)"

    # Final fallback: fetch BibTeX directly from INSPIRE
    bibtex = get_inspire_bibtex(key)
    if bibtex:
        return bibtex, "INSPIRE (fallback)"

    return None, None


def fetch_bibtex_inspire_preferred(key, api_key):
    """Fetch BibTeX preferring INSPIRE, with ADS as fallback."""
    # Try INSPIRE first
    bibtex = get_inspire_bibtex(key)
    if bibtex:
        return bibtex, "INSPIRE"

    # Fall back to ADS
    if is_ads_bibcode(key):
        bibtex = get_ads_bibtex(key, api_key)
        if bibtex:
            return bibtex, "ADS (fallback, direct)"

    # Try to get ADS bibcode from INSPIRE metadata
    ads_bibcode, arxiv_id = get_ads_info_from_inspire(key)
    if ads_bibcode:
        bibtex = get_ads_bibtex(ads_bibcode, api_key)
        if bibtex:
            return bibtex, f"ADS (fallback, via INSPIRE)"

    if arxiv_id:
        ads_bibcode = search_ads_by_arxiv(arxiv_id, api_key)
        if ads_bibcode:
            bibtex = get_ads_bibtex(ads_bibcode, api_key)
            if bibtex:
                return bibtex, f"ADS (fallback, via arXiv)"

    return None, None


def fetch_bibtex_auto(key, api_key):
    """Fetch BibTeX using the source that matches the key format."""
    if is_ads_bibcode(key):
        # Key looks like ADS bibcode, prefer ADS
        bibtex = get_ads_bibtex(key, api_key)
        if bibtex:
            return bibtex, "ADS (auto)"
        # Fallback to INSPIRE
        bibtex = get_inspire_bibtex(key)
        if bibtex:
            return bibtex, "INSPIRE (fallback)"
    else:
        # Key looks like INSPIRE key, prefer INSPIRE
        bibtex = get_inspire_bibtex(key)
        if bibtex:
            return bibtex, "INSPIRE (auto)"
        # Fallback to ADS via INSPIRE cross-reference
        ads_bibcode, arxiv_id = get_ads_info_from_inspire(key)
        if ads_bibcode:
            bibtex = get_ads_bibtex(ads_bibcode, api_key)
            if bibtex:
                return bibtex, f"ADS (fallback, via INSPIRE)"
        if arxiv_id:
            ads_bibcode = search_ads_by_arxiv(arxiv_id, api_key)
            if ads_bibcode:
                bibtex = get_ads_bibtex(ads_bibcode, api_key)
                if bibtex:
                    return bibtex, f"ADS (fallback, via arXiv)"

    return None, None


def fetch_bibtex(key, api_key, source="ads"):
    """Fetch BibTeX using the specified source preference."""
    if source == "ads":
        return fetch_bibtex_ads_preferred(key, api_key)
    elif source == "inspire":
        return fetch_bibtex_inspire_preferred(key, api_key)
    elif source == "auto":
        return fetch_bibtex_auto(key, api_key)
    else:
        return fetch_bibtex_ads_preferred(key, api_key)


def main():
    import os

    parser = argparse.ArgumentParser(
        description="Extract citations and download BibTeX from NASA/ADS"
    )
    parser.add_argument("directory", help="Directory containing LaTeX files")
    parser.add_argument(
        "-o", "--output", default="references.bib", help="Output BibTeX file"
    )
    parser.add_argument(
        "-a",
        "--max-authors",
        type=int,
        default=3,
        help="Maximum number of authors before truncating with 'and others' (default: 3, use 0 for no limit)",
    )
    parser.add_argument(
        "-l",
        "--list-keys",
        action="store_true",
        help="List citation keys found in LaTeX files and exit (no lookup)",
    )
    parser.add_argument(
        "--fresh",
        action="store_true",
        help="Start from scratch, ignoring existing output file",
    )
    parser.add_argument(
        "-s",
        "--source",
        choices=["ads", "inspire", "auto"],
        default="ads",
        help="Preferred BibTeX source: 'ads' (default), 'inspire', or 'auto' (based on key format)",
    )
    args = parser.parse_args()

    # Collect all citation keys
    tex_dir = Path(args.directory)
    all_keys = set()
    all_warnings = []
    for tex_file in tex_dir.glob("**/*.tex"):
        keys, warnings = extract_cite_keys(tex_file)
        all_keys.update(keys)
        all_warnings.extend(warnings)

    # Print warnings for invalid keys
    if all_warnings:
        print("Warnings:")
        for warning in all_warnings:
            print(f"  {warning}")
        print()

    print(f"Found {len(all_keys)} unique citation keys")

    # If --list-keys, print keys and exit
    if args.list_keys:
        for key in sorted(all_keys):
            print(key)
        return 0

    # Check for ADS API key (not required if using --source inspire)
    api_key = os.getenv("ADS_API_KEY")
    if not api_key and args.source != "inspire":
        print("Error: ADS_API_KEY environment variable not set")
        print("Get your API key from: https://ui.adsabs.harvard.edu/user/settings/token")
        print("(Or use --source inspire to fetch from INSPIRE without an ADS key)")
        return 1

    # Check for existing bib file and determine which keys to fetch
    output_path = Path(args.output)
    existing_content = ""
    if not args.fresh and output_path.exists():
        existing_keys = extract_existing_bib_keys(output_path)
        keys_to_fetch = all_keys - existing_keys
        with open(output_path, "r", encoding="utf-8") as f:
            existing_content = f.read().strip()
        print(f"Found {len(existing_keys)} existing entries in {args.output}")
        print(f"Fetching {len(keys_to_fetch)} new keys")
    else:
        keys_to_fetch = all_keys
        if args.fresh and output_path.exists():
            print(f"Starting fresh (ignoring existing {args.output})")

    # Download BibTeX entries
    bibtex_entries = []
    not_found = []
    for key in sorted(keys_to_fetch):
        print(f"Fetching {key}...", end=" ")
        bibtex, source = fetch_bibtex(key, api_key, args.source)
        if bibtex:
            bibtex = replace_bibtex_key(bibtex, key)
            bibtex = truncate_authors(bibtex, args.max_authors)
            bibtex_entries.append(bibtex)
            print(f"✓ {source}")
        else:
            not_found.append(key)
            print("✗ Not found")

    # Write output (append new entries to existing content)
    with open(args.output, "w", encoding="utf-8") as f:
        if existing_content and bibtex_entries:
            f.write(existing_content + "\n\n" + "\n\n".join(bibtex_entries))
        elif existing_content:
            f.write(existing_content)
        else:
            f.write("\n\n".join(bibtex_entries))

    print(f"\nWrote {len(bibtex_entries)} new entries to {args.output}")

    if not_found:
        print(f"\nCould not find {len(not_found)} keys:")
        for key in not_found:
            print(f"  - {key}")


if __name__ == "__main__":
    main()
```
