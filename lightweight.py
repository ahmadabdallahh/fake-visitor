#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Lightweight Load Testing - خفيف على الموارد وسريع
"""

import requests
import time
import random
from datetime import datetime
import threading
import queue

class LightweightTester:
    def __init__(self, url, total_requests=5000, workers=5):
        self.url = url
        self.total_requests = total_requests
        self.workers = workers
        self.success_count = 0
        self.error_count = 0
        self.start_time = None
        self.lock = threading.Lock()
        self.request_queue = queue.Queue()

        # Simple user agents
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        ]

    def worker(self, worker_id):
        """Single worker thread - minimal resource usage"""
        session = requests.Session()
        session.headers.update({
            'User-Agent': random.choice(self.user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'keep-alive',
        })

        while True:
            try:
                request_id = self.request_queue.get_nowait()
            except queue.Empty:
                break

            try:
                response = session.get(self.url, timeout=3)

                with self.lock:
                    if response.status_code == 200:
                        self.success_count += 1
                    else:
                        self.error_count += 1

                # Progress every 50 requests
                with self.lock:
                    total_completed = self.success_count + self.error_count
                    if total_completed % 50 == 0:
                        elapsed = time.time() - self.start_time
                        rps = total_completed / elapsed if elapsed > 0 else 0
                        print(f"⚡ Progress: {total_completed}/{self.total_requests} - {rps:.1f} RPS - Success: {self.success_count}")

            except Exception:
                with self.lock:
                    self.error_count += 1

            self.request_queue.task_done()

            # Small delay to prevent CPU overload
            time.sleep(0.01)

    def run_test(self):
        """Run lightweight test"""
        print(f"⚡ LIGHTWEIGHT MODE - {self.total_requests} requests")
        print(f"📍 URL: {self.url}")
        print(f"👥 Workers: {self.workers} (low resource usage)")
        print(f"🔋 Optimized for CPU/RAM efficiency")
        print("=" * 50)

        # Fill queue with requests
        for i in range(1, self.total_requests + 1):
            self.request_queue.put(i)

        self.start_time = time.time()

        # Start worker threads
        threads = []
        for i in range(self.workers):
            thread = threading.Thread(target=self.worker, args=(i+1,))
            thread.start()
            threads.append(thread)

        # Wait for all threads to complete
        for thread in threads:
            thread.join()

        end_time = time.time()
        total_time = end_time - self.start_time

        # Results
        print("=" * 50)
        print("🏁 LIGHTWEIGHT TEST COMPLETED!")
        print("=" * 50)
        print(f"⏱️  Total time: {total_time:.2f} seconds")
        print(f"✅ Successful: {self.success_count}")
        print(f"❌ Failed: {self.error_count}")
        print(f"📊 Success rate: {(self.success_count/self.total_requests*100):.1f}%")
        print(f"🔥 Average RPS: {self.total_requests/total_time:.1f}")
        print(f"💡 Low resource usage: {self.workers} threads")
        print("=" * 50)

def main():
    print("💡 LIGHTWEIGHT LOAD TESTER")
    print("-" * 35)
    print("🔋 Optimized for low CPU/RAM usage")
    print("⚡ Still fast but resource-friendly")
    print("-" * 35)

    url = input("🌐 Enter URL: ").strip()
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url

    requests_count = int(input("📊 Number of requests (default 5000): ") or "5000")
    workers = int(input("👥 Workers (default 5): ") or "5")

    print(f"\n⚡ Starting lightweight test...")
    print("💡 This won't overload your computer!")

    tester = LightweightTester(url, requests_count, workers)

    try:
        tester.run_test()
    except KeyboardInterrupt:
        print("\n\n⏹️  TEST STOPPED BY USER (Ctrl+C)")
        print("💡 Lightweight test cancelled!")
        sys.exit(0)

if __name__ == "__main__":
    main()
