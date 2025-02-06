from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from app.models import FormData
from selenium.webdriver.chrome.options import Options

def fill_form(data: FormData):
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)

    try:
        driver.get("https://sos.oregon.gov/")
        
        # Нажатие на кнопку "Register a Business"
        register_business_button = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Register a Business")))
        register_business_button.click()

        # Переключение на новое окно
        wait.until(EC.number_of_windows_to_be(2))
        windows = driver.window_handles
        driver.switch_to.window(windows[1])

        # Авторизация
        log_in_button = wait.until(EC.element_to_be_clickable((By.ID, "loginButton")))
        log_in_button.click()

        login = wait.until(EC.presence_of_element_located((By.ID, "username")))
        login.send_keys(credentials.login)
        password = wait.until(EC.presence_of_element_located((By.ID, "password")))
        password.send_keys(credentials.password)
        login_button = driver.find_element(By.NAME, "Login")
        login_button.click()

        time.sleep(5)

        # Закрытие возможных всплывающих окон
        try:
            cancel_button = wait.until(EC.element_to_be_clickable((By.ID, "cancelButton"))) 
            cancel_button.click()
        except:
            pass

        # Клик по кнопке Start
        register_business_start_button = wait.until(EC.element_to_be_clickable((By.ID, "startBusinessButtonID")))
        register_business_start_button.click()

        wait.until(EC.number_of_windows_to_be(2))
        register_name_button = driver.find_element(By.ID, "startBusRegBtn")
        register_name_button.click()
        wait.until(EC.number_of_windows_to_be(2))

        # Выбор типа бизнеса
        business_type = driver.find_element(By.ID, "filingType")
        business_type.click()
        dllc_option = driver.find_element(By.XPATH, "//option[@value='DLLC']")
        dllc_option.click()
        wait.until(EC.number_of_windows_to_be(2))

        # Заполнение данных компании
        business_name_textarea = driver.find_element(By.ID, "busOverview_businessName")
        business_name_textarea.send_keys(data['business_name'])
        activity_description_textarea = driver.find_element(By.ID, "busOverview_activityDescription")
        activity_description_textarea.send_keys(data['activity_description'])
        perpetual_radio = driver.find_element(By.ID, "busOverview_duration_type_perpetual")
        perpetual_radio.click()

        email_input = driver.find_element(By.ID, "busOverview_emailAddress_emailAddress")
        email_input.send_keys(data['email'])
        reenter_email_input = driver.find_element(By.ID, "busOverview_emailAddress_emailAddressVerification")
        reenter_email_input.send_keys(data['email'])

        # Заполнение адреса для уведомлений
        country_select = driver.find_element(By.ID, "busOverview_principalAddr_country")
        Select(country_select).select_by_value('USA')
        address_input = driver.find_element(By.ID, "busOverview_principalAddr_addressLine1")
        address_input.send_keys(data['address'])
        zip_input = driver.find_element(By.ID, "busOverview_principalAddr_zip")
        zip_input.send_keys(data['zip'])
        city_input = driver.find_element(By.ID, "busOverview_principalAddr_city")
        city_input.send_keys(data['city'])
        state_select = driver.find_element(By.ID, "busOverview_principalAddr_state")
        Select(state_select).select_by_value('OR')

        time.sleep(10)
        continue_button = driver.find_element(By.ID, "pageButton3")
        continue_button.click()

        # Заполнение контактных данных
        name_input = driver.find_element(By.ID, "busOverview_businessContact_name")
        name_input.send_keys(data['contact_name'])
        phone_input = driver.find_element(By.ID, "busOverview_businessContact_phone_number")
        phone_input.send_keys(data['phone'])
        continue_button = driver.find_element(By.XPATH, "//span[contains(text(),'Continue')]")
        continue_button.click()

        time.sleep(10)
        # Заполнение данных уведомлений (Email)
        notification_select = Select(wait.until(EC.presence_of_element_located((By.ID, "eSelection"))))
        notification_select.select_by_value("EMAIL")
        contact_name_input = wait.until(EC.presence_of_element_located((By.ID, "contactDetail")))
        contact_name_input.send_keys(data['contact_name'])
        contact_email_input = wait.until(EC.presence_of_element_located((By.ID, "contactEmail")))
        contact_email_input.send_keys(data['email'])
        reenter_email_input = wait.until(EC.presence_of_element_located((By.ID, "validateEmail")))
        reenter_email_input.send_keys(data['email'])

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        continue_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'Continue')]")))
        continue_button.click()

        # Заполнение данных для зарегистрированного агента
        individual_radio = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "registeredAgent_indvAssocNameEntityType"))
        )
        individual_radio.click()
        first_name_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "registeredAgent_individual_firstName"))
        )
        first_name_input.send_keys(data['agent_first_name'])
        last_name_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "registeredAgent_individual_lastName"))
        )
        last_name_input.send_keys(data['agent_last_name'])

        # Завершающие шаги
        submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Submit')]"))
        )
        submit_button.click()
        
        time.sleep(10)
        
        # Возврат успешного результата
        return {
            "registration_completed": True,
            "message": "Registration successful"
        }

    finally:
        driver.quit()