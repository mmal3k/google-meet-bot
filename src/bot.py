from playwright.sync_api import sync_playwright
import os
from dotenv import load_dotenv
import random
import time
from pathlib import Path 

load_dotenv()

class GoogleMeetBot:
    def __init__(self):
        self.email = os.getenv('GOOGLE_EMAIL')
        self.password = os.getenv('GOOGLE_PASSWORD')
        self.meet_link = os.getenv('GOOGLE_MEET')
        

    def human_type(self, element, text):
        for char in text:
            element.type(char)
            time.sleep(random.uniform(0.1, 0.3))

    def login_to_google(self, page):
        def go_to_gmail(page):
            page.goto('https://accounts.google.com/signin')
            page.wait_for_load_state('networkidle')
            page.wait_for_timeout(2000)
            
        def enter_email(page):
            email_input = page.wait_for_selector('input[type="email"]')
            email_input.click()
            self.human_type(email_input, self.email)
            
        def press_next_after_email(page):
            next_button = page.locator('button:has-text("Next")')
            if next_button.is_visible():
                next_button.click()
            else:
                next_button = page.locator('#identifierNext')
                next_button.click()
            
        def enter_password(page):
            password_input = page.wait_for_selector('input[type="password"]')
            password_input.click()
            self.human_type(password_input, self.password)
        
        def press_next_after_password(page):
            password_next = page.locator('#passwordNext')
            password_next.click()
        
        try:
            go_to_gmail(page)
            enter_email(page)
            press_next_after_email(page)
            enter_password(page)
            press_next_after_password(page)

        except Exception as e:
            print(f"Login error: {e}")
            print(f"Current URL: {page.url}")
            raise

    def join_meet(self, page):
        def go_to_specific_meet(page):
            if "meet.google.com/" in self.meet_link:
                full_url = self.meet_link
            else:
                full_url = f"https://meet.google.com/{self.meet_link}"
            
            page.set_extra_http_headers({
                'Referer': 'https://meet.google.com/',
                'Origin': 'https://meet.google.com'
            })
            
            page.goto(full_url)
            page.wait_for_load_state('networkidle')
            page.wait_for_timeout(2000)
            
        def disable_camera(page):
            try:
                    # Method 1: Look for specific camera button
                    camera_button = page.locator('button[aria-label="Turn off camera (ctrl + e)"]')
                    if camera_button.is_visible():
                        print("Found camera button (Method 1)")
                        camera_button.click()
                        page.wait_for_timeout(1000)
                    
                    # Method 2: Alternative camera button
                    if not camera_button.is_visible():
                        camera_button = page.locator('button[data-is-muted="false"]:has([aria-label*="camera"])')
                        if camera_button.is_visible():
                            print("Found camera button (Method 2)")
                            camera_button.click()
                            page.wait_for_timeout(1000)
                    
                    # Method 3: Try by role
                    if not camera_button.is_visible():
                        camera_button = page.get_by_role("button", name="Turn off camera")
                        if camera_button.is_visible():
                            print("Found camera button (Method 3)")
                            camera_button.click()
                            page.wait_for_timeout(1000)
                    
                    print("Camera should be disabled now")
                    
            except Exception as e:
                print(f"Error with camera: {e}")
        
        def ask_to_join(page):
            join_button = page.locator('span[jsname="V67aGc"][class="UywwFc-vQzf8d"]')
            if join_button.is_visible():
                print("Found join button, clicking...")
                join_button.click()

                play_audio_and_exit(page)
        
        def play_audio_and_exit(page):
            try:
                print("Starting audio playback...")
                
                time.sleep(5)
                
                audio_path = Path("audio/hello.mp3")
                
                if os.name == 'nt':  # Windows
                    os.system(f'start {audio_path}')
                else:  # Mac/Linux
                    os.system(f'afplay {audio_path}')  # This plays the audio through BlackHole
                
                print("Audio finished, leaving meeting...")
                page.close()
        
            except Exception as e:
                print(f"Error in audio playback: {e}")
                page.close()  
        
        try:
            go_to_specific_meet(page)
            try:
                print("Configuring devices...")
                disable_camera(page)
            except Exception as e:
                print(f"Error configuring devices: {e}")
            ask_to_join(page)
        except Exception as e:
            print(f"Error in join_meet: {e}")
            raise

    def run(self):
        print("Starting Google Meet Bot...")
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=False,
                args=[
                    '--disable-blink-features=AutomationControlled',
                    '--no-sandbox',
                    '--disable-web-security',
                    '--disable-features=IsolateOrigins,site-per-process'
                ]
            )
            
            context = browser.new_context(
                viewport={'width': 1280, 'height': 720},
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
                accept_downloads=True,
                ignore_https_errors=True,
                locale='en-US',
                timezone_id='Europe/London',
                permissions=['camera', 'microphone']
            )
            
            try:
                page = context.new_page()
                self.login_to_google(page)
                
                try:
                    page.wait_for_selector('div[role="navigation"]', timeout=30000)
                    print("Login successful!")
                    
                    self.join_meet(page)
                    
                except Exception as e:
                    print(f"Error after login: {e}")
                    page.wait_for_timeout(15000)
                
            except Exception as e:
                print(f"An error occurred: {e}")
            finally:
                browser.close()


if __name__ == "__main__":
    bot = GoogleMeetBot()
    bot.run()