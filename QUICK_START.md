# Quick Start Guide - Python Backlink Generator

## 🚀 Getting Started (2 Minutes)

### 1. **Windows Users**
```bash
# Method 1: Using batch file (easiest)
backlink.bat example.com

# Method 2: Using Python directly
python backlink-generator.py example.com
```

### 2. **Linux/Mac Users**
```bash
# Method 1: Using shell script (easiest)
chmod +x backlink.sh
./backlink.sh example.com

# Method 2: Using Python directly
python3 backlink-generator.py example.com
```

---

## 📋 Common Tasks

### Generate backlinks for your domain
```bash
python backlink-generator.py yoursite.com
```

### Generate backlinks for a specific page
```bash
python backlink-generator.py "https://yoursite.com/blog/page"
```

### Generate YouTube backlinks
```bash
python backlink-generator.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

### Test which backlinks are active
```bash
python backlink-generator.py example.com --test
```

### Save results to custom file
```bash
python backlink-generator.py example.com --output my-backlinks.csv
```

### Process multiple domains
```bash
# Create a file with domains (one per line):
# Edit domains-sample.txt or create your own

python advanced-backlink-generator.py --batch domains.txt
```

### Export to multiple formats (CSV, JSON, TXT)
```bash
python backlink-generator.py example.com --output results.csv
python advanced-backlink-generator.py example.com --export-formats csv,json,txt
```

### Generate detailed report
```bash
python advanced-backlink-generator.py example.com --test --report
```

### Analyze how templates work
```bash
python advanced-backlink-generator.py --analyze example.com
```

---

## 📊 Understanding the Output

### Console Output
```
🔗 Generating backlinks for: example.com
======================================================================

📍 Domain: https://example.com
✓ Loaded 4393 backlink templates
✓ Loaded 167 YouTube templates
✓ Loaded 4 CORS proxies

INDEX  STATUS   URL
────────────────────────────────────────────────────────────────────
1      -        https://example1.com/...
2      ✓        https://example2.com/...  (✓ = working, ✗ = broken)
3      ✗        https://example3.com/...

Total: 4417 backlinks generated

✓ Results saved to: backlinks_20240509_143022.csv
```

### CSV Output File
```
index,url,template,type,status
1,https://example1.com/...,[TEMPLATE],regular,
2,https://archive.today/...,https://web.archive.org/save/[URL],archive_variant,✓
...
```

---

## 🎯 Pro Tips

### Tip 1: Batch Processing
Create a file `sites.txt`:
```
site1.com
site2.com
https://site3.com/special-page
youtube.com/watch?v=xyz
```

Then process all at once:
```bash
python advanced-backlink-generator.py --batch sites.txt --test
```

### Tip 2: Find Working Backlinks
Only show working ones:
```bash
python backlink-generator.py example.com --test
# Then check the CSV - look for ✓ status
```

### Tip 3: Schedule Regular Runs
Create a script to run daily:

**Windows (batch):**
```batch
@echo off
cd C:\path\to\backlink-tool
python backlink-generator.py example.com >> log.txt
```

**Linux/Mac (cron):**
```bash
# Run daily at 2 AM
0 2 * * * cd /path/to/backlink-tool && python3 backlink-generator.py example.com >> log.txt
```

### Tip 4: Monitor Template Performance
```bash
python advanced-backlink-generator.py --analyze example.com
```
This shows which templates work best for your domain.

### Tip 5: Clean Results
Process and keep only active backlinks:
```bash
python backlink-generator.py example.com --test --output active-backlinks.csv
# CSV will have ✓ for working, ✗ for broken
```

---

## 🔧 Advanced Options

### Help for basic tool
```bash
python backlink-generator.py --help
```

### Help for advanced tool
```bash
python advanced-backlink-generator.py --help
```

### Common advanced options
```bash
# Process with concurrent URL testing
python backlink-generator.py example.com --test --workers 20

# Limit results display
python backlink-generator.py example.com --limit 50

# Don't shuffle (keep original order)
python backlink-generator.py example.com --no-shuffle

# Use custom template directory
python backlink-generator.py example.com --config-dir ./my-templates

# Generate report and export multiple formats
python advanced-backlink-generator.py example.com --test --report \
  --export-formats csv,json,txt --output-dir ./results
```

---

## ❓ Troubleshooting

### **"backlink-generator.py not found"**
Make sure you're in the correct directory:
```bash
cd path/to/backlink-generator-tool
```

### **"backlink-templates.json not found"**
The JSON template files must be in the same directory as the script. Download them or ensure they're in the right location.

### **"Invalid URL" error**
Use a proper domain format:
```bash
✓ Correct:   example.com
✓ Correct:   https://example.com
✓ Correct:   subdomain.example.com
✗ Wrong:     justoneword
```

### **URLs are timing out during --test**
Some backlinks might be slow. This is normal. Try:
```bash
python backlink-generator.py example.com --test  # 5 second timeout (default)
```

### **"Permission denied" on Linux/Mac**
Make the script executable:
```bash
chmod +x backlink.sh
chmod +x backlink-generator.py
```

### **Python not found**
Make sure Python 3.6+ is installed:
```bash
python --version
# or
python3 --version
```

---

## 📈 Understanding the Results

### What is a "backlink"?
A backlink is another website that links to your site. This tool generates URLs from 4000+ template websites that you can submit to various SEO services.

### Types of backlinks:
1. **Regular Links** - Standard URLs from template sites
2. **Archive Variants** - Same content on different archive services (archive.today, archive.is, etc.)
3. **YouTube Links** - Special URLs for YouTube videos

### Status meanings:
- **✓** - URL is active and working
- **✗** - URL returned an error or is inactive
- **-** - URL was not tested (use --test flag to test)

### Success Rate
```
Success rate: 120/500 (24%)
```
This means 120 out of 500 backlinks are currently working. This is normal - many backlink sources change over time.

---

## 💾 Output Files

### Default CSV
```
backlinks_20240509_143022.csv
```

### With custom name
```
python backlink-generator.py example.com --output my-results.csv
```

### Multiple formats
```
results.csv
results.json
results.txt
```

### Open results
- **CSV**: Excel, Google Sheets, any spreadsheet app
- **JSON**: Text editor, Python, JavaScript
- **TXT**: Notepad, any text editor

---

## 🔗 Useful Links

- [Original JavaScript Version](index.html)
- [Template Files](backlink-templates.json)
- [Full Documentation](PYTHON_README.md)
- [Advanced Features](advanced-backlink-generator.py)

---

## 📞 Support

For issues or questions:
1. Check the PYTHON_README.md for detailed documentation
2. Review troubleshooting section above
3. Check that all template JSON files are present
4. Ensure Python 3.6+ is installed

---

**Happy backlink generation!** 🚀
