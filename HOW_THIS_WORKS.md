# How This Selenium Test Works - Simple Explanation

## What is This For?
This is a simple program that automatically tests a shopping website (TutorialsNinja Demo) by:
1. Opening a web browser
2. Logging in (or creating an account if needed)
3. Searching for a product
4. Adding it to the shopping cart
5. Changing the quantity
6. Checking that everything worked correctly
7. Taking screenshots along the way
8. Creating a test report

Think of it like having a robot that does all the clicking and typing for you, then checks if everything worked.

## Files You Need
- `test_ecommerce.py` - The main program (this is what you run)
- `test_data.xlsx` - A simple Excel file with your login info and what to test
- `screenshots/` - Folder where pictures of each step will be saved
- `reports/` - Folder where the test report will be saved

## How to Run It
1. Make sure you have Python installed
2. Install the needed tools by running: `pip install selenium openpyxl pytest pytest-html`
3. Double-click the `test_ecommerce.py` file OR run in command prompt: `python test_ecommerce.py`
4. Watch the browser open and do the test automatically!
5. When done, open `reports/report.html` to see what happened

## What's Inside the Excel File (`test_data.xlsx`)
This file tells the test what to use:
- **A1**: username (your email for login)
- **B1**: password 
- **C1**: product to search for (like "MacBook")
- **D1**: quantity to buy (like 2)

Example:
| A (username)   | B (password)   | C (product)    | D (quantity) |
|----------------|----------------|----------------|--------------|
| test@email.com | mypassword123  | MacBook        | 2            |

## How the Code Works - Step by Step

### 1. Getting Ready
```python
# Read login info and test data from Excel
email, password, product, quantity = read_test_data()
```
- This reads your login details and what product to test from the Excel file
- Think of it like reading instructions from a note

### 2. Setting Up the Browser
```python
# Setup Chrome options
chrome_options = Options()
chrome_options.add_argument("--start-maximized")

# Initialize the Chrome driver
driver = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(driver, 10)
```
- This opens a Chrome browser window and makes it big (maximized)
- Sets up a "waiter" that will patiently wait up to 10 seconds for things to load
- Like telling the robot: "Wait up to 10 seconds for each thing to appear before complaining"

### 3. Going to the Website
```python
driver.get("https://tutorialsninja.com/demo/")
print("Navigated to TutorialsNinja")
driver.save_screenshot("screenshots/01_launch.png")
```
- Opens the TutorialsNinja shopping website (like typing the address in your browser)
- Takes a screenshot so we can see what the starting page looks like

### 4. Logging In
```python
# Click My Account
my_account_link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "My Account")))
my_account_link.click()

# Click Login
login_link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Login")))
login_link.click()

# Type in email and password
email_input = wait.until(EC.visibility_of_element_located((By.ID, "input-email")))
email_input.clear()
email_input.send_keys(email)

password_input = wait.until(EC.visibility_of_element_located((By.ID, "input-password")))
password_input.clear()
password_input.send_keys(password)

# Click the Login button
login_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='submit']")))
login_button.click()

# Check if login worked by looking for "Logout" link
try:
    wait.until(EC.visibility_of_element_located((By.LINK_TEXT, "Logout")))
    print("Login successful")
    driver.save_screenshot("screenshots/02_login.png")
```
- Finds and clicks "My Account" then "Login" links
- Types your email and password into the boxes
- Clicks the Login button
- Checks for a "Logout" link to confirm you're logged in
- Takes a screenshot after login

### 5. Searching for a Product
```python
# Find the search box
search_box = wait.until(EC.visibility_of_element_located((By.NAME, "search")))
search_box.clear()
search_box.send_keys(product)
search_box.send_keys(Keys.RETURN)  # Press Enter key

# Make sure we see the product in results
wait.until(EC.text_to_be_present_in_element((By.TAG_NAME, "body"), product))
print(f"Search results for '{product}' found")
driver.save_screenshot("screenshots/03_search.png")
```
- Finds the search box, clears anything in it, types the product name (like "MacBook")
- Presses Enter to start the search
- Waits to see the product name appear somewhere on the page
- Takes a screenshot of the search results

