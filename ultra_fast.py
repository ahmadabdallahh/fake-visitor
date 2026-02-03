#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ultra Fast Load Testing - أسرع سكريبت للزيارات
"""

import requests
import time
import random
from datetime import datetime
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import sys

class UltraFastTester:
    def __init__(self, url, total_requests=10000, concurrent_users=50):
        self.url = url
        self.total_requests = total_requests
        self.concurrent_users = concurrent_users
        self.success_count = 0
        self.error_count = 0
        self.start_time = None
        self.lock = threading.Lock()

        # Minimal fake users for speed
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        ]

        self.user_names = ['User1', 'User2', 'User3', 'User4', 'User5']

    def single_request(self, request_id):
        """Execute a single request - ultra fast version"""
        try:
            headers = {
                'User-Agent': random.choice(self.user_agents),
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
            }

            # Simple session with minimal cookies
            session = requests.Session()
            session.headers.update(headers)
            session.cookies.set('user_id', str(random.randint(1, 1000)))
            session.cookies.set('session', f'sess_{random.randint(10000, 99999)}')

            response = session.get(self.url, timeout=2)

            with self.lock:
                if response.status_code == 200:
                    self.success_count += 1
                else:
                    self.error_count += 1

            # Show progress every 50 requests (more frequent updates)
            if request_id % 50 == 0:
                elapsed = time.time() - self.start_time
                rps = request_id / elapsed if elapsed > 0 else 0
                print(f"🚀 {request_id}/{self.total_requests} - {rps:.1f} RPS - Success: {self.success_count}")

        except Exception:
            with self.lock:
                self.error_count += 1

    def run_test(self):
        """Run ultra fast test"""
        print(f"🚀 ULTRA FAST MODE - {self.total_requests} requests")
        print(f"📍 URL: {self.url}")
        print(f"⚡ Concurrent users: {self.concurrent_users}")
        print(f"🔥 NO DELAYS - MAXIMUM SPEED!")
        print("=" * 60)

        self.start_time = time.time()

        # Use ThreadPoolExecutor for maximum speed
        with ThreadPoolExecutor(max_workers=self.concurrent_users) as executor:
            # Submit all tasks
            futures = [executor.submit(self.single_request, i) for i in range(1, self.total_requests + 1)]

            # Wait for completion
            for future in as_completed(futures):
                try:
                    future.result()
                except:
                    pass

        end_time = time.time()
        total_time = end_time - self.start_time

        # Final results
        print("=" * 60)
        print("🏁 ULTRA FAST TEST COMPLETED!")
        print("=" * 60)
        print(f"⏱️  Total time: {total_time:.2f} seconds")
        print(f"✅ Successful: {self.success_count}")
        print(f"❌ Failed: {self.error_count}")
        print(f"📊 Success rate: {(self.success_count/self.total_requests*100):.1f}%")
        print(f"🔥 Average RPS: {self.total_requests/total_time:.1f}")
        print(f"⚡ Peak performance: {self.concurrent_users} concurrent threads")
        print("=" * 60)

def main():
    print("⚡ ULTRA FAST LOAD TESTER")
    print("-" * 40)

    url = input("🌐 Enter URL: ").strip()
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url

    requests_count = int(input("📊 Number of requests (default 10000): ") or "10000")
    concurrent = int(input("⚡ Concurrent users (default 100): ") or "100")

    print(f"\n🚀 Starting ultra fast test...")
    print("⚠️  WARNING: This will generate VERY high traffic!")

    tester = UltraFastTester(url, requests_count, concurrent)

    try:
        tester.run_test()
    except KeyboardInterrupt:
        print("\n\n⏹️  TEST STOPPED BY USER (Ctrl+C)")
        print("🔥 Ultra fast test cancelled!")
        sys.exit(0)

if __name__ == "__main__":
    main()
