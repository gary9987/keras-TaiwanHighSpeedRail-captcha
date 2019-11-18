from selenium import webdriver
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import time
import urllib.request
import requests
import threading
import csv
import demo
import img_process
import time
plt.rcParams.update({'figure.max_open_warning': 0}) #fix the memory error

Chrome_driver_location = '/Users/garys/Desktop/cnn project /2018 01 20/selenium method/chromedriver'
destination_url_student = 'https://irs.thsrc.com.tw/IMINT/?student=university'
destination_url_default = 'https://irs.thsrc.com.tw/IMINT/'
train_number = 434 #火車班次號碼



driver = webdriver.Chrome(Chrome_driver_location)
driver.get(destination_url_default)  # 輸入範例網址，交給瀏覽器
cookie = driver.get_cookies() #get cookie
pageSource = driver.page_source  # 取得網頁原始碼

#driver.find_element_by_id("bookingMethod2").click()
#driver.find_element_by_name("toTrainIDInputField").send_keys(train_number)
啟程站 = Select(driver.find_element_by_name('selectStartStation'))
啟程站.select_by_value("1")
終點站 = Select(driver.find_element_by_name('selectDestinationStation'))
終點站.select_by_value("3")
driver.find_element_by_id('toTimeInputField').clear
日期 = driver.find_element_by_id('toTimeInputField').send_keys('2018/01/21')
時間 = Select(driver.find_element_by_name('toTimeTable'))
時間.select_by_value("1201A")

session = requests.Session()
for c in cookie:
    session.cookies.set(c['name'], c['value'])
#-----------------------------------------------------
with open('/Users/garys/Desktop/get c img/2/lebal/lebal2.csv', mode='w', encoding='utf-8') as write_file:
    writer = csv.writer(write_file)
    
    count = 2271
    times = 0
    while( count <= 5000):
    
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        img = soup.find('img')
        img_url = 'https://irs.thsrc.com.tw'+img.get('src') #find img url
        #print(img_url)
        get_img = session.get(img_url)

        dir = '/Users/garys/Desktop/get c img/2/temp/t.jpg'
        with open(dir, 'wb') as file:
            file.write(get_img.content)
            file.flush()
        img_process.process(dir) #process
        passcode = demo.predict(dir) #predict
        #print(passcode)
        #------------------------------------------------------
        driver.find_element_by_name("homeCaptcha:securityCode").clear()
        driver.find_element_by_name("homeCaptcha:securityCode").send_keys(passcode)
        #time.sleep(1)
        driver.find_element_by_id('SubmitButton').click() #submit
        try:
            driver.find_element_by_name('TrainQueryDataViewPanel:TrainGroup')
            with open('/Users/garys/Desktop/get c img/2/img/'+str(count)+'.jpg', 'wb') as file:
                file.write(get_img.content)
                file.flush()
            
            writer.writerow([passcode])
            driver.back()
            driver.find_element_by_id('BookingS1Form_homeCaptcha_reCodeLink').click()
            count += 1
        except:
            driver.find_element_by_id('BookingS1Form_homeCaptcha_reCodeLink').click()
        
        times += 1

    print(times)

'''
    except:
        print('erer')
'''

