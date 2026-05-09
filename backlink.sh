#!/bin/bash
# Backlink Generator Shell Script for Linux/Mac
# Makes it easy to run the Python script

if [ -z "$1" ]; then
    echo ""
    echo "Backlink Generator Tool"
    echo "======================="
    echo ""
    echo "Usage:"
    echo "  ./backlink.sh <domain> [options]"
    echo ""
    echo "Examples:"
    echo "  ./backlink.sh example.com"
    echo "  ./backlink.sh example.com --test"
    echo "  ./backlink.sh example.com --test --output backlinks.csv"
    echo "  ./backlink.sh example.com --limit 20"
    echo ""
    python3 backlink-generator.py
else
    python3 backlink-generator.py "$@"
fi
