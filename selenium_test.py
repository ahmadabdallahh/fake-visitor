#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Selenium Test Script - للزيارات الواقعية مع JavaScript
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import random
import json

class SeleniumVisitor:
    def __init__(self, url, num_visitors=10):
        self.url = url
        self.num_visitors = num_visitors
        self.fake_users = self.generate_users()

    def generate_users(self):
        """Generate fake user profiles"""
        users = []
        names = ['John Doe', 'Jane Smith', 'Mike Johnson', 'Sarah Williams', 'David Brown']
        devices = ['Desktop', 'Mobile', 'Tablet']

        for i in range(10):
            users.append({
                'name': random.choice(names),
                'device': random.choice(devices),
                'screen_size': random.choice(['1920,1080', '1366,768', '375,667', '768,1024'])
            })
        return users

    def setup_driver(self, user):
        """Setup Chrome driver with realistic settings"""
        options = Options()

        # Mobile vs Desktop
        if user['device'] == 'Mobile':
            mobile_emulation = {
                "deviceMetrics": {"width": 375, "height": 667, "pixelRatio": 2.0},
                "userAgent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Mobile/15E148 Safari/604.1"
            }
            options.add_experimental_option("mobileEmulation", mobile_emulation)
        elif user['device'] == 'Tablet':
            mobile_emulation = {
                "deviceMetrics": {"width": 768, "height": 1024, "pixelRatio": 2.0},
                "userAgent": "Mozilla/5.0 (iPad; CPU OS 16_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Mobile/15E148 Safari/604.1"
            }
            options.add_experimental_option("mobileEmulation", mobile_emulation)

        # Anti-detection settings
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument("--disable-extensions")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")

        # Random viewport
        width, height = map(int, user['screen_size'].split(','))
        options.add_argument(f"--window-size={width},{height}")

        try:
            # Use webdriver-manager to automatically download and manage ChromeDriver
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=options)
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            return driver
        except Exception as e:
            print(f"❌ Error setting up driver: {e}")
            print("💡 Make sure Chrome browser is installed")
            print("💡 Try: pip install --upgrade webdriver-manager")
            return None

    def simulate_visit(self, user):
        """Simulate a realistic website visit"""
        driver = self.setup_driver(user)
        if not driver:
            return False

        try:
            print(f"👤 {user['name']} ({user['device']}) visiting...")

            # Visit the website
            driver.get(self.url)
            time.sleep(random.uniform(2, 5))  # Wait for page load

            # Scroll down (simulate reading)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
            time.sleep(random.uniform(1, 3))

            # Scroll back up
            driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(random.uniform(1, 2))

            # Click on something if available
            try:
                # Look for common clickable elements
                selectors = ['a', 'button', '[onclick]', '.btn', '.link']
                for selector in selectors:
                    elements = driver.find_elements(By.CSS_SELECTOR, selector)
                    if elements:
                        random.choice(elements).click()
                        time.sleep(random.uniform(1, 2))
                        break
            except:
                pass

            # Stay on page for realistic time
            time.sleep(random.uniform(3, 8))

            print(f"✅ {user['name']} completed visit")
            return True

        except Exception as e:
            print(f"❌ {user['name']} failed: {e}")
            return False
        finally:
            driver.quit()

    def run_test(self):
        """Run the visitor simulation"""
        print(f"🚀 Starting {self.num_visitors} realistic visits to {self.url}")
        print("=" * 60)

        success_count = 0
        for i in range(self.num_visitors):
            user = random.choice(self.fake_users)

            if self.simulate_visit(user):
                success_count += 1

            # Random delay between visitors
            delay = random.uniform(5, 15)
            print(f"⏱️  Waiting {delay:.1f} seconds before next visitor...")
            time.sleep(delay)

        print("=" * 60)
        print(f"📊 Results: {success_count}/{self.num_visitors} successful visits")
        print(f"📈 Success rate: {success_count/self.num_visitors*100:.1f}%")

def main():
    print("🌐 Selenium Realistic Visitor Simulator")
    print("-" * 40)

    url = input("🌐 Enter your website URL: ").strip()
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url

    num_visitors = int(input("👥 Number of visitors (default 10): ") or "10")

    print("\n⚠️  Requirements:")
    print("- Install Chrome browser")
    print("- Install selenium: pip install selenium")
    print("- Download ChromeDriver matching your Chrome version")
    print("-" * 40)

    simulator = SeleniumVisitor(url, num_visitors)
    simulator.run_test()

if __name__ == "__main__":
    main()
