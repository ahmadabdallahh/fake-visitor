#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple Selenium Test - أسهل طريقة للزيارات الواقعية
"""

import time
import random

def install_chrome_driver():
    """تثبيت ChromeDriver تلقائيًا"""
    try:
        from webdriver_manager.chrome import ChromeDriverManager
        from selenium import webdriver
        from selenium.webdriver.chrome.service import Service
        from selenium.webdriver.chrome.options import Options

        print("🔧 Setting up ChromeDriver automatically...")

        # Download and install ChromeDriver
        service = Service(ChromeDriverManager().install())

        # Chrome options
        options = Options()
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        # Test the driver
        driver = webdriver.Chrome(service=service, options=options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        print("✅ ChromeDriver setup successful!")
        driver.quit()
        return True

    except Exception as e:
        print(f"❌ ChromeDriver setup failed: {e}")
        print("\n🔧 Manual setup required:")
        print("1. Install Chrome browser")
        print("2. Download ChromeDriver: https://chromedriver.chromium.org/")
        print("3. Add ChromeDriver to PATH")
        return False

def quick_test(url, num_visits=5):
    """اختبار سريع للزيارات"""
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.service import Service
        from selenium.webdriver.chrome.options import Options
        from webdriver_manager.chrome import ChromeDriverManager

        print(f"🚀 Starting {num_visits} realistic visits to {url}")
        print("=" * 50)

        success_count = 0

        for i in range(num_visits):
            try:
                # Setup driver
                service = Service(ChromeDriverManager().install())
                options = Options()
                options.add_argument("--disable-blink-features=AutomationControlled")
                options.add_experimental_option("excludeSwitches", ["enable-automation"])
                options.add_experimental_option('useAutomationExtension', False)
                options.add_argument("--no-sandbox")
                options.add_argument("--disable-dev-shm-usage")

                driver = webdriver.Chrome(service=service, options=options)
                driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

                # Visit website
                print(f"👤 Visitor {i+1} visiting...")
                driver.get(url)

                # Wait for page load
                time.sleep(random.uniform(3, 6))

                # Scroll down
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
                time.sleep(random.uniform(2, 4))

                # Scroll back up
                driver.execute_script("window.scrollTo(0, 0);")
                time.sleep(random.uniform(1, 3))

                # Stay on page
                time.sleep(random.uniform(5, 10))

                driver.quit()
                success_count += 1
                print(f"✅ Visitor {i+1} completed successfully")

                # Wait between visitors
                if i < num_visits - 1:
                    wait_time = random.uniform(8, 15)
                    print(f"⏱️  Waiting {wait_time:.1f} seconds...")
                    time.sleep(wait_time)

            except Exception as e:
                print(f"❌ Visitor {i+1} failed: {e}")
                try:
                    driver.quit()
                except:
                    pass

        print("=" * 50)
        print(f"📊 Results: {success_count}/{num_visits} successful visits")
        print(f"📈 Success rate: {success_count/num_visits*100:.1f}%")

    except ImportError as e:
        print(f"❌ Missing dependencies: {e}")
        print("💡 Run: pip install selenium webdriver-manager")

def main():
    print("🌐 Simple Selenium Visitor Test")
    print("-" * 40)

    # First, test ChromeDriver setup
    if not install_chrome_driver():
        return

    url = input("\n🌐 Enter your website URL: ").strip()
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url

    num_visits = int(input("👥 Number of visits (default 5): ") or "5")

    print(f"\n🎯 Starting realistic visit test...")
    quick_test(url, num_visits)

if __name__ == "__main__":
    main()
