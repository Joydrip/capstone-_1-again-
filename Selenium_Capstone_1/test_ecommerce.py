import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoAlertPresentException, TimeoutException
from selenium.webdriver.common.keys import Keys
import openpyxl

def read_test_data():
    workbook = openpyxl.load_workbook("test_data.xlsx")
    sheet = workbook.active
    base_email = sheet["A2"].value
    password = sheet["B2"].value
    product = sheet["C2"].value
    quantity = sheet["D2"].value
    return base_email, password, product, quantity

def test_ecommerce():

    base_email, password, product, quantity = read_test_data()


    timestamp = str(int(time.time()))
    if "@" in base_email:
        local_part, domain = base_email.split("@", 1)
        email = f"{local_part}+{timestamp}@{domain}"
    else:
        email = f"{base_email}+{timestamp}"

    print(f"Using email: {email}")

    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")

    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 10)

    try:
        driver.get("https://tutorialsninja.com/demo/")
        print("Navigated to TutorialsNinja")

        driver.save_screenshot("screenshots/01_launch.png")

 
        my_account_link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "My Account")))
        my_account_link.click()

        login_link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Login")))
        login_link.click()

        email_input = wait.until(EC.visibility_of_element_located((By.ID, "input-email")))
        email_input.clear()
        email_input.send_keys(email)

        password_input = wait.until(EC.visibility_of_element_located((By.ID, "input-password")))
        password_input.clear()
        password_input.send_keys(password)

        login_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='submit']")))
        login_button.click()

        try:
            wait.until(EC.visibility_of_element_located((By.LINK_TEXT, "Logout")))
            print("Login successful")
            driver.save_screenshot("screenshots/02_login.png")
        except TimeoutException:
            try:
                error_message = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.alert-danger")))
                print(f"Login failed: {error_message.text}")
            except TimeoutException:
                print("Login failed: Unknown error")

            print("Attempting to register a new account...")
            driver.save_screenshot("screenshots/login_failed.png")

            register_link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Register")))
            register_link.click()

        
            firstname_input = wait.until(EC.visibility_of_element_located((By.ID, "input-firstname")))
            firstname_input.clear()
            firstname_input.send_keys("Test")

            lastname_input = wait.until(EC.visibility_of_element_located((By.ID, "input-lastname")))
            lastname_input.clear()
            lastname_input.send_keys("User")

            email_input_reg = wait.until(EC.visibility_of_element_located((By.ID, "input-email")))
            email_input_reg.clear()
            email_input_reg.send_keys(email)

            telephone_input = wait.until(EC.visibility_of_element_located((By.ID, "input-telephone")))
            telephone_input.clear()
            telephone_input.send_keys("1234567890")

            password_input_reg = wait.until(EC.visibility_of_element_located((By.ID, "input-password")))
            password_input_reg.clear()
            password_input_reg.send_keys(password)

            password_confirm_input = wait.until(EC.visibility_of_element_located((By.ID, "input-confirm")))
            password_confirm_input.clear()
            password_confirm_input.send_keys(password)

            subscribe_yes = wait.until(EC.element_to_be_clickable((By.NAME, "newsletter")))
            subscribe_label = wait.until(EC.element_to_be_clickable((By.XPATH, "//label[normalize-space()='Yes']")))
            subscribe_label.click()

            agree_checkbox = wait.until(EC.element_to_be_clickable((By.NAME, "agree")))
            agree_checkbox.click()

            continue_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='submit']")))
            continue_button.click()

   
            try:
                wait.until(EC.text_to_be_present_in_element((By.TAG_NAME, "h1"), "Your Account Has Been Created!"))
                print("Registration successful")
            except TimeoutException:
                try:
                    wait.until(EC.text_to_be_present_in_element((By.TAG_NAME, "h1"), "Account Successfully Created"))
                    print("Registration successful (alternate check)")
                except TimeoutException:
                    print("Assuming registration completed (no error visible)")
                    time.sleep(3)

            driver.save_screenshot("screenshots/registration_success.png")

            try:
                wait.until(EC.visibility_of_element_located((By.LINK_TEXT, "Logout")))
                print("Logged in after registration")
                driver.save_screenshot("screenshots/02_login.png")
            except TimeoutException:
                print("Not automatically logged in, proceeding to login...")
                my_account_link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "My Account")))
                my_account_link.click()
                login_link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Login")))
                login_link.click()

                email_input = wait.until(EC.visibility_of_element_located((By.ID, "input-email")))
                email_input.clear()
                email_input.send_keys(email)

                password_input = wait.until(EC.visibility_of_element_located((By.ID, "input-password")))
                password_input.clear()
                password_input.send_keys(password)

                login_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='submit']")))
                login_button.click()

                wait.until(EC.visibility_of_element_located((By.LINK_TEXT, "Logout")))
                print("Login successful after registration")
                driver.save_screenshot("screenshots/02_login.png")

        search_box = wait.until(EC.visibility_of_element_located((By.NAME, "search")))
        search_box.clear()
        search_box.send_keys(product)
        search_box.send_keys(Keys.RETURN)
        
        wait.until(EC.text_to_be_present_in_element((By.TAG_NAME, "body"), product))
        print(f"Search results for '{product}' found")
        driver.save_screenshot("screenshots/03_search.png")

        product_link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, product)))
        product_link.click()

        wait.until(EC.title_contains(product))
        print(f"Opened product page for '{product}'")
        driver.save_screenshot("screenshots/04_product.png")

        add_to_cart_button = wait.until(EC.element_to_be_clickable((By.ID, "button-cart")))
        add_to_cart_button.click()

        wait.until(EC.visibility_of_element_located((By.ID, "cart")))
        print("Product added to cart")
        driver.save_screenshot("screenshots/05_added_to_cart.png")

        try:
            alert = driver.switch_to.alert
            alert_text = alert.text
            print(f"Alert present: {alert_text}")
            alert.accept()
        except NoAlertPresentException:
            print("No alert present")

        cart_link = wait.until(EC.element_to_be_clickable((By.ID, "cart")))
        cart_link.click()

        view_cart_link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "View Cart")))
        view_cart_link.click()

        wait.until(EC.title_contains("Shopping Cart"))
        print("Opened shopping cart")
        driver.save_screenshot("screenshots/06_cart.png")

  
        product_in_cart = wait.until(EC.text_to_be_present_in_element((By.TAG_NAME, "body"), product))
        assert product_in_cart, f"Product '{product}' not found in cart"
        print(f"Verified product '{product}' is in cart")


        quantity_input = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[name^='quantity']")))
        quantity_input.clear()
        quantity_input.send_keys(str(quantity))

        update_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn.btn-primary")))
        update_button.click()

        wait.until(EC.text_to_be_present_in_element_value((By.CSS_SELECTOR, "input[name^='quantity']"), str(quantity)))
        print(f"Updated quantity to {quantity}")
        driver.save_screenshot("screenshots/07_quantity_updated.png")

        quantity_input = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[name^='quantity']")))
        actual_quantity = quantity_input.get_attribute("value")
        assert actual_quantity == str(quantity), f"Expected quantity {quantity}, but got {actual_quantity}"
        print(f"Verified quantity is {actual_quantity}")

        assert product in driver.page_source, f"Product '{product}' not found in cart after update"
        print("Cart verification passed")

        driver.save_screenshot("screenshots/08_final_cart.png")
        print("Test completed successfully")

    except Exception as e:
        print(f"Test failed: {str(e)}")
        driver.save_screenshot("screenshots/failure.png")
        raise
    finally:
        driver.quit()

if __name__ == "__main__":
    test_ecommerce()