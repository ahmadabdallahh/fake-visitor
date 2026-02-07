"""
Ultra Fast Load Testing - with anti-IP-block options (proxies, stealth, throttling)
"""

import requests
import time
import random
import os
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import sys

def load_proxies(proxies_file="proxies.txt"):
    proxies = []
    env_proxies = os.environ.get("PROXIES", "").strip()
    if env_proxies:
        for line in env_proxies.replace(",", "\n").split():
            line = line.strip()
            if line and (line.startswith("http") or ":" in line):
                if not line.startswith("http"):
                    line = "http://" + line
                proxies.append(line)
    if not proxies and os.path.exists(proxies_file):
        with open(proxies_file, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                line = line.strip().split("#")[0]
                if line and (line.startswith("http") or ":" in line):
                    if not line.startswith("http"):
                        line = "http://" + line
                    proxies.append(line)
    return proxies


class UltraFastTester:
    def __init__(self, url, total_requests=10000, concurrent_users=50,
                proxies=None, stealth=False, max_rps=None, delay_min=0, delay_max=0):
        self.url = url
        self.total_requests = total_requests
        self.concurrent_users = concurrent_users
        self.proxies = proxies or []
        self.stealth = stealth
        self.max_rps = max_rps  # cap requests per second to avoid blocks
        self.delay_min = delay_min
        self.delay_max = delay_max
        self.success_count = 0
        self.error_count = 0
        self.block_count = 0  # 429 / 403 from rate limit
        self.start_time = None
        self.lock = threading.Lock()
        self._rps_window = []
        self._rps_lock = threading.Lock()

        # More user agents to look less bot-like
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15',
        ]
        self.referers = [
            'https://www.google.com/',
            'https://www.bing.com/',
            'https://duckduckgo.com/',
            '',
        ]

    def _get_proxy(self):
        if not self.proxies:
            return None
        return {"http": random.choice(self.proxies), "https": random.choice(self.proxies)}

    def _throttle_rps(self):
        if not self.max_rps or self.max_rps <= 0:
            return
        now = time.time()
        with self._rps_lock:
            self._rps_window = [t for t in self._rps_window if now - t < 1.0]
            while len(self._rps_window) >= self.max_rps:
                time.sleep(0.05)
                now = time.time()
                self._rps_window = [t for t in self._rps_window if now - t < 1.0]
            self._rps_window.append(now)

    def single_request(self, request_id):
        """Execute a single request with optional proxy and anti-block behavior"""
        try:
            if self.max_rps:
                self._throttle_rps()
            if self.stealth and (self.delay_min or self.delay_max):
                delay = random.uniform(self.delay_min, self.delay_max)
                time.sleep(delay)

            ua = random.choice(self.user_agents)
            headers = {
                'User-Agent': ua,
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.9,ar;q=0.8',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
            }
            if self.stealth and self.referers:
                ref = random.choice(self.referers)
                if ref:
                    headers['Referer'] = ref

            session = requests.Session()
            session.headers.update(headers)
            session.cookies.set('user_id', str(random.randint(1, 1000)))
            session.cookies.set('session', f'sess_{random.randint(10000, 99999)}')

            proxy = self._get_proxy()
            response = session.get(self.url, timeout=10, proxies=proxy)

            with self.lock:
                if response.status_code == 200:
                    self.success_count += 1
                elif response.status_code in (429, 403):
                    self.block_count += 1
                    self.error_count += 1
                    if response.status_code == 429 and self.stealth:
                        retry_after = response.headers.get("Retry-After")
                        if retry_after and retry_after.isdigit():
                            time.sleep(min(int(retry_after), 5))
                else:
                    self.error_count += 1

            if request_id % 50 == 0:
                elapsed = time.time() - self.start_time
                rps = request_id / elapsed if elapsed > 0 else 0
                blk = f" | Blocked: {self.block_count}" if self.block_count else ""
                print(f"🚀 {request_id}/{self.total_requests} - {rps:.1f} RPS - OK: {self.success_count}{blk}")

        except requests.exceptions.ProxyError:
            with self.lock:
                self.error_count += 1
        except Exception:
            with self.lock:
                self.error_count += 1

    def run_test(self):
        """Run test"""
        mode = "STEALTH (anti-block)" if self.stealth else "ULTRA FAST"
        print(f"🚀 {mode} - {self.total_requests} requests")
        print(f"📍 URL: {self.url}")
        print(f"⚡ Concurrent users: {self.concurrent_users}")
        if self.proxies:
            print(f"🌐 Proxies: {len(self.proxies)} (IP rotation enabled)")
        if self.max_rps:
            print(f"⏱️  Max RPS cap: {self.max_rps}")
        if self.stealth and (self.delay_min or self.delay_max):
            print(f"🐢 Random delay: {self.delay_min}-{self.delay_max}s")
        if not self.stealth and not self.proxies:
            print(f"🔥 NO DELAYS - MAXIMUM SPEED (risk of IP block)")
        print("=" * 60)

        self.start_time = time.time()
        interrupted = False
        futures = []

        try:
            with ThreadPoolExecutor(max_workers=self.concurrent_users) as executor:
                futures = [executor.submit(self.single_request, i) for i in range(1, self.total_requests + 1)]
                for future in as_completed(futures):
                    try:
                        future.result()
                    except KeyboardInterrupt:
                        print("\n\n⏹️  Stopping... (Ctrl+C) cancelling pending requests...")
                        for f in futures:
                            f.cancel()
                        interrupted = True
                        raise
                    except Exception:
                        pass
        except KeyboardInterrupt:
            interrupted = True
            if not futures:
                print("\n\n⏹️  Stopped by user (Ctrl+C)")

        end_time = time.time()
        total_time = end_time - self.start_time
        completed = self.success_count + self.error_count

        # Final results
        print("=" * 60)
        print("🏁 TEST STOPPED BY USER (Ctrl+C)" if interrupted else "🏁 TEST COMPLETED!")
        print("=" * 60)
        print(f"⏱️  Total time: {total_time:.2f} seconds")
        if interrupted:
            print(f"📋 Completed before stop: {completed} / {self.total_requests}")
        print(f"✅ Successful: {self.success_count}")
        print(f"❌ Failed: {self.error_count}")
        if self.block_count:
            print(f"🚫 Blocked (429/403): {self.block_count}")
        if completed > 0:
            print(f"📊 Success rate: {(self.success_count/completed*100):.1f}%")
            print(f"🔥 Average RPS: {completed/total_time:.1f}")
        print(f"⚡ Concurrent threads: {self.concurrent_users}")
        if self.proxies:
            print(f"🌐 Proxies used: {len(self.proxies)}")
        print("=" * 60)

def main():
    print("⚡ LOAD TESTER (with anti-IP-block options)")
    print("-" * 50)

    url = input("🌐 Enter URL: ").strip()
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url

    requests_count = int(input("📊 Number of requests (default 10000): ") or "10000")
    concurrent = int(input("⚡ Concurrent users (default 50): ") or "50")

    # Anti-block options
    proxies = load_proxies()
    if proxies:
        print(f"✅ Loaded {len(proxies)} proxies from proxies.txt or PROXIES env")
    use_stealth = input("🛡️  Stealth mode? (y/N, slower, less likely to block): ").strip().lower() == 'y'
    max_rps = None
    delay_min = delay_max = 0
    if use_stealth:
        rps_in = input("   Max RPS per second (e.g. 20, empty=no limit): ").strip()
        if rps_in.isdigit():
            max_rps = int(rps_in)
        delay_in = input("   Random delay between requests in sec (e.g. 0.1 0.5): ").strip().split()
        if len(delay_in) >= 2:
            try:
                delay_min, delay_max = float(delay_in[0]), float(delay_in[1])
            except ValueError:
                pass
        elif len(delay_in) == 1 and delay_in[0]:
            try:
                delay_min = delay_max = float(delay_in[0])
            except ValueError:
                pass
    if not use_stealth and not proxies:
        print("⚠️  No proxies & no stealth: high chance of IP block!")

    print(f"\n🚀 Starting test...")

    tester = UltraFastTester(
        url, requests_count, concurrent,
        proxies=proxies if proxies else None,
        stealth=use_stealth,
        max_rps=max_rps,
        delay_min=delay_min,
        delay_max=delay_max,
    )

    try:
        tester.run_test()
    except KeyboardInterrupt:
        print("\n\n⏹️  TEST STOPPED BY USER (Ctrl+C)")
        sys.exit(0)

if __name__ == "__main__":
    main()
