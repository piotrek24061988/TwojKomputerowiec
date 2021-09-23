#pip install cloudinary
#https://cloudinary.com/console/c-e21d3a7e1a1abbcf182a3ecdfa0ca3
#https://cloudinary.com/documentation/image_upload_api_reference

import cloudinary, cloudinary.uploader

cloudinary.config(cloud_name="do08cz1nj", api_key="311767175853995", api_secret="M_ApqE5rBoqTHpY94c9exAVmn0M")

#result = cloudinary.uploader.upload("TwojKomputerowiec/static/media/ikony/pgwhite900blackfull.png", folder="twojkomputerowiec", resource_type="image")
#print(result.get("url"))

result = cloudinary.Search().expression('folder:twojkomputerowiec AND resource_type:image').execute()
#print(result)
#print("---------------------------------")
for resource in result['resources']:
    print(resource.get("url"))

print("====================================")


result = cloudinary.Search().expression('folder:twojkomputerowiec AND resource_type:video').execute()
#print(result)
#print("---------------------------------")
for resource in result['resources']:
    print(resource.get("url"))

print("====================================")


result = cloudinary.Search().expression('folder:twojkomputerowiec AND resource_type:raw').execute()
#print(result)
#print("---------------------------------")
for resource in result['resources']:
    print(resource.get("url"))