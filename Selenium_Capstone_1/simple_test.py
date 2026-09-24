from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Setup Chrome options
chrome_options = Options()
chrome_options.add_argument("--start-maximized")

# Initialize the Chrome driver
driver = webdriver.Chrome(options=chrome_options)

try:
    # Navigate to TutorialsNinja
    driver.get("https://tutorialsninja.com/demo/")
    print("Page title:", driver.title)

    # Take a screenshot
    driver.save_screenshot("screenshots/simple_test.png")
    print("Screenshot saved")

finally:
    # Close the browser
    driver.quit()