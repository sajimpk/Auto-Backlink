#!/usr/bin/env python3
"""
Backlink Generator Tool - Advanced Version
Batch processing, URL testing, scheduling, and advanced features
"""

import json
import sys
import os
import re
import csv
import argparse
import time
import threading
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Set
from collections import defaultdict
import concurrent.futures
import sys
import importlib.util

# Load backlink-generator.py as module
spec = importlib.util.spec_from_file_location("backlink_generator", "backlink-generator.py")
backlink_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(backlink_module)
BacklinkGenerator = backlink_module.BacklinkGenerator


class AdvancedBacklinkGenerator(BacklinkGenerator):
    """Extended backlink generator with advanced features"""
    
    def __init__(self, config_dir: str = "."):
        super().__init__(config_dir)
        self.test_results = defaultdict(lambda: {'success': 0, 'failed': 0, 'total': 0})
        self.cache = {}

    def test_urls_concurrent(self, urls: List[str], max_workers: int = 10, timeout: int = 5) -> Dict[str, bool]:
        """Test multiple URLs concurrently"""
        results = {}
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(self.test_url, url, timeout): url for url in urls}
            
            completed = 0
            for future in concurrent.futures.as_completed(futures):
                url = futures[future]
                try:
                    result = future.result()
                    results[url] = result
                    completed += 1
                    print(f"✓ Tested {completed}/{len(urls)} URLs...", end='\r')
                except Exception as e:
                    results[url] = False
                    completed += 1
        
        print(" " * 50, end='\r')  # Clear progress line
        return results

    def batch_process(self, domains: List[str], test_urls: bool = False, 
                     max_workers: int = 10, output_dir: str = ".") -> Dict[str, str]:
        """Process multiple domains in batch"""
        results_files = {}
        
        print(f"\n📦 Batch processing {len(domains)} domains...")
        print("=" * 70)
        
        for idx, domain in enumerate(domains, 1):
            print(f"\n[{idx}/{len(domains)}] Processing: {domain}")
            print("-" * 70)
            
            try:
                results = self.generate_backlinks(domain, test_urls=test_urls, shuffle=True)
                
                if results:
                    # Generate filename
                    clean_domain = domain.replace('://', '_').replace('/', '_').replace('?', '_')
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = os.path.join(output_dir, f"backlinks_{clean_domain}_{timestamp}.csv")
                    
                    # Save results
                    self.save_results(results, filename)
                    results_files[domain] = filename
                    
                    # Print summary
                    print(f"✓ Generated {len(results)} backlinks")
                    if test_urls:
                        successful = sum(1 for r in results if r.get('status') == '✓')
                        rate = (successful * 100) // len(results)
                        print(f"📊 Success rate: {successful}/{len(results)} ({rate}%)")
                
            except Exception as e:
                print(f"✗ Error processing {domain}: {e}")
        
        return results_files

    def analyze_templates(self, sample_url: str = "example.com") -> Dict[str, Dict]:
        """Analyze template performance"""
        print(f"\n📊 Analyzing templates with sample URL: {sample_url}")
        print("=" * 70)
        
        normalized = self.normalize_url(sample_url)
        if not normalized:
            print("Invalid URL")
            return {}
        
        analysis = {
            'total_templates': len(self.backlink_templates),
            'templates_by_type': defaultdict(int),
            'sample_outputs': [],
            'archive_templates': [],
            'youtube_templates': len(self.youtube_templates)
        }
        
        # Analyze each template
        for idx, template in enumerate(self.backlink_templates[:50]):  # Sample first 50
            try:
                final_url = self.generate_url(template, normalized)
                
                domain = final_url.split('/')[2] if final_url else 'unknown'
                analysis['templates_by_type'][domain] += 1
                
                if idx < 10:  # Store sample outputs
                    analysis['sample_outputs'].append({
                        'template': template[:100],
                        'output': final_url[:100]
                    })
                
                # Check if archive
                if self.is_archive_host(domain):
                    analysis['archive_templates'].append(template)
                    
            except Exception as e:
                pass
        
        # Print analysis
        print(f"\nTotal backlink templates: {analysis['total_templates']}")
        print(f"YouTube templates: {analysis['youtube_templates']}")
        print(f"Archive templates: {len(analysis['archive_templates'])}")
        print(f"Unique domains using templates: {len(analysis['templates_by_type'])}")
        
        print(f"\nTop 10 most used domains in templates:")
        sorted_domains = sorted(analysis['templates_by_type'].items(), key=lambda x: x[1], reverse=True)
        for domain, count in sorted_domains[:10]:
            print(f"  {domain}: {count} templates")
        
        return analysis

    def filter_results(self, results: List[Dict], filter_type: str = None,
                      domain_filter: str = None) -> List[Dict]:
        """Filter results by various criteria"""
        filtered = results
        
        if filter_type:
            filtered = [r for r in filtered if r.get('type') == filter_type]
        
        if domain_filter:
            filtered = [r for r in filtered if domain_filter.lower() in r.get('url', '').lower()]
        
        return filtered

    def deduplicate_results(self, results: List[Dict]) -> List[Dict]:
        """Remove duplicate URLs from results"""
        seen = set()
        unique = []
        
        for result in results:
            url = result['url']
            if url not in seen:
                seen.add(url)
                unique.append(result)
        
        return unique

    def merge_results(self, *result_lists) -> List[Dict]:
        """Merge multiple result lists"""
        merged = []
        index = 1
        
        for results in result_lists:
            for result in results:
                result['index'] = index
                merged.append(result)
                index += 1
        
        return self.deduplicate_results(merged)

    def export_to_formats(self, results: List[Dict], base_filename: str, 
                         formats: List[str] = None) -> Dict[str, str]:
        """Export results to multiple formats"""
        if formats is None:
            formats = ['csv', 'json', 'txt']
        
        exported = {}
        base = os.path.splitext(base_filename)[0]
        
        for fmt in formats:
            try:
                if fmt == 'csv':
                    filename = f"{base}.csv"
                    with open(filename, 'w', newline='', encoding='utf-8') as f:
                        if results:
                            writer = csv.DictWriter(f, fieldnames=results[0].keys())
                            writer.writeheader()
                            writer.writerows(results)
                    exported['csv'] = filename
                    print(f"✓ Exported to CSV: {filename}")
                
                elif fmt == 'json':
                    filename = f"{base}.json"
                    with open(filename, 'w', encoding='utf-8') as f:
                        json.dump(results, f, indent=2)
                    exported['json'] = filename
                    print(f"✓ Exported to JSON: {filename}")
                
                elif fmt == 'txt':
                    filename = f"{base}.txt"
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write("BACKLINKS REPORT\n")
                        f.write("=" * 80 + "\n\n")
                        for result in results:
                            f.write(f"[{result['index']}] {result['url']}\n")
                    exported['txt'] = filename
                    print(f"✓ Exported to TXT: {filename}")
                
            except Exception as e:
                print(f"✗ Error exporting to {fmt}: {e}")
        
        return exported

    def generate_report(self, results: List[Dict], domain: str) -> str:
        """Generate a detailed report"""
        report = f"""
╔═══════════════════════════════════════════════════════════════════════════╗
║                       BACKLINK GENERATION REPORT                          ║
╚═══════════════════════════════════════════════════════════════════════════╝

Target Domain: {domain}
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

SUMMARY
{'─' * 75}
Total Backlinks:        {len(results)}
Successfully Tested:    {sum(1 for r in results if r.get('status') == '✓')}
Failed Tests:           {sum(1 for r in results if r.get('status') == '✗')}
Regular Links:          {sum(1 for r in results if r.get('type') == 'regular')}
Archive Variants:       {sum(1 for r in results if r.get('type') == 'archive_variant')}

URL SAMPLE (First 10)
{'─' * 75}
"""
        for result in results[:10]:
            status = result.get('status', '-')
            url = result['url']
            if len(url) > 70:
                url = url[:67] + "..."
            report += f"{status:<3} {url}\n"
        
        if len(results) > 10:
            report += f"\n... and {len(results) - 10} more backlinks\n"
        
        report += f"\n{'═' * 75}\n"
        report += f"End of Report\n"
        
        return report


def main():
    parser = argparse.ArgumentParser(
        description='Advanced Backlink Generator - Batch processing and analysis',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Batch process multiple domains
  python advanced-backlink-generator.py --batch domains.txt
  
  # Analyze template performance
  python advanced-backlink-generator.py --analyze example.com
  
  # Process domain and export to multiple formats
  python advanced-backlink-generator.py example.com --export-formats csv,json,txt
  
  # Test URLs concurrently
  python advanced-backlink-generator.py example.com --test --workers 20
        """
    )

    parser.add_argument('domain', nargs='?', help='Single domain to process')
    parser.add_argument('--batch', help='File containing list of domains (one per line)')
    parser.add_argument('--analyze', action='store_true', help='Analyze template performance')
    parser.add_argument('--test', action='store_true', help='Test if generated URLs are accessible')
    parser.add_argument('--workers', type=int, default=10, help='Number of concurrent workers for testing')
    parser.add_argument('--output-dir', '-d', default='.', help='Output directory for results')
    parser.add_argument('--export-formats', default='csv', help='Export formats (csv,json,txt)')
    parser.add_argument('--no-shuffle', dest='shuffle', action='store_false', default=True)
    parser.add_argument('--config-dir', default='.', help='Directory with template JSON files')
    parser.add_argument('--limit', type=int, help='Limit displayed results')
    parser.add_argument('--report', action='store_true', help='Generate detailed report')

    args = parser.parse_args()

    # Initialize generator
    generator = AdvancedBacklinkGenerator(config_dir=args.config_dir)

    # Analyze templates
    if args.analyze:
        domain = args.domain or "example.com"
        generator.analyze_templates(domain)
        return

    # Batch processing
    if args.batch:
        if not os.path.exists(args.batch):
            print(f"✗ File not found: {args.batch}")
            return
        
        with open(args.batch, 'r') as f:
            domains = [line.strip() for line in f if line.strip()]
        
        results = generator.batch_process(domains, test_urls=args.test, 
                                        max_workers=args.workers,
                                        output_dir=args.output_dir)
        
        print(f"\n✓ Batch processing complete")
        print(f"📊 Generated files for {len(results)} domains:")
        for domain, filename in results.items():
            print(f"  {domain}: {filename}")
        return

    # Single domain processing
    if not args.domain:
        domain = input("Enter domain or URL (e.g., example.com): ").strip()
        if not domain:
            print("No domain provided")
            return
    else:
        domain = args.domain

    print(f"\n🔗 Generating backlinks for: {domain}")
    results = generator.generate_backlinks(domain, test_urls=args.test, shuffle=args.shuffle)

    if results:
        # Display results
        generator.display_results(results, limit=args.limit)

        # Generate report if requested
        if args.report:
            report = generator.generate_report(results, domain)
            print(report)
            
            # Save report
            report_file = os.path.join(args.output_dir, f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"✓ Report saved to: {report_file}")

        # Export to multiple formats
        formats = [f.strip() for f in args.export_formats.split(',')]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_filename = os.path.join(args.output_dir, f"backlinks_{timestamp}")
        
        exported = generator.export_to_formats(results, base_filename, formats)

        # Summary
        print(f"\n✓ Complete! Generated {len(results)} backlinks")
    else:
        print("No backlinks generated")


if __name__ == '__main__':
    main()
