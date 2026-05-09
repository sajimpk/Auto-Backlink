#!/usr/bin/env python3
"""
Backlink Generator Tool - Python Version
Converts the JavaScript tool to Python for command-line usage
Generates backlinks by creating URLs from templates with placeholders
"""

import json
import sys
import os
import re
import csv
import argparse
import urllib.parse
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional, Tuple
import time

# Archive TLDs for variant grouping
ARCHIVE_TLDS = ["archive.today", "archive.li", "archive.vn", "archive.fo", "archive.md", "archive.ph", "archive.is"]

class BacklinkGenerator:
    def __init__(self, config_dir: str = "."):
        """Initialize the backlink generator with templates from JSON files"""
        self.config_dir = config_dir
        self.backlink_templates = []
        self.youtube_templates = []
        self.cors_proxies = []
        self.load_templates()

    def load_templates(self):
        """Load templates from JSON files"""
        templates_file = os.path.join(self.config_dir, "backlink-templates.json")
        youtube_file = os.path.join(self.config_dir, "youtube-backlink-templates.json")
        cors_file = os.path.join(self.config_dir, "cors-proxies.json")

        try:
            with open(templates_file, 'r', encoding='utf-8') as f:
                self.backlink_templates = json.load(f)
                print(f"✓ Loaded {len(self.backlink_templates)} backlink templates")
        except FileNotFoundError:
            print(f"⚠ Warning: {templates_file} not found, using defaults")
            self.backlink_templates = []

        try:
            with open(youtube_file, 'r', encoding='utf-8') as f:
                self.youtube_templates = json.load(f)
                print(f"✓ Loaded {len(self.youtube_templates)} YouTube templates")
        except FileNotFoundError:
            print(f"⚠ Warning: {youtube_file} not found")
            self.youtube_templates = []

        try:
            with open(cors_file, 'r', encoding='utf-8') as f:
                self.cors_proxies = json.load(f)
                print(f"✓ Loaded {len(self.cors_proxies)} CORS proxies")
        except FileNotFoundError:
            print(f"⚠ Warning: {cors_file} not found")
            self.cors_proxies = []

    def normalize_url(self, raw_url: str) -> Optional[str]:
        """Normalize and validate a URL"""
        if not raw_url or not isinstance(raw_url, str):
            return None

        raw_url = raw_url.strip()

        # Try to decode if percent-encoded
        try:
            decoded = urllib.parse.unquote(raw_url)
            if decoded and decoded != raw_url:
                raw_url = decoded
        except:
            pass

        # Add https:// if no scheme
        if not re.match(r'^[a-zA-Z][a-zA-Z0-9+\-.]*://', raw_url):
            raw_url = 'https://' + raw_url

        try:
            from urllib.parse import urlparse
            parsed = urlparse(raw_url)
            
            # Validate hostname
            hostname = parsed.hostname
            if not hostname:
                return None

            # Remove www prefix
            hostname = hostname.replace('www.', '', 1)
            
            # Reconstruct URL
            if parsed.port:
                netloc = f"{hostname}:{parsed.port}"
            else:
                netloc = hostname

            # Remove trailing slash if no path
            path = parsed.path if parsed.path and parsed.path != '/' else ''
            
            result = f"{parsed.scheme}://{netloc}{path}"
            if parsed.query:
                result += f"?{parsed.query}"
            if parsed.fragment:
                result += f"#{parsed.fragment}"
            
            return result
        except:
            return None

    def is_archive_host(self, hostname: str) -> bool:
        """Check if hostname is an archive.* TLD"""
        return hostname.lower() in ARCHIVE_TLDS

    def build_url_map(self, url: str, video_id: Optional[str] = None) -> Dict[str, str]:
        """Build a map of placeholders for template replacement"""
        from urllib.parse import urlparse, quote
        
        try:
            parsed = urlparse(url)
            parts = parsed.hostname.split('.')
            ln = len(parts)

            hostname_no_www = parsed.hostname.replace('www.', '', 1)
            
            url_map = {
                'PROTOCOL': parsed.scheme + ':',
                'SUBDOMAIN': '.'.join(parts[:-2]) + '.' if ln > 2 else '',
                'DOMAINNAME': parts[-2] if ln >= 2 else '',
                'TLD': parts[-1] if ln >= 1 else '',
                'HOST': parsed.hostname,
                'PORT': f':{parsed.port}' if parsed.port else '',
                'PATH': parsed.path,
                'QUERY': parsed.query if parsed.query else '',
                'PARAMS': parsed.query[1:] if parsed.query else '',
                'FRAGMENT': parsed.fragment if parsed.fragment else '',
                'URL': url,
                'DOMAIN': parsed.hostname,
                'NOPROTOCOL_URL': f"{parsed.hostname}{parsed.path}{'?' + parsed.query if parsed.query else ''}{'#' + parsed.fragment if parsed.fragment else ''}",
                'NOSUBDOMAIN_URL': f"{hostname_no_www}{parsed.path}{'?' + parsed.query if parsed.query else ''}{'#' + parsed.fragment if parsed.fragment else ''}"
            }

            if video_id:
                url_map['ID'] = video_id

            # Add encoded versions
            for key in list(url_map.keys()):
                try:
                    url_map[f'ENCODE_{key}'] = quote(str(url_map[key]), safe='')
                except:
                    url_map[f'ENCODE_{key}'] = ''

            return url_map
        except Exception as e:
            print(f"Error building URL map: {e}")
            return {}

    def replace_placeholders(self, template: str, url_map: Dict[str, str]) -> str:
        """Replace placeholders in template with values from map"""
        result = template
        
        # Pattern matches [KEY], {{KEY}}, [ENCODE_KEY], {{ENCODE_KEY}}
        pattern = r'(\{\{|\[)\s*(ENCODE_)?([A-Z0-9_]+)\s*(\}\}|\])'
        
        def replace_func(match):
            open_bracket, encode_prefix, key, close_bracket = match.groups()
            key = key.upper()
            
            if encode_prefix:
                encoded_key = f'ENCODE_{key}'
                return url_map.get(encoded_key, '')
            else:
                return url_map.get(key, '')
        
        result = re.sub(pattern, replace_func, result)
        return result

    def generate_url(self, template: str, normalized_url: str, video_id: Optional[str] = None) -> str:
        """Generate a backlink URL from template"""
        if not template:
            return ''

        # Normalize template encoding
        template = re.sub(r'%5B\s*(ENCODE_)?([A-Z0-9_]+)\s*%5D', r'[\1\2]', template)
        template = re.sub(r'%7B%7B\s*(ENCODE_)?([A-Z0-9_]+)\s*%7D%7D', r'{{\1\2}}', template)

        url_map = self.build_url_map(normalized_url, video_id)
        return self.replace_placeholders(template, url_map)

    def build_archive_url_variants(self, final_url: str) -> Optional[List[str]]:
        """Build archive.* TLD variants for a URL"""
        try:
            from urllib.parse import urlparse
            parsed = urlparse(final_url)
            
            if not self.is_archive_host(parsed.hostname):
                return None
            
            variants = []
            for tld in ARCHIVE_TLDS:
                # Replace the archive TLD
                url_with_tld = final_url.replace(parsed.hostname, tld)
                variants.append(url_with_tld)
            
            return variants
        except:
            return None

    def extract_youtube_id(self, url: str) -> Optional[str]:
        """Extract YouTube video ID from URL"""
        patterns = [
            r'(?:youtube\.com\/watch\?v=|youtu\.be\/)([^&\n?#]+)',
            r'youtube\.com/embed/([^&\n?#]+)',
            r'youtube\.com/v/([^&\n?#]+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        
        return None

    def test_url(self, url: str, timeout: int = 5) -> bool:
        """Test if a URL is accessible"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            req = Request(url, headers=headers)
            response = urlopen(req, timeout=timeout)
            return response.status == 200
        except:
            return False

    def generate_backlinks(self, domain: str, test_urls: bool = False, shuffle: bool = True) -> List[Dict]:
        """Generate backlinks for a domain"""
        # Normalize the domain
        normalized_url = self.normalize_url(domain)
        if not normalized_url:
            print(f"✗ Invalid URL: {domain}")
            return []

        print(f"\n📍 Domain: {normalized_url}")
        print(f"{'='*70}")

        # Check if it's a YouTube link
        video_id = self.extract_youtube_id(normalized_url)
        if video_id:
            print(f"✓ Detected YouTube video ID: {video_id}")
            templates = self.youtube_templates + ['https://web.archive.org/save/[URL]']
        else:
            templates = self.backlink_templates.copy()

        if shuffle:
            import random
            random.shuffle(templates)

        # Generate URLs
        results = []
        archive_group_keys = set()

        for idx, template in enumerate(templates, 1):
            try:
                final_url = self.generate_url(template, normalized_url, video_id)
                if not final_url or not final_url.strip():
                    continue

                from urllib.parse import urlparse
                parsed = urlparse(final_url)
                is_archive = self.is_archive_host(parsed.hostname)

                # Group archive variants
                if is_archive:
                    group_key = f"{parsed.scheme}//{parsed.path}{parsed.query}{'#' + parsed.fragment if parsed.fragment else ''}"
                    if group_key in archive_group_keys:
                        continue
                    archive_group_keys.add(group_key)

                    variants = self.build_archive_url_variants(final_url)
                    if variants:
                        for variant_url in variants:
                            result = {
                                'index': len(results) + 1,
                                'url': variant_url,
                                'template': template,
                                'type': 'archive_variant'
                            }
                            
                            if test_urls:
                                result['status'] = '✓' if self.test_url(variant_url) else '✗'
                            
                            results.append(result)
                        continue

                # Regular URL
                result = {
                    'index': len(results) + 1,
                    'url': final_url,
                    'template': template,
                    'type': 'regular'
                }

                if test_urls:
                    result['status'] = '✓' if self.test_url(final_url) else '✗'

                results.append(result)

            except Exception as e:
                print(f"Error processing template {idx}: {e}")
                continue

        return results

    def save_results(self, results: List[Dict], filename: Optional[str] = None) -> str:
        """Save results to CSV file (URLs only)"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"backlinks_{timestamp}.csv"

        try:
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                # Write only URLs, one per line
                f.write("URL\n")
                for result in results:
                    f.write(result['url'] + '\n')
            
            print(f"✓ Results saved to: {filename}")
            return filename
        except Exception as e:
            print(f"✗ Error saving results: {e}")
            return ""

    def display_results(self, results: List[Dict], limit: Optional[int] = None):
        """Display results in formatted table"""
        if not results:
            print("No results generated")
            return

        display_results = results[:limit] if limit else results
        
        print(f"\n{'INDEX':<6} {'STATUS':<8} {'URL':<60}")
        print("-" * 80)

        for result in display_results:
            status = result.get('status', '-')
            url = result['url']
            if len(url) > 60:
                url = url[:57] + "..."
            print(f"{result['index']:<6} {status:<8} {url:<60}")

        if limit and len(results) > limit:
            print(f"\n... and {len(results) - limit} more results")

        print(f"\nTotal: {len(results)} backlinks generated")


def main():
    parser = argparse.ArgumentParser(
        description='Backlink Generator - Generate SEO backlinks from a domain/URL',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python backlink-generator.py example.com
  python backlink-generator.py "https://example.com/page"
  python backlink-generator.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
  python backlink-generator.py example.com --test
        """
    )

    parser.add_argument('domain', nargs='?', help='Domain or URL to generate backlinks for')
    parser.add_argument('--test', action='store_true', help='Test if generated URLs are accessible')
    parser.add_argument('--output', '-o', help='Output CSV filename (auto-generated if not specified)')
    parser.add_argument('--no-shuffle', dest='shuffle', action='store_false', default=True, help='Do not shuffle templates')
    parser.add_argument('--config-dir', default='.', help='Directory containing template JSON files')

    args = parser.parse_args()

    # Get domain from argument or interactive input
    domain = args.domain
    if not domain:
        print("\n" + "="*70)
        print("🔗 BACKLINK GENERATOR")
        print("="*70)
        domain = input("\nEnter domain or URL (e.g., example.com): ").strip()
        if not domain:
            print("❌ No domain provided")
            sys.exit(1)

    # Initialize generator
    generator = BacklinkGenerator(config_dir=args.config_dir)

    # Generate backlinks
    print(f"\n🔗 Generating backlinks for: {domain}")
    print("⏳ Please wait...\n")
    results = generator.generate_backlinks(domain, test_urls=args.test, shuffle=args.shuffle)

    # Display results
    if results:
        print(f"\n{'='*70}")
        print(f"✅ Generated {len(results)} backlinks")
        print(f"{'='*70}\n")
        generator.display_results(results)
        
        # Auto-save results with clean filename
        clean_domain = domain.replace('://', '_').replace('/', '_').replace('?', '_').replace(':', '_')[:30]
        if not args.output:
            output_file = f"backlinks_{clean_domain}.csv"
        else:
            output_file = args.output
        
        generator.save_results(results, output_file)
        
        # Summary
        print(f"\n{'='*70}")
        if args.test:
            successful = sum(1 for r in results if r.get('status') == '✓')
            rate = (successful * 100) // len(results) if results else 0
            print(f"📊 Success rate: {successful}/{len(results)} ({rate}%)")
        print(f"✅ All {len(results)} URLs saved to: {output_file}")
        print(f"{'='*70}\n")
    else:
        print("❌ No backlinks generated")
        sys.exit(1)


if __name__ == '__main__':
    main()