### 6. Opening the Product Page
```python
# Find and click the product link
product_link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, product)))
product_link.click()

# Make sure we're on the right product page
wait.until(EC.title_contains(product))
print(f"Opened product page for '{product}'")
driver.save_screenshot("screenshots/04_product.png")
```
- Finds the link that has the exact product name (like "MacBook") and clicks it
- Checks that the browser tab title now contains the product name
- Takes a screenshot of the product page

### 7. Adding to Cart
```python
# Find and click "Add to Cart" button
add_to_cart_button = wait.until(EC.element_to_be_clickable((By.ID, "button-cart")))
add_to_cart_button.click()

# Wait for the cart to update (look for the cart icon)
wait.until(EC.visibility_of_element_located((By.ID, "cart")))
print("Product added to cart")
driver.save_screenshot("screenshots/05_added_to_cart.png")
```
- Finds the "Add to Cart" button (usually has ID="button-cart") and clicks it
- Waits for the shopping cart icon to update/show it has items
- Takes a screenshot showing the product was added

### 8. Handling Pop-ups (if any)
```python
try:
    alert = driver.switch_to.alert
    alert_text = alert.text
    print(f"Alert present: {alert_text}")
    alert.accept()  # Click OK on the alert
except NoAlertPresentException:
    print("No alert present")
```
- Checks if a annoying pop-up appeared (like "Are you sure?")
- If yes, reads what it says and clicks OK
- If no pop-up, just continues

### 9. Viewing the Shopping Cart
```python
# Click the cart icon
cart_link = wait.until(EC.element_to_be_clickable((By.ID, "cart")))
cart_link.click()

# Click "View Cart" in the dropdown menu
view_cart_link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "View Cart")))
view_cart_link.click()

# Make sure we're on the cart page
wait.until(EC.title_contains("Shopping Cart"))
print("Opened shopping cart")
driver.save_screenshot("screenshots/06_cart.png")
```
- Clicks the shopping cart icon (usually in top-right)
- Clicks the "View Cart" link that appears
- Checks that the page title now says "Shopping Cart"
- Takes a screenshot of your cart

### 10. Checking the Product is in Cart
```python
# Make sure we see the product name somewhere in the cart page
product_in_cart = wait.until(EC.text_to_be_present_in_element((By.TAG_NAME, "body"), product))
assert product_in_cart, f"Product '{product}' not found in cart"
print(f"Verified product '{product}' is in cart"
```
- Checks that the product name (like "MacBook") appears somewhere on the cart page
- If not found, the test will stop and show an error
- If found, prints success message

### 11. Changing the Quantity
```python
# Find the quantity box (usually looks like: <input name="quantity[...]">)
quantity_input = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[name^='quantity']")))
quantity_input.clear()  # Clear whatever is there
quantity_input.send_keys(str(quantity))  # Type the new quantity (from Excel)

# Find and click the update button
update_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn.btn-primary")))
update_button.click()

# Wait for the quantity to actually change
wait.until(EC.text_to_be_present_in_element_value((By.CSS_SELECTOR, "input[name^='quantity']"), str(quantity)))
print(f"Updated quantity to {quantity}")
driver.save_screenshot("screenshots/07_quantity_updated.png")
```
- Finds the box where you can change how many you want to buy
- Clears the current number and types the new quantity from Excel (like "2")
- Finds and clicks the "Update" button (usually a blue button)
- Waits to see the number in the box actually change to what we typed
- Takes a screenshot after updating

### 12. Double-Checking the Quantity
```python
# Find the quantity box again (to avoid "stale element" errors)
quantity_input = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[name^='quantity']")))
actual_quantity = quantity_input.get_attribute("value")  # Get what's actually in the box

# Check if it matches what we wanted
assert actual_quantity == str(quantity), f"Expected quantity {quantity}, but got {actual_quantity}"
print(f"Verified quantity is {actual_quantity}"
```
- Looks at the quantity box again to get the current number
- Compares it to what we wanted from Excel
- If they match, great! If not, test fails with an error message

### 13. Final Verification
```python
# One last check: make sure the product name is still in the cart page
assert product in driver.page_source, f"Product '{product}' not found in cart after update"
print("Cart verification passed"
```
- Does one final check that the product name is still somewhere on the page
- This catches if something went wrong during the quantity update

### 14. Final Screenshot and Cleanup
```python
# Take one last screenshot of the final cart
driver.save_screenshot("screenshots/08_final_cart.png")
print("Test completed successfully"
```
- Takes a final picture of your cart with the correct product and quantity
- Closes the browser window
- The test is done!

## What If Something Goes Wrong?
The code has "try/except" blocks which are like safety nets:
- If it can't find an element (like a button or box), it saves a screenshot called "failure.png"
- It prints an error message explaining what went wrong
- Then it closes the browser and stops
- This helps you see exactly where it got stuck

## Key Concepts Explained Simply

### What is Selenium?
- Selenium is a tool that can control web browsers automatically
- It's like having a robot arm that can move a mouse and type on a keyboard
- But instead of a physical robot, it's code that tells the browser what to do

### What is a WebDriver?
- This is the part that actually talks to the browser
- `webdriver.Chrome()` means we're controlling Google Chrome
- It's like giving the robot arm instructions specifically for Chrome

### What are Locators?
- These are ways to find things on a web page
- Examples:
  - `By.ID` - Find something by its unique ID (like finding a person by their employee number)
  - `By.NAME` - Find something by its name attribute
  - `By.LINK_TEXT` - Find a link by its exact text
  - `By.CSS_SELECTOR` - Find things using CSS patterns (like finding all red buttons)
  - `By.XPATH` - Find things using their position in the page structure

### What are Explicit Waits?
- Websites don't load instantly - sometimes images or buttons take a second to appear
- Instead of guessing how long to wait (and sometimes waiting too long or not enough),
  we use "explicit waits"
- `WebDriverWait(driver, 10)` means: "Wait up to 10 seconds for this specific thing to appear"
- If it appears in 2 seconds, we continue immediately
- If it takes 12 seconds, we give up and report an error
- This makes tests faster and more reliable than just using `time.sleep(5)` everywhere

### What is an Assertion?
- `assert something == something_else` is how we check if things are correct
- If the assertion is true, the test keeps going
- If it's false, the test stops immediately and reports a failure
- It's like the robot saying: "If this isn't true, something is wrong - stop everything!"

### Why Take Screenshots?
- Screenshots are like taking pictures at each step
- If the test fails, you can look at the screenshots to see exactly what the browser showed
- Very helpful for debugging - you can see if a button was missing, or if you're on the wrong page

## What This Teaches You About Test Automation
1. **Separation of Concerns**: We keep test data (Excel) separate from test logic (Python)
2. **Reusability**: Functions like `read_test_data()` can be used in other tests
3. **Error Handling**: Good tests don't just crash - they tell you what went wrong
4. **Verification**: We don't just perform actions - we check that each action worked
5. **Documentation**: Screenshots and reports make it easy to show others what happened

## Next Steps You Could Try
1. Change the values in `test_data.xlsx` to test different products or quantities
2. Try adding more verification steps (like checking the price in the cart)
3. Try taking a screenshot when you're logged out
4. Experiment with different wait times to see how it affects speed

Remember: The goal of automated testing is to find problems before real users do - so if this test passes, it means the basic shopping flow on this website is working correctly!

---
*Created for Selenium Capstone 1 - September 24, 2026*