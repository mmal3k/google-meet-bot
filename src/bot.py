from playwright.sync_api import sync_playwright
import os
from dotenv import load_dotenv
import random
import time
import string
from pathlib import Path

load_dotenv()

class GoogleMeetBot:
    def __init__(self):
        self.meet_link = os.getenv('GOOGLE_MEET')
        self.names = ["Alex Johnson", "Sam Lee", "Jordan Smith"]

    def human_type(self, element, text):
        for char in text:
            if random.random() < 0.05:
                element.type(random.choice(string.ascii_letters))
                time.sleep(0.2)
                element.type('\b')
            element.type(char)
            time.sleep(random.uniform(0.08, 0.4))

    def handle_camera(self, page):
        try:
            camera_button = page.locator('button[aria-label="Turn off camera (ctrl + e)"]')
            
            if not camera_button.is_visible():
                camera_button = page.get_by_role("button", name="Turn off camera")
                if camera_button.is_visible():
                    print("Found camera button (Method 3)")
                    camera_button.click()
                    page.wait_for_timeout(1000)
            
                    
        except Exception as e:
            print(f"Error with camera: {e}")

        # Fallback to text-based detection
        for lang in ['en', 'fr']:
            try:
                camera_button = page.locator(f'button:has-text("{self.locales[lang][2]}")')
                if camera_button.is_visible():
                    camera_button.click()
                    time.sleep(random.uniform(0.5, 1.2))
                    break
            except:
                continue

    def join_meet(self, page):
        try:
            meet_url = f"{self.meet_link}?hl=en"  # Always force English
            page.goto(meet_url)
            page.wait_for_load_state('networkidle', timeout=15000)
            
            time.sleep(random.uniform(1, 3))
            self.handle_camera(page)
            
            name_input = page.locator('input[type="text"]')
            name_input.click()
            self.human_type(name_input, random.choice(self.names))
            
            time.sleep(random.uniform(0.5, 1.5))
            
            # Simplified English-only selector
            join_button = page.locator('button:has-text("Ask to join"), button:has-text("Join now")')
            if join_button.is_visible():
                join_button.click()
                time.sleep(random.uniform(2, 4))
                self.play_audio()

        except Exception as e:
            print(f"Error: {e}")


    def play_audio(self):
        audio_path = Path("audio/hello.mp3")
        try:
            if os.name == 'nt':
                os.system(f'start {audio_path}')
            else:
                os.system(f'afplay {audio_path}')
        except Exception as e:
            print(f"Audio error: {e}")

    def run(self):
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=False,
                args=[
                    '--disable-blink-features=AutomationControlled',
                    '--use-fake-ui-for-media-stream',
                    '--no-sandbox',
                    '--lang=en-US'  # Force English language
                ]
            )
            
            context = browser.new_context(
                viewport={'width': 1280 + random.randint(-100, 100), 
                         'height': 720 + random.randint(-50, 50)},
                locale='en-US',  # Set browser locale
                permissions=['camera', 'microphone']
            )
            
            try:
                page = context.new_page()
                self.join_meet(page)

            finally:
                browser.close()

if __name__ == "__main__":
    bot = GoogleMeetBot()
    bot.run()