#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Load Testing Script - اختبار تحمّل المواقع
مصمم لاختبار 5000 طلب على موقعك الخاص
"""

import requests
import time
import random
from datetime import datetime
import threading
from concurrent.futures import ThreadPoolExecutor
import sys
import urllib.parse
import json

class LoadTester:
    def __init__(self, url, total_requests=5000, concurrent_users=10, delay_range=(0.1, 0.5), use_proxy=False):
        self.url = url
        self.total_requests = total_requests
        self.concurrent_users = concurrent_users
        self.delay_range = delay_range
        self.use_proxy = use_proxy
        self.success_count = 0
        self.error_count = 0
        self.response_times = []
        self.lock = threading.Lock()

        # Fake user profiles for realistic simulation
        self.fake_users = self.generate_fake_users()

        # Proxy list (you can replace with paid proxies for better results)
        self.proxies = [
            {'http': 'http://20.205.61.143:80', 'https': 'http://20.205.61.143:80'},
            {'http': 'http://52.167.144.100:80', 'https': 'http://52.167.144.100:80'},
            {'http': 'http://52.167.144.101:80', 'https': 'http://52.167.144.101:80'},
            {'http': 'http://52.167.144.102:80', 'https': 'http://52.167.144.102:80'},
            {'http': 'http://52.167.144.103:80', 'https': 'http://52.167.144.103:80'},
            {'http': 'http://52.167.144.104:80', 'https': 'http://52.167.144.104:80'},
            {'http': 'http://52.167.144.105:80', 'https': 'http://52.167.144.105:80'},
            {'http': 'http://52.167.144.106:80', 'https': 'http://52.167.144.106:80'},
            {'http': 'http://52.167.144.107:80', 'https': 'http://52.167.144.107:80'},
            {'http': 'http://52.167.144.108:80', 'https': 'http://52.167.144.108:80'},
        ]

        # قائمة User-Aagents متنوعة
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/121.0',
            'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/121.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
        ]

    def generate_fake_users(self):
        """Generate realistic fake user profiles"""
        first_names = ['John', 'Jane', 'Michael', 'Sarah', 'David', 'Emily', 'Robert', 'Lisa', 'James', 'Mary',
                      'William', 'Jennifer', 'Richard', 'Linda', 'Joseph', 'Patricia', 'Thomas', 'Barbara', 'Charles', 'Susan']
        last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez',
                     'Hernandez', 'Lopez', 'Gonzalez', 'Wilson', 'Anderson', 'Thomas', 'Taylor', 'Moore', 'Jackson', 'Martin']

        domains = ['gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com', 'icloud.com', 'aol.com', 'mail.com']
        countries = ['US', 'UK', 'CA', 'AU', 'DE', 'FR', 'ES', 'IT', 'NL', 'SE']
        cities = ['New York', 'London', 'Toronto', 'Sydney', 'Berlin', 'Paris', 'Madrid', 'Rome', 'Amsterdam', 'Stockholm']

        devices = ['Desktop', 'Mobile', 'Tablet']
        browsers = ['Chrome', 'Firefox', 'Safari', 'Edge']

        fake_users = []
        for i in range(100):  # Generate 100 unique fake users
            first_name = random.choice(first_names)
            last_name = random.choice(last_names)

            user = {
                'id': i + 1,
                'name': f"{first_name} {last_name}",
                'email': f"{first_name.lower()}.{last_name.lower()}{random.randint(1, 999)}@{random.choice(domains)}",
                'username': f"{first_name.lower()}{random.randint(100, 999)}",
                'age': random.randint(18, 65),
                'gender': random.choice(['Male', 'Female', 'Other']),
                'country': random.choice(countries),
                'city': random.choice(cities),
                'device': random.choice(devices),
                'browser': random.choice(browsers),
                'ip': f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}",
                'session_id': f"sess_{random.randint(100000, 999999)}_{int(time.time())}",
                'referrer': random.choice(['https://www.google.com', 'https://www.facebook.com', 'https://twitter.com', 'https://www.linkedin.com', 'direct']),
                'user_agent': '',  # Will be set based on device/browser
                'screen_resolution': random.choice(['1920x1080', '1366x768', '1440x900', '1280x720', '2560x1440']),
                'timezone': random.choice(['UTC-5', 'UTC-6', 'UTC-8', 'UTC+0', 'UTC+1', 'UTC+2']),
                'language': random.choice(['en-US', 'en-GB', 'en-CA', 'en-AU', 'es-ES', 'fr-FR', 'de-DE', 'it-IT']),
            }

            # Set appropriate User-Agent based on device and browser
            user['user_agent'] = self.get_user_agent_for_device(user['device'], user['browser'])

            fake_users.append(user)

        return fake_users

    def get_user_agent_for_device(self, device, browser):
        """Get realistic User-Agent string for device and browser"""
        if device == 'Mobile':
            if browser == 'Chrome':
                return f"Mozilla/5.0 (Linux; Android {random.randint(10, 13)}; SM-G99{random.randint(0, 9)}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{random.randint(110, 120)}.0.0.0 Mobile Safari/537.36"
            elif browser == 'Safari':
                return f"Mozilla/5.0 (iPhone; CPU iPhone OS {random.randint(15, 17)}_{random.randint(0, 2)} like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/{random.randint(15, 17)}.{random.randint(0, 3)} Mobile/15E148 Safari/604.1"
        elif device == 'Tablet':
            if browser == 'Chrome':
                return f"Mozilla/5.0 (Linux; Android {random.randint(10, 13)}; SM-T{random.randint(5, 9)}{random.randint(0, 9)}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{random.randint(110, 120)}.0.0.0 Safari/537.36"
            elif browser == 'Safari':
                return f"Mozilla/5.0 (iPad; CPU OS {random.randint(15, 17)}_{random.randint(0, 2)} like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/{random.randint(15, 17)}.{random.randint(0, 3)} Mobile/15E148 Safari/604.1"
        else:  # Desktop
            if browser == 'Chrome':
                return f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{random.randint(110, 120)}.0.0.0 Safari/537.36"
            elif browser == 'Firefox':
                return f"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:{random.randint(110, 120)}.0) Gecko/20100101 Firefox/{random.randint(110, 120)}.0"
            elif browser == 'Safari':
                return f"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_{random.randint(13, 15)}_{random.randint(0, 9)}) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/{random.randint(15, 17)}.{random.randint(0, 3)} Safari/605.1.15"
            elif browser == 'Edge':
                return f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{random.randint(110, 120)}.0.0.0 Safari/537.36 Edg/{random.randint(110, 120)}.0.0"

        # Fallback
        return f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

    def single_request(self, request_id):
        """Execute a single request with fake user profile"""
        try:
            start_time = time.time()

            # اختيار بروكسي عشوائي لو مفعل
            proxy = None
            if self.use_proxy and self.proxies:
                proxy = random.choice(self.proxies)

            # اختيار مستخدم وهمي عشوائي
            fake_user = random.choice(self.fake_users)

            # Build realistic headers based on fake user profile
            headers = {
                'User-Agent': fake_user['user_agent'],
                'Accept': random.choice([
                    'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
                ]),
                'Accept-Language': fake_user['language'],
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': random.choice(['keep-alive', 'close']),
                'Upgrade-Insecure-Requests': '1',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'none',
                'Cache-Control': random.choice(['no-cache', 'max-age=0']),
                'Referer': fake_user['referrer'],
                'X-Forwarded-For': fake_user['ip'],
                'X-Real-IP': fake_user['ip'],
                'X-Client-IP': fake_user['ip'],
                'CF-Connecting-IP': fake_user['ip'],
            }

            # Add device-specific headers
            if fake_user['device'] == 'Mobile':
                headers['Sec-CH-UA-Mobile'] = '?1'
                headers['Sec-CH-UA-Platform'] = '"Android"'
            elif fake_user['device'] == 'Tablet':
                headers['Sec-CH-UA-Mobile'] = '?1'
                headers['Sec-CH-UA-Platform'] = '"Android"'
            else:  # Desktop
                headers['Sec-CH-UA-Mobile'] = '?0'
                headers['Sec-CH-UA-Platform'] = '"Windows"'

            # إضافة بعض الـ Headers الإضافية للتشبيه
            if random.random() > 0.7:  # 30% فرصة إضافة headers إضافية
                headers['DNT'] = str(random.choice([1, 0]))
                headers['Sec-GPC'] = str(random.choice([1, 0]))

            session = requests.Session()
            session.headers.update(headers)

            # Add cookies to simulate returning user
            session.cookies.set('session_id', fake_user['session_id'])
            session.cookies.set('user_id', str(fake_user['id']))
            session.cookies.set('username', fake_user['username'])
            session.cookies.set('device', fake_user['device'])
            session.cookies.set('last_visit', str(int(time.time() - random.randint(3600, 86400))))

            response = session.get(self.url, proxies=proxy, timeout=15)
            end_time = time.time()

            response_time = (end_time - start_time) * 1000  # بالمللي ثانية

            with self.lock:
                self.response_times.append(response_time)
                if response.status_code == 200:
                    self.success_count += 1
                else:
                    self.error_count += 1

            proxy_info = f" (Proxy: {proxy['http'][:20]}...)" if proxy else ""
            user_info = f" (User: {fake_user['name']}, {fake_user['device']}, {fake_user['country']})"
            print(f"Request #{request_id}: {response.status_code} - {response_time:.2f}ms{proxy_info}{user_info}")

            # تأخير عشوائي بين الطلبات (أطول شوية عشان تتجنب الـ Block)
            if self.delay_range:
                delay = random.uniform(*self.delay_range)
                time.sleep(delay)

        except Exception as e:
            with self.lock:
                self.error_count += 1
            print(f"Request #{request_id}: Error - {str(e)}")

    def run_test(self):
        """Run the complete test"""
        print("Starting load testing...")
        print(f"URL: {self.url}")
        print(f"Number of requests: {self.total_requests}")
        print(f"Number of concurrent users: {self.concurrent_users}")
        print(f"Using proxy: {'Enabled' if self.use_proxy else 'Disabled'}")
        print(f"Number of available proxies: {len(self.proxies) if self.use_proxy else 0}")
        print(f"Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("-" * 60)

        start_time = time.time()

        # تشغيل الطلبات بشكل متوازي
        with ThreadPoolExecutor(max_workers=self.concurrent_users) as executor:
            futures = []
            for i in range(1, self.total_requests + 1):
                future = executor.submit(self.single_request, i)
                futures.append(future)

            # انتظار انتهاء كل الطلبات
            for future in futures:
                future.result()

        end_time = time.time()
        total_time = end_time - start_time

        # عرض النتائج النهائية
        self.display_results(total_time)

    def display_results(self, total_time):
        """Display test results"""
        print("\n" + "=" * 60)
        print("Final Test Results")
        print("=" * 60)
        print(f"Total time: {total_time:.2f} seconds")
        print(f"Successful requests: {self.success_count}")
        print(f"Failed requests: {self.error_count}")
        print(f"Success rate: {(self.success_count/self.total_requests*100):.2f}%")

        if self.response_times:
            avg_time = sum(self.response_times) / len(self.response_times)
            min_time = min(self.response_times)
            max_time = max(self.response_times)

            print(f"Average response time: {avg_time:.2f}ms")
            print(f"Slowest response: {max_time:.2f}ms")
            print(f"Fastest response: {min_time:.2f}ms")

            # Calculate requests per second
            rps = self.total_requests / total_time
            print(f"Requests per second: {rps:.2f} RPS")

        print("=" * 60)

def main():
    """Main function"""
    print("Advanced Load Testing Tool")
    print("-" * 50)

    # Get URL from user
    url = input("Enter the URL to test (example: http://localhost:3000): ").strip()

    if not url:
        print("URL is required!")
        return

    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url

    # Advanced options
    try:
        requests_count = int(input("Number of requests (default 5000): ") or "5000")
        concurrent = int(input("Concurrent users (default 20): ") or "20")

        # Proxy option
        use_proxy_choice = input("Use proxy to avoid blocks? (y/n, default n): ").lower()
        use_proxy = use_proxy_choice == 'y'

        delay_choice = input("Delay between requests? (y/n, default n): ").lower()
        delay_range = (0.1, 0.5) if delay_choice == 'y' else (0.01, 0.1)  # Fast mode by default

    except ValueError:
        print("Invalid values! Using defaults.")
        requests_count = 5000
        concurrent = 20  # More concurrent users for speed
        use_proxy = False  # Default to no proxy
        delay_range = (0.01, 0.1)  # Fast mode

    # Run test
    tester = LoadTester(
        url=url,
        total_requests=requests_count,
        concurrent_users=concurrent,
        delay_range=delay_range,
        use_proxy=use_proxy
    )

    print("\nImportant notes:")
    print("- Free proxies are often unreliable and slow")
    print("- Default is NO proxy for better reliability")
    print("- Use proxy only if you get blocked")
    print("- Longer delays help avoid blocks")
    print("-" * 50)

    try:
        tester.run_test()
    except KeyboardInterrupt:
        print("\n\n⏹️  TEST STOPPED BY USER (Ctrl+C)")
        print("📊 Load test cancelled!")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Error occurred: {str(e)}")

if __name__ == "__main__":
    main()
