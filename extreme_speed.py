#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EXTREME SPEED Load Testing - أقصى سرعة ممكنة!
"""

import requests
import time
import random
from datetime import datetime
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import sys

class ExtremeSpeedTester:
    def __init__(self, url, total_requests=20000, concurrent_users=200):
        self.url = url
        self.total_requests = total_requests
        self.concurrent_users = concurrent_users
        self.success_count = 0
        self.error_count = 0
        self.start_time = None
        self.lock = threading.Lock()

        # Ultra minimal headers for maximum speed
        self.base_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Connection': 'keep-alive',
        }

    def single_request(self, request_id):
        """Execute a single request - EXTREME SPEED version"""
        try:
            # Use raw requests for maximum speed
            headers = self.base_headers.copy()
            headers['User-Agent'] = f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

            # No session, no cookies, no delays - PURE SPEED
            response = requests.get(
                self.url,
                headers=headers,
                timeout=1,  # Ultra fast timeout
                stream=False  # Don't stream for speed
            )

            with self.lock:
                if response.status_code == 200:
                    self.success_count += 1
                else:
                    self.error_count += 1

            # Show progress every 25 requests (even more frequent)
            if request_id % 25 == 0:
                elapsed = time.time() - self.start_time
                rps = request_id / elapsed if elapsed > 0 else 0
                print(f"⚡ {request_id}/{self.total_requests} - {rps:.1f} RPS - ✅{self.success_count}")

        except Exception:
            with self.lock:
                self.error_count += 1

    def run_test(self):
        """Run EXTREME SPEED test"""
        print(f"⚡ EXTREME SPEED MODE - {self.total_requests} requests")
        print(f"📍 URL: {self.url}")
        print(f"🚀 Concurrent users: {self.concurrent_users}")
        print(f"⚡ NO DELAYS - MAXIMUM SPEED!")
        print(f"🔥 Timeout: 1 second - Ultra fast!")
        print("=" * 60)

        self.start_time = time.time()

        # Use ThreadPoolExecutor with maximum workers
        with ThreadPoolExecutor(max_workers=self.concurrent_users) as executor:
            # Submit all tasks at once for maximum speed
            futures = [executor.submit(self.single_request, i) for i in range(1, self.total_requests + 1)]

            # Process as they complete
            completed = 0
            for future in as_completed(futures):
                try:
                    future.result()
                    completed += 1

                    # Show completion percentage
                    if completed % 500 == 0:
                        elapsed = time.time() - self.start_time
                        rps = completed / elapsed if elapsed > 0 else 0
                        progress = (completed / self.total_requests) * 100
                        print(f"🎯 {progress:.1f}% - {rps:.1f} RPS")

                except:
                    pass

        end_time = time.time()
        total_time = end_time - self.start_time

        # Final results
        print("=" * 60)
        print("🏁 EXTREME SPEED TEST COMPLETED!")
        print("=" * 60)
        print(f"⏱️  Total time: {total_time:.2f} seconds")
        print(f"✅ Successful: {self.success_count}")
        print(f"❌ Failed: {self.error_count}")
        print(f"📊 Success rate: {(self.success_count/self.total_requests*100):.1f}%")
        print(f"🔥 Average RPS: {self.total_requests/total_time:.1f}")
        print(f"⚡ Peak performance: {self.concurrent_users} concurrent threads")
        print(f"🚀 Speed mode: EXTREME")
        print("=" * 60)

def main():
    print("⚡ EXTREME SPEED LOAD TESTER")
    print("-" * 50)
    print("🚀 MAXIMUM SPEED POSSIBLE")
    print("⚡ 200+ concurrent threads")
    print("🔥 1 second timeout")
    print("💨 No delays, no waiting")
    print("-" * 50)

    url = input("🌐 Enter URL: ").strip()
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url

    requests_count = int(input("📊 Number of requests (default 20000): ") or "20000")
    concurrent = int(input("⚡ Concurrent users (default 200): ") or "200")

    print(f"\n⚡ Starting EXTREME SPEED test...")
    print("🚀 WARNING: This will generate INSANE traffic!")
    print("💻 Make sure your computer can handle this!")

    tester = ExtremeSpeedTester(url, requests_count, concurrent)

    try:
        tester.run_test()
    except KeyboardInterrupt:
        print("\n\n⏹️  EXTREME SPEED TEST STOPPED!")
        print("🔥 Speed test cancelled by user!")
        sys.exit(0)

if __name__ == "__main__":
    main()
