from selenium import webdriver
from selenium.webdriver.support.ui import Select
Chrome_driver_location = '/Users/garys/Desktop/Python/selenium method/chromedriver'
destination_url_student = 'https://irs.thsrc.com.tw/IMINT/?student=university'
destination_url_default = 'https://irs.thsrc.com.tw/IMINT/'
train_number = 434 #火車班次號碼



driver = webdriver.Chrome(Chrome_driver_location)
driver.get(destination_url)  # 輸入範例網址，交給瀏覽器
pageSource = driver.page_source  # 取得網頁原始碼

driver.find_element_by_id("bookingMethod2").click()
driver.find_element_by_name("toTrainIDInputField").send_keys(train_number)
啟程站 = Select(driver.find_element_by_name('selectStartStation'))
啟程站.select_by_value("1")
終點站 = Select(driver.find_element_by_name('selectDestinationStation'))
終點站.select_by_value("8")
#print(pageSource)

#bookingMethod2
#driver.close()  # 關閉瀏覽器

