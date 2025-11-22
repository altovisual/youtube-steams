#!/usr/bin/env python3
"""
Script para extraer solo las cookies de YouTube de un archivo grande
"""

import sys

def extract_youtube_cookies(input_file, output_file):
    """Extract only YouTube-related cookies from a large cookies file"""
    youtube_cookies = []
    
    # Add Netscape header (required format)
    youtube_cookies.append('# Netscape HTTP Cookie File')
    youtube_cookies.append('# https://curl.haxx.se/rfc/cookie_spec.html')
    youtube_cookies.append('# This is a generated file! Do not edit.')
    youtube_cookies.append('')
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            for line in f:
                line_stripped = line.strip()
                # Skip existing headers
                if line_stripped.startswith('#'):
                    continue
                # Keep only YouTube and Google cookies
                if line_stripped and ('youtube.com' in line_stripped or 'googlevideo.com' in line_stripped or '.google.com' in line_stripped):
                    youtube_cookies.append(line_stripped)
        
        # Write filtered cookies
        with open(output_file, 'w', encoding='utf-8', newline='\n') as f:
            f.write('\n'.join(youtube_cookies))
        
        cookie_count = len(youtube_cookies) - 4  # Subtract header lines
        print(f"✅ Extraídas {cookie_count} cookies de YouTube")
        print(f"📁 Guardadas en: {output_file}")
        print(f"\n📋 Ahora copia el contenido de '{output_file}' a la variable YOUTUBE_COOKIES en Render")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    input_file = '95f608f8-5ce2-4786-9340-8b5e5eeee403.txt'
    output_file = 'youtube_cookies_only.txt'
    
    extract_youtube_cookies(input_file, output_file)
