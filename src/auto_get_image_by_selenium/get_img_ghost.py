from selenium import webdriver
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import requests
import csv
import util
import img_process

plt.rcParams.update({'figure.max_open_warning': 0}) #fix the memory error

Chrome_driver_location = 'auto_get_image_by_selenium/2/webdriver/chromedriver78'
destination_url_student = 'https://irs.thsrc.com.tw/IMINT/?student=university'
destination_url_default = 'https://irs.thsrc.com.tw/IMINT/'
train_number = 434 #火車班次號碼

options = webdriver.ChromeOptions()
options.add_argument('--no -sandbox')
options.add_argument('--disable -setuid-sandbox')
options.add_argument('headless')

driver = webdriver.Chrome(chrome_options=options)
driver.implicitly_wait(2) # 隐性等待，最长等30秒
driver.get(destination_url_default)  # 輸入範例網址，交給瀏覽器
cookie = driver.get_cookies() #get cookie
pageSource = driver.page_source  # 取得網頁原始碼

#driver.find_element_by_id("bookingMethod2").click()
#driver.find_element_by_name("toTrainIDInputField").send_keys(train_number)
driver.find_element_by_id('btn-confirm').click()

啟程站 = Select(driver.find_element_by_name('selectStartStation'))
啟程站.select_by_value("1")
終點站 = Select(driver.find_element_by_name('selectDestinationStation'))
終點站.select_by_value("3")
driver.find_element_by_name('toTimeInputField').clear()
日期 = driver.find_element_by_name('toTimeInputField').send_keys('2018/02/02')
時間 = Select(driver.find_element_by_name('toTimeTable'))
時間.select_by_value("630A")

session = requests.Session()
for c in cookie:
    session.cookies.set(c['name'], c['value'])
#-----------------------------------------------------
with open('label/label.csv', mode='w', encoding='utf-8') as write_file:
    writer = csv.writer(write_file)
    
    count = 0
    times = 0
    while( count <= 11000):
    
        soup = BeautifulSoup(driver.page_source, 'lxml')
        img = soup.find('img')
        img_url = 'https://irs.thsrc.com.tw'+img.get('src') #find img url
        print(img_url)
        get_img = session.get(img_url)

        dir = './temp/t.jpg'
        with open(dir, 'wb') as file:
            file.write(get_img.content)
            file.flush()
        img_process.process(dir) #process
        passcode = util.predict(dir) #predict
        #print(passcode)
        #------------------------------------------------------
        driver.find_element_by_name("homeCaptcha:securityCode").clear()
        driver.find_element_by_name("homeCaptcha:securityCode").send_keys(passcode)
        #time.sleep(1)
        driver.find_element_by_id('SubmitButton').click() #submit
            #try:
            #driver.find_element_by_name('TrainQueryDataViewPanel:TrainGroup')
        found = soup.find('TrainQueryDataViewPanel:TrainGroup')
        if(found != 'None'):
            print(count)
            with open('./img/'+str(count)+'.jpg', 'wb') as file:
                file.write(get_img.content)
                file.flush()
            
            writer.writerow([passcode])
            driver.back()
            #WebDriverWait(driver, 10, 0.5).until(EC.presence_of_element_located((By.ID, 'BookingS1Form_homeCaptcha_reCodeLink')))
            try:
                driver.find_element_by_id('BookingS1Form_homeCaptcha_reCodeLink').click()
            except:
                driver.find_element_by_id('BookingS1Form_homeCaptcha_reCodeLink').click()
            count += 1
        else:
            print('error')
            driver.find_element_by_id('BookingS1Form_homeCaptcha_reCodeLink').click()
        
        times += 1

    print(times)

'''
    except:
        print('erer')
'''

