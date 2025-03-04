from playwright.sync_api import sync_playwright
import os
from dotenv import load_dotenv
import random
import time

load_dotenv()

class GoogleMeetBot:
    def __init__(self):
        self.email = os.getenv('GOOGLE_EMAIL')
        self.password = os.getenv('GOOGLE_PASSWORD')
        
        # Add rate limiting
        self.min_delay = 2  # minimum seconds between actions
        
        # Add usage limits
        self.max_daily_uses = 5  # reasonable limit
        
        # Add proper documentation
        self.purpose = "Personal automation for educational meetings"

    def human_type(self, element, text):
        """Type like a human with random delays"""
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

    def join_meet(self, page, meet_link):
        """Join a Google Meet"""
        try:
            # First go to Google Meet home to ensure we're properly authenticated
            print("Going to Google Meet home first...")
            page.goto("https://meet.google.com")
            page.wait_for_load_state('networkidle')
            page.wait_for_timeout(3000)
            
            # Then navigate to the specific meeting
            if "meet.google.com/" in meet_link:
                full_url = meet_link
            else:
                full_url = f"https://meet.google.com/{meet_link}"
            
            print(f"Now navigating to: {full_url}")
            
            # Use page.goto with referer header to look more like a regular browser
            page.set_extra_http_headers({
                'Referer': 'https://meet.google.com/',
                'Origin': 'https://meet.google.com'
            })
            
            page.goto(full_url)
            page.wait_for_load_state('networkidle')
            page.wait_for_timeout(5000)
            
            # Rest of your join code...
            try:
                print("Configuring devices...")
                # Turn off microphone if it's on
                mic_button = page.locator('button[aria-label*="microphone"]')
                if mic_button.is_visible():
                    mic_button.click()
                    print("Microphone turned off")
                    
                # Turn off camera if it's on    
                camera_button = page.locator('button[aria-label*="camera"]')
                if camera_button.is_visible():
                    camera_button.click()
                    print("Camera turned off")
            except Exception as e:
                print(f"Error configuring devices: {e}")
            
            # Look for the join button
            print("Looking for join button...")
            join_button = page.locator('span[jsname="V67aGc"]')
            if join_button.is_visible():
                print("Found join button, clicking...")
                join_button.click()
                print("Join button clicked!")
            
        except Exception as e:
            print(f"Error in join_meet: {e}")
            page.screenshot(path="error.png")
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
                
                # Wait for login completion
                try:
                    page.wait_for_selector('div[role="navigation"]', timeout=30000)
                    print("Login successful!")
                    
                    # After successful login, join the meet
                    meet_link = "https://meet.google.com/jro-xrft-zhp"  # Replace with your meet link
                    self.join_meet(page, meet_link)
                    
                    # Keep the browser open while in meeting
                    input("Press Enter to leave the meeting and close the browser...")
                    
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