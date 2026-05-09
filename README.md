# Python Backlink Generator Tool

A standalone Python backlink generation toolkit that creates SEO backlink URLs from template collections. This repository includes both a simple generator and an advanced batch-processing version.

## Files Included

- `backlink-generator.py` - Main Python backlink generator script
- `advanced-backlink-generator.py` - Advanced script with batch processing, reporting, and concurrent URL testing
- `backlink.bat` - Windows launcher for the main generator
- `backlink.sh` - Unix shell launcher for the main generator
- `backlink-templates.json` - Backlink URL templates
- `youtube-backlink-templates.json` - YouTube backlink templates
- `cors-proxies.json` - CORS proxy list used by URL testing
- `domains-sample.txt` - Sample domains file for batch processing
- `PROJECT_SUMMARY.md` - Project overview and feature summary
- `PYTHON_README.md` - Full Python documentation
- `QUICK_START.md` - Quick start guide
- `START_HERE.md` - Starter notes

## Features

- Generate thousands of backlink URLs per domain
- Support for standard and YouTube backlink templates
- Placeholder-driven template expansion
- Optional URL testing to verify generated links
- CSV/JSON/TXT export support
- Batch processing for multiple domains
- Built with Python standard library only

## Quick Start

### Windows
```powershell
backlink.bat example.com
```

### macOS / Linux
```bash
chmod +x backlink.sh
./backlink.sh example.com
```

### Direct Python usage
```bash
python backlink-generator.py example.com
```

## Advanced Usage

```bash
python advanced-backlink-generator.py --batch domains.txt --test
```

```bash
python advanced-backlink-generator.py example.com --report --export-formats csv,json,txt
```

## Common Options

- `--test` — validate generated URLs
- `--output` — save results to a custom file
- `--limit` — limit displayed results
- `--no-shuffle` — preserve template order
- `--config-dir` — specify a custom template directory

## How it Works

1. Load backlink templates from JSON
2. Normalize the input domain or URL
3. Map placeholders to actual values
4. Generate backlink URLs from templates
5. Optionally test generated links
6. Export results to CSV or additional formats

## Requirements

- Python 3.6+
- No external packages required

## Notes

- Keep the JSON template files and scripts together in the same directory.
- Use `domains-sample.txt` as a reference for batch input.
- Review `PYTHON_README.md` and `QUICK_START.md` for deeper usage details.
