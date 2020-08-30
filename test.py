import requests
url = "http://www.flinkhub.com/"
timeout = 5
try:
	request = requests.get(url, timeout=timeout)
	print("Connected to the Internet")
except Exception as inst:
    print(inst,inst.__class__)
    if inst==ConnectionError:
    	print("No internet connection.")