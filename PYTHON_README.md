# Backlink Generator Tool - Python Version

This is a Python command-line version of the Backlink Generator tool. It converts the JavaScript web tool into a standalone Python script that can generate SEO backlinks for any domain or URL.

## Features

✨ **Core Features:**
- Generate backlinks from 50+ templates
- Support for YouTube video links
- Archive.org variants (archive.today, archive.li, archive.vn, etc.)
- URL validation and normalization
- CORS proxy support
- CSV export with results
- Optional URL testing/verification

## Installation

No external dependencies required! This tool uses only Python's standard library.

**Python Requirements:**
- Python 3.6+

## Usage

### Basic Usage

Generate backlinks for a domain:

```bash
python backlink-generator.py example.com
```

Generate backlinks for a full URL:

```bash
python backlink-generator.py "https://example.com/page"
```

Generate backlinks for a YouTube video:

```bash
python backlink-generator.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
```

### Advanced Options

**Test if generated URLs are accessible:**
```bash
python backlink-generator.py example.com --test
```

**Save results to a specific CSV file:**
```bash
python backlink-generator.py example.com --output backlinks.csv
```

**Don't shuffle templates (keep original order):**
```bash
python backlink-generator.py example.com --no-shuffle
```

**Limit displayed results:**
```bash
python backlink-generator.py example.com --limit 20
```

**Specify custom template directory:**
```bash
python backlink-generator.py example.com --config-dir ./config
```

**Combined example:**
```bash
python backlink-generator.py example.com --test --output results.csv --no-shuffle --limit 50
```

## Interactive Mode

If no domain is provided, the tool will prompt you:

```bash
python backlink-generator.py
```

## Output

### Console Output
The tool displays:
- ✓ Successfully loaded templates
- 📍 Normalized domain URL
- ✓ YouTube detection (if applicable)
- Formatted table of generated backlinks
- 📊 Success rate (if testing URLs)

### CSV Export
Results are saved as CSV with columns:
- `index`: Sequential number
- `url`: Generated backlink URL
- `template`: Template used to generate the URL
- `type`: Type of link (regular or archive_variant)
- `status`: Test result (if --test flag used)

Example filename: `backlinks_20240509_143022.csv`

## How It Works

1. **Load Templates**: Reads from JSON files (backlink-templates.json, youtube-backlink-templates.json, cors-proxies.json)

2. **Normalize URL**: Validates and normalizes the input domain/URL

3. **URL Mapping**: Creates a map of placeholder values:
   - `[URL]` - Full URL
   - `[DOMAIN]` - Domain name
   - `[NOPROTOCOL_URL]` - URL without protocol
   - `[DOMAINNAME]` - Domain without TLD
   - `[TLD]` - Top-level domain
   - `[ENCODE_*]` - URL-encoded versions of above
   - `[ID]` - YouTube video ID (if applicable)

4. **Generate Backlinks**: Replaces placeholders in each template with actual values

5. **Group Archive Variants**: Archives (archive.today, archive.li, etc.) are automatically grouped

6. **Test URLs** (optional): Verifies if generated URLs are accessible

7. **Export Results**: Saves all results to CSV file

## Template Formats

Templates support multiple bracket styles:

- `[PLACEHOLDER]` - Square brackets
- `{{PLACEHOLDER}}` - Double braces
- `[ENCODE_URL]` - URL-encoded placeholder
- `{{ENCODE_URL}}` - Double brace encoded

## Example Output

```
🔗 Generating backlinks for: example.com
======================================================================

📍 Domain: https://example.com
✓ Loaded 50 backlink templates
✓ Loaded 20 YouTube templates
✓ Loaded 4 CORS proxies

INDEX STATUS   URL
------ -------- ------------------------------------------------------------
1      ✓        https://forums2.battleon.com/f/interceptor.asp?dest=example.com/
2      ✓        https://webseiten-analyse24.de/en/www/example.com
3      ✓        https://altovalleit.com/tools/robots-txt-tester/example.com
...

Total: 150 backlinks generated

✓ Results saved to: backlinks_20240509_143022.csv

📊 Success rate: 45/150 (30%)
```

## Tips for Best Results

1. **Use Valid Domains**: Enter properly formatted domain names or URLs
2. **Test URLs**: Use `--test` flag to identify working backlink sources
3. **Monitor Results**: Check the CSV output to analyze which templates work best
4. **Schedule Runs**: Run periodically to create continuous backlinks
5. **Vary Domains**: Test with different pages/URLs on your site

## Supported Template Placeholders

| Placeholder | Example | Notes |
|-------------|---------|-------|
| `[URL]` | `https://example.com/page` | Full URL |
| `[DOMAIN]` | `example.com` | Domain with all subdomains |
| `[DOMAINNAME]` | `example` | Domain without TLD |
| `[TLD]` | `com` | Top-level domain |
| `[SUBDOMAIN]` | `www.` | Subdomain part |
| `[PROTOCOL]` | `https:` | Protocol scheme |
| `[PORT]` | `:8080` | Port if applicable |
| `[PATH]` | `/page/path` | URL path |
| `[QUERY]` | `?key=value` | Query string |
| `[FRAGMENT]` | `#section` | Fragment/anchor |
| `[NOPROTOCOL_URL]` | `example.com/page` | URL without protocol |
| `[NOSUBDOMAIN_URL]` | `example.com/page` | URL without www subdomain |
| `[ENCODE_*]` | Various | URL-encoded version of any above |
| `[ID]` | `dQw4w9WgXcQ` | YouTube video ID |

## Troubleshooting

### No templates loaded
- Ensure `backlink-templates.json`, `youtube-backlink-templates.json`, and `cors-proxies.json` are in the same directory as the script
- Or use `--config-dir` to specify the location

### Invalid URL error
- Enter a valid domain (e.g., `example.com`) or full URL (e.g., `https://example.com/page`)
- Single-word domains without a TLD will be rejected

### Connection timeout during testing
- Use `--test` flag for accurate results
- Some backlink sources may be unavailable or blocked

## License

This tool is for SEO research and testing purposes only. Use responsibly and comply with all applicable laws and website terms of service.

## Original JavaScript Version

For the interactive web version, open `index.html` in a browser or visit the GitHub repository.
