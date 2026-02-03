#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Smart Counter Load Testing - عداد ذكي يعمل 100%
"""

import requests
import time
import random
import threading
import sys

class SmartCounterTester:
    def __init__(self, url, total_requests=5000, workers=5):
        self.url = url
        self.total_requests = total_requests
        self.workers = workers
        self.success_count = 0
        self.error_count = 0
        self.completed_count = 0
        self.start_time = None
        self.lock = threading.Lock()
        self.stop_event = threading.Event()

        # Simple user agents
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        ]

        # Start progress monitor thread
        self.progress_thread = threading.Thread(target=self.progress_monitor)
        self.progress_thread.daemon = True

    def progress_monitor(self):
        """Monitor progress in separate thread"""
        while not self.stop_event.is_set() and self.completed_count < self.total_requests:
            time.sleep(2)  # Update every 2 seconds

            with self.lock:
                if self.start_time:
                    elapsed = time.time() - self.start_time
                    rps = self.completed_count / elapsed if elapsed > 0 else 0
                    progress = (self.completed_count / self.total_requests) * 100

                    print(f"📊 Progress: {self.completed_count}/{self.total_requests} ({progress:.1f}%) - {rps:.1f} RPS - ✅{self.success_count} ❌{self.error_count}")

    def worker(self, worker_id):
        """Worker thread with smart counting"""
        session = requests.Session()
        session.headers.update({
            'User-Agent': random.choice(self.user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'keep-alive',
        })

        while not self.stop_event.is_set():
            with self.lock:
                if self.completed_count >= self.total_requests:
                    break

                # Get current request number
                current_request = self.completed_count + 1
                self.completed_count += 1

            try:
                response = session.get(self.url, timeout=5)

                with self.lock:
                    if response.status_code == 200:
                        self.success_count += 1
                    else:
                        self.error_count += 1

            except Exception as e:
                with self.lock:
                    self.error_count += 1

            # Small delay
            time.sleep(0.02)

    def run_test(self):
        """Run smart counter test"""
        print(f"🧠 SMART COUNTER MODE - {self.total_requests} requests")
        print(f"📍 URL: {self.url}")
        print(f"👥 Workers: {self.workers}")
        print(f"📊 Real-time progress tracking")
        print("=" * 50)

        self.start_time = time.time()

        # Start progress monitor
        self.progress_thread.start()

        # Start worker threads
        threads = []
        for i in range(self.workers):
            thread = threading.Thread(target=self.worker, args=(i+1,))
            thread.start()
            threads.append(thread)

        # Wait for completion
        for thread in threads:
            thread.join()

        # Stop progress monitor
        self.stop_event.set()

        end_time = time.time()
        total_time = end_time - self.start_time

        # Final results
        print("\n" + "=" * 50)
        print("🏁 SMART COUNTER TEST COMPLETED!")
        print("=" * 50)
        print(f"⏱️  Total time: {total_time:.2f} seconds")
        print(f"✅ Successful: {self.success_count}")
        print(f"❌ Failed: {self.error_count}")
        print(f"📊 Total completed: {self.completed_count}")
        print(f"📈 Success rate: {(self.success_count/self.completed_count*100):.1f}%")
        print(f"🔥 Average RPS: {self.completed_count/total_time:.1f}")
        print("=" * 50)

def main():
    print("🧠 SMART COUNTER LOAD TESTER")
    print("-" * 40)
    print("📊 Accurate real-time counting")
    print("⚡ Fast and reliable")
    print("-" * 40)

    url = input("🌐 Enter URL: ").strip()
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url

    requests_count = int(input("📊 Number of requests (default 5000): ") or "5000")
    workers = int(input("👥 Workers (default 5): ") or "5")

    print(f"\n🧠 Starting smart counter test...")

    tester = SmartCounterTester(url, requests_count, workers)

    try:
        tester.run_test()
    except KeyboardInterrupt:
        print("\n\n⏹️  TEST STOPPED BY USER (Ctrl+C)")
        print("📊 Final stats:")
        print(f"   ✅ Completed: {tester.completed_count}/{tester.total_requests}")
        print(f"   📈 Success: {tester.success_count}")
        print(f"   ❌ Failed: {tester.error_count}")
        tester.stop_event.set()
        sys.exit(0)

if __name__ == "__main__":
    main()
