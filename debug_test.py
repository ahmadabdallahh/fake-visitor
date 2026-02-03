#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Debug Test Script - لتشخيص مشاكل الزيارات
"""

import requests
import time
import json
from datetime import datetime

def debug_website(url):
    """فحص الموقع وتشخيص المشاكل"""
    print(f"🔍 Debugging: {url}")
    print("=" * 50)

    # 1. Test basic connection
    print("1️⃣ Testing basic connection...")
    try:
        response = requests.get(url, timeout=10)
        print(f"   ✅ Status: {response.status_code}")
        print(f"   ✅ Response size: {len(response.content)} bytes")
        print(f"   ✅ Headers: {dict(response.headers)}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return

    # 2. Check for JavaScript requirements
    print("\n2️⃣ Checking JavaScript requirements...")
    if 'javascript' in response.text.lower():
        print("   ⚠️  Website requires JavaScript!")
        print("   💡 Your fake visitors might not be counted")

    # 3. Check for analytics scripts
    print("\n3️⃣ Looking for analytics scripts...")
    analytics_found = []
    if 'google-analytics' in response.text:
        analytics_found.append('Google Analytics')
    if 'facebook.com/tr' in response.text:
        analytics_found.append('Facebook Pixel')
    if 'googletagmanager' in response.text:
        analytics_found.append('Google Tag Manager')
    if 'mixpanel' in response.text:
        analytics_found.append('Mixpanel')
    if 'hotjar' in response.text:
        analytics_found.append('Hotjar')

    if analytics_found:
        print(f"   ✅ Found: {', '.join(analytics_found)}")
    else:
        print("   ❌ No analytics scripts detected")

    # 4. Test with different user agents
    print("\n4️⃣ Testing different User-Agents...")
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 16_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Mobile/15E148 Safari/604.1'
    ]

    for i, ua in enumerate(user_agents):
        try:
            headers = {'User-Agent': ua}
            resp = requests.get(url, headers=headers, timeout=10)
            print(f"   ✅ UA {i+1}: {resp.status_code}")
        except Exception as e:
            print(f"   ❌ UA {i+1}: {e}")

    # 5. Test with cookies
    print("\n5️⃣ Testing with cookies...")
    session = requests.Session()
    session.cookies.set('test_visit', 'true')
    session.cookies.set('timestamp', str(int(time.time())))

    try:
        resp = session.get(url, timeout=10)
        print(f"   ✅ With cookies: {resp.status_code}")
        print(f"   🍪 Cookies set: {dict(session.cookies)}")
    except Exception as e:
        print(f"   ❌ With cookies: {e}")

    # 6. Test multiple requests
    print("\n6️⃣ Testing multiple rapid requests...")
    success_count = 0
    for i in range(5):
        try:
            resp = requests.get(url, timeout=5)
            if resp.status_code == 200:
                success_count += 1
            print(f"   Request {i+1}: {resp.status_code}")
            time.sleep(1)  # 1 second delay
        except Exception as e:
            print(f"   Request {i+1}: Error - {e}")

    print(f"\n📊 Success rate: {success_count}/5 ({success_count/5*100:.1f}%)")

    # 7. Recommendations
    print("\n💡 Recommendations:")
    if 'javascript' in response.text.lower():
        print("   🔄 Use Selenium or Playwright for JavaScript-heavy sites")
    if not analytics_found:
        print("   📊 Install analytics tools to track visitors")
    if success_count < 5:
        print("   ⏱️  Increase delays between requests")

    print("   🔍 Check server logs for incoming requests")
    print("   📈 Verify analytics configuration")

def main():
    print("🔧 Website Debug Tool")
    print("-" * 30)

    url = input("🌐 Enter your website URL: ").strip()
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url

    debug_website(url)

if __name__ == "__main__":
    main()
