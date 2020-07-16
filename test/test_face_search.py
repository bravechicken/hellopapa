 # encoding:utf-8
import requests

# client_id 为官网获取的AK， client_secret 为官网获取的SK
client_id=
screte=
host = f'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=${client_id}&client_secret=${screte}'
response = requests.get(host)
if response:
    print(response.json())



'''
人脸注册
'''
request_url = "https://aip.baidubce.com/rest/2.0/face/v3/faceset/user/add"
params = "{\"image\":\"027d8308a2ec665acb1bdf63e513bcb9\",\"image_type\":\"FACE_TOKEN\",\"group_id\":\"group_repeat\",\"user_id\":\"user1\",\"user_info\":\"abc\",\"quality_control\":\"LOW\",\"liveness_control\":\"NORMAL\"}"
access_token = '[调用鉴权接口获取的token]'
request_url = request_url + "?access_token=" + access_token
headers = {'content-type': 'application/json'}
response = requests.post(request_url, data=params, headers=headers)
if response:
    print (response.json())




'''
人脸搜索:https://ai.baidu.com/ai-doc/FACE/Gk37c1uzc#%E8%AF%B7%E6%B1%82%E8%AF%B4%E6%98%8E
'''

request_url = "https://aip.baidubce.com/rest/2.0/face/v3/search"

params = "{\"image\":\"027d8308a2ec665acb1bdf63e513bcb9\",\"image_type\":\"FACE_TOKEN\",\"group_id_list\":\"group_repeat,group_233\",\"quality_control\":\"LOW\",\"liveness_control\":\"NORMAL\"}"
access_token = '[调用鉴权接口获取的token]'
request_url = request_url + "?access_token=" + access_token
headers = {'content-type': 'application/json'}
response = requests.post(request_url, data=params, headers=headers)
if response:
    print (response.json())