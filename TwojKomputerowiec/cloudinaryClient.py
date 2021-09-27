#pip install cloudinary
#https://cloudinary.com/documentation/image_upload_api_reference

import os
import sys

if 'proxy' in sys.argv:
    os.environ["CLOUDINARY_URL"] = "cloudinary://311767175853995:M_ApqE5rBoqTHpY94c9exAVmn0M@do08cz1nj?api_proxy=http://proxy.server:3128"
    print('default proxy enabled')
else:
    os.environ["CLOUDINARY_URL"] = "cloudinary://311767175853995:M_ApqE5rBoqTHpY94c9exAVmn0M@do08cz1nj"

import cloudinary

if 'proxy' in sys.argv:
    cloudinary.config(cloud_name="do08cz1nj", api_key="311767175853995", api_secret="M_ApqE5rBoqTHpY94c9exAVmn0M", api_proxy="http://proxy.server:3128")
else:
    cloudinary.config(cloud_name="do08cz1nj", api_key="311767175853995", api_secret="M_ApqE5rBoqTHpY94c9exAVmn0M", api_proxy="http://proxy.server:3128")

#import cloudinary.uploader
#result = cloudinary.uploader.upload("./cloudinaryClient.py", folder="twojkomputerowiec", resource_type="raw",
#                                    context="alt=my description|caption=my title")
#print(result.get("url"))

try:
    result = cloudinary.Search().expression('folder:twojkomputerowiec AND resource_type:image').with_field('context').execute()
except:
    result = None
if result:
    for resource in result['resources']:
        print(resource.get("url"))

print("====================================")

try:
    result = cloudinary.Search().expression('folder:twojkomputerowiec AND resource_type:video').with_field('context').execute()
except:
    result = None
if result:
    for resource in result['resources']:
        print(resource.get("url"))

print("====================================")

try:
    result = cloudinary.Search().expression('folder:twojkomputerowiec AND resource_type:raw').with_field('context').execute()
except:
    result = None
if result:
    for resource in result['resources']:
        print(resource.get("url"))