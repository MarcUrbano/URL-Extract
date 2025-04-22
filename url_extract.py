import requests, argparse, re, urllib.parse, os
from bs4 import BeautifulSoup
from rich.console import Console
from rich.table import Table

console = Console()
visited = set()

def extract_urls(domain, depth=1, current_depth=0, ext=None, match=None, analyze_js=False):
    if current_depth > depth or domain in visited:
        return []

    headers = {"User-Agent": "Mozilla/5.0 (RedTeamRecon)"}
    visited.add(domain)

    try:
        response = requests.get(domain, headers=headers, timeout=10)
        response.raise_for_status()
    except Exception as e:
        console.print(f"[red]Error fetching {domain}: {e}[/red]")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    raw_urls = set()

    # Extract from HTML tags
    tags_attrs = {
        "a": "href",
        "script": "src",
        "link": "href",
        "img": "src",
        "iframe": "src"
    }

    for tag, attr in tags_attrs.items():
        for element in soup.find_all(tag):
            url = element.get(attr)
            if url:
                full_url = urllib.parse.urljoin(domain, url)
                raw_urls.add(full_url)

    # Regex fallback
    regex_urls = re.findall(r'https?://[^\s"\']+', response.text)
    raw_urls.update(regex_urls)

    # Filter same-origin
    base = urllib.parse.urlparse(domain).netloc
    in_scope_urls = [u for u in raw_urls if base in urllib.parse.urlparse(u).netloc]

    # Apply extension filter
    if ext:
        in_scope_urls = [u for u in in_scope_urls if u.lower().endswith(f".{ext.lower()}")]

    # Apply path matcher
    if match:
        in_scope_urls = [u for u in in_scope_urls if match.lower() in u.lower()]

    recursive_urls = []
    for url in in_scope_urls:
        if url.endswith("/"):
            recursive_urls.extend(
                extract_urls(url, depth, current_depth + 1, ext, match, analyze_js)
            )

    # Analyze JS if requested
    if analyze_js and ext == "js":
        for js_url in in_scope_urls:
            analyze_javascript(js_url)

    return sorted(set(in_scope_urls + recursive_urls))

def analyze_javascript(js_url):
    try:
        r = requests.get(js_url, timeout=5)
        if r.status_code == 200:
            matches = re.findall(r'(?i)(api|key|token|admin|debug|config|endpoint)[^\n"\']{0,50}', r.text)
            if matches:
                console.print(f"[magenta][JS Analysis][/magenta] [cyan]{js_url}[/cyan] → [bold yellow]{set(matches)}[/bold yellow]")
    except Exception as e:
        console.print(f"[red]Failed to analyze JS: {js_url} → {e}[/red]")

def display_results(urls, domain):
    if not urls:
        console.print(f"[yellow]No URLs found on {domain}.[/yellow]")
        return

    table = Table(title=f"Extracted URLs from {domain}")
    table.add_column("URL", style="cyan")
    for url in sorted(set(urls)):
        table.add_row(url)

    console.print(table)

def export_results(urls, out_path):
    try:
        with open(out_path, "w") as f:
            for url in sorted(set(urls)):
                f.write(url + "\n")
        console.print(f"[green]✔ Exported to {out_path}[/green]")
    except Exception as e:
        console.print(f"[red]Error writing to {out_path}: {e}[/red]")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Recursive URL Extractor with Filters and JS Analyzer")
    parser.add_argument("target", help="Target URL (e.g. https://example.com)")
    parser.add_argument("--depth", type=int, default=1, help="Recursion depth (default: 1)")
    parser.add_argument("--ext", help="Filter URLs by extension (e.g. js, php, pdf)")
    parser.add_argument("--match", help="Filter URLs by path substring match (e.g. admin)")
    parser.add_argument("--out", help="Export URLs to file (e.g. urls.txt)")
    parser.add_argument("--analyze-js", action="store_true", help="Enable JavaScript keyword scan")

    args = parser.parse_args()
    console.print(f"[bold blue]🌐 Scanning {args.target} with depth={args.depth}, ext={args.ext}, match={args.match}[/bold blue]")

    urls = extract_urls(args.target, args.depth, ext=args.ext, match=args.match, analyze_js=args.analyze_js)
    display_results(urls, args.target)

    if args.out:
        export_results(urls, args.out)
