# -*- coding:utf-8 -*-
import base64
from json import JSONDecoder
import simplejson
from pip._vendor import requests

key = "JoStgK_wz9hknKaT8NWZmNUUsVACMYg9"
secret = "YlHCRxNR4pmuQ5o3ZF0nO-VfTSX7qgev"

def find_face(imgpath):
    print("finding")
    http_url = 'https://api-cn.faceplusplus.com/facepp/v3/detect'
    data = {"api_key": key, "api_secret": secret, "image_url": imgpath, "return_landmark": 1}
    files = {"image_file": open(imgpath, "rb")}
    response = requests.post(http_url, data=data, files=files)
    req_con = response.content.decode('utf-8')
    req_dict = JSONDecoder().decode(req_con)

    this_json = simplejson.dumps(req_dict)
    this_json2 = simplejson.loads(this_json)

    faces = this_json2['faces']
    list0 = faces[0]
    rectangle = list0['face_rectangle']
    # print(rectangle)
    return rectangle

# 模板图片地址 合成图片地址 生成图片地址 合成指数0-100
def add_face(image_url_1,image_url_2,image_url,number):

    ff1 = find_face(image_url_1)
    ff2 = find_face(image_url_2)

    rectangle1 = str(str(ff1['top']) + "," + str(ff1['left']) + "," + str(ff1['width']) + "," + str(ff1['height']))
    rectangle2 = str(ff2['top']) + "," + str(ff2['left']) + "," + str(ff2['width']) + "," + str(ff2['height'])

    # print(rectangle1)
    # print(rectangle2)

    url_add = "https://api-cn.faceplusplus.com/imagepp/v1/mergeface"

    f1 = open(image_url_1, 'rb')
    f1_64 = base64.b64encode(f1.read())
    f1.close()
    f2 = open(image_url_2, 'rb')
    f2_64 = base64.b64encode(f2.read())
    f2.close()

    data = {"api_key": key, "api_secret": secret, "template_base64": f1_64, "template_rectangle": rectangle1,
            "merge_base64": f2_64, "merge_rectangle": rectangle2, "merge_rate": number}

    response = requests.post(url_add, data=data)
    req_con = response.content.decode('utf-8')
    req_dict = JSONDecoder().decode(req_con)
    print(req_dict)
    result = req_dict['result']
    imgdata = base64.b64decode(result)
    file = open(image_url, 'wb')
    file.write(imgdata)
    file.close()

def add_many(list_face):

    print("正在合成第1-2张")
    image_now = r'C:\Users\zfb\Desktop\tu\now.jpg'
    add_face(list_face[0], list_face[1], image_now, 50)

    for index in range(2,len(list_face)):
        print("正在合成第"+str(index+1)+"张")
        add_face(image_now, list_face[index], image_now, 50)


# 单独两张照片的合成示例

# image_url_1 = r"C:\Users\1.jpg"
# image_url_2 = r"C:\Users\2.jpg"
# image_url = r'C:\Users\zfb\Desktop\result.jpg'
# add_face(image_url_1,image_url_2,image_url,50)


# 多张照片合成的示例

list = []
list.append(r"C:\Users\1.jpg")
list.append(r"C:\Users\2.jpg")
list.append(r"C:\Users\3.jpg")
list.append(r"C:\Users\4.jpg")
add_many(list)