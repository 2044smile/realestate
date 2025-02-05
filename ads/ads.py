from selenium import webdriver


driver_path = "Chrome Driver Path"

service = webdriver.ChromeService(executable_path=driver_path)
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(service=service, options=options)

driver.get("https://www.naver.com")