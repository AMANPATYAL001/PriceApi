import requests
import os
import re
from typing import Union
from fastapi import FastAPI
import time
from selenium import webdriver  
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.chrome.options import Options


app = FastAPI()

opts = Options()
opts.add_argument("--headless")
opts.add_argument("--no-sandbox")
opts.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36")
opts.add_argument("--disable-blink-features=AutomationControlled")
opts.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
opts.add_experimental_option('useAutomationExtension', False)


headers={"User-Agent" : "Mozilla/5.0 \(X11; Linux x86_64\) AppleWebKit/537.36 \(KHTML, like Gecko\) Chrome/107.0.0.0 Safari/537.36",'Accept': '*/*','Accept-Encoding': 'gzip','Referer':'https://www.lowes.com/'}

@app.get("/url/")
def read_root(q: Union[str, None] = None):
# def read_root(q:str):
#    try:
#       URL=q
#        r = requests.get(URL,headers=headers)

#        x = re.search("retailPrice\":\d+\.\d*,", r.text)
#        y = re.search("\d+\.\d*", x.group())
    
#    except:
#        return {'error':'aman '+r.status_code}
    try:
        start_time=time.time()
        driver = webdriver.Chrome(executable_path=str(os.environ.get('CHROMEDRIVER_PATH')),chrome_options=opts)

        driver.maximize_window()
        driver.get("https://www.lowes.com/pd/Valspar-2000-Satin-High-Hide-White-Interior-Paint-Actual-Net-Contents-128-fl-oz/1000380217")
        driver.implicitly_wait(10)

        pinCode=2512

        time.sleep(10)
        driver.find_elements(By.XPATH,"//*[@data-linkid='selected-store']")[0].click()

        time.sleep(5)
        a=driver.find_elements(By.XPATH,"//div[@id='storeListContainer']//button")
        a[1].click()

        time.sleep(2)

        store=driver.find_element(By.ID,'store-search-handler').get_attribute('innerText')
        print(store)
        price=driver.find_element(By.CLASS_NAME,'main-price').get_attribute('innerText')
        print(price)
        driver.close()

        return {"price": price,"timeTaken":time.time()-start_time,'store':store}
    
    except Exception as e:
        return {'eee':str(e)}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    try:
        URL = "https://www.lowes.com/pd/Anke-Anker-PowerCore-Essential-20000-Portable-Charger-Power-Bank/1003251768"
        r = requests.get(URL,headers=headers)

        x = re.search("retailPrice\":\d+\.\d*,", r.text)
        y = re.search("\d+\.\d*", x.group())
    except:
        return {'status':r.status_code}
    return {"item_id": item_id, "q": q,'y':y.group(),'status':r.status_code}
# @app.get("/it/")
# async def read_items(q: Union[str, None] = None):
#     results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
#     if q:
#         results.update({"q": q})
#     return results

#     while  true
# do
#       ffprobe -hide_banner -loglevel quiet  /var/www/bigbluebutton-default/recording/$1.mp4 ; 
#       retVal=$?
#       if [ $retVal -eq  1 ];
#       then
#            sleep 5
#       else
#           #curl -X POST https://8d7c-122-160-143-16.ngrok.io/home/callback?mergeVideoUrl=https://byokuldev.centralindia.cloudapp.azure.com/recording/$1.mp4
#           curl -X POST https://3a92-122-160-143-16.ngrok.io/bigBlueButton/mergeVideo?meetingID=$1
#           break
#       fi  
#   done

# bbb-mp4.sh
