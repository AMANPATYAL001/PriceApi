import requests
import re
from typing import Union
from fastapi import FastAPI
# from bs4 import BeautifulSoup

app = FastAPI()

# URL = "https://www.lowes.com/pd/Anker-Anker-PowerCore-Essential-20000-Portable-Charger-Power-Bank/1003251768"



@app.get("/")
def read_root(q: Union[str, None] = None):
    # price=23.091
    URL=q
    headers={"User-Agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"}
    r = requests.get(URL,headers=headers)

    x = re.search("retailPrice\":\d+\.\d*,", r.text)
    # print(x.group())
    # print(x)
    y = re.search("\d+\.\d*", x.group())

    return {"price": y.group()}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

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