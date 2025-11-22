#!/usr/bin/env python3
"""
Script para extraer solo las cookies de YouTube de un archivo grande
"""

import sys

def extract_youtube_cookies(input_file, output_file):
    """Extract only YouTube-related cookies from a large cookies file"""
    youtube_cookies = []
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                # Keep header comments
                if line.startswith('#'):
                    if 'Netscape' in line or 'HTTP Cookie' in line:
                        youtube_cookies.append(line)
                # Keep only YouTube and Google Video cookies
                elif 'youtube.com' in line or 'googlevideo.com' in line or 'google.com' in line:
                    youtube_cookies.append(line)
        
        # Write filtered cookies
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(youtube_cookies))
        
        print(f"✅ Extraídas {len(youtube_cookies)} cookies de YouTube")
        print(f"📁 Guardadas en: {output_file}")
        print(f"\n📋 Ahora copia el contenido de '{output_file}' a la variable YOUTUBE_COOKIES en Render")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    input_file = '95f608f8-5ce2-4786-9340-8b5e5eeee403.txt'
    output_file = 'youtube_cookies_only.txt'
    
    extract_youtube_cookies(input_file, output_file)
