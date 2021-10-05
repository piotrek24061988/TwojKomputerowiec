#pip install imagekitio
#https://github.com/imagekit-developer/imagekit-python

from imagekitio import ImageKit

imagekit = ImageKit(
    private_key='private_/VE3e+xlNcOda8x5H0rWdJkadH8=',
    public_key='public_3DO66QF/NddNueQIPN2rVtp3oIE=',
    url_endpoint='https://ik.imagekit.io/bry5gj5urua'
)

#uploading files
"""
imagekit.upload_file(
    file= open("imagekitioClient.py", "rb"),
    file_name= "imagekitioClient.py",
    options= {
        "folder" : "/twojkomputerowiec/",
        "tags": ["skrypt testowy"],
        "is_private_file": False,
        "use_unique_file_name": True,
        "response_fields": ["tags"],
    }
)
"""

"""
#listing files
results = imagekit.list_files({
    "path": "/twojkomputerowiec/",
    "skip": 0,
    "limit": 10,
})

if not results['error']:
    for result in results['response']:
        print(result.get('url'))
        title = result.get('tags')
        if title:
            print(title[-1])
        print("=======================")
else:
    print('error', results['error'])
print("#######################")

#listing images
results = imagekit.list_files({
    "path": "/twojkomputerowiec/",
    "skip": 0,
    "limit": 10,
    "fileType": "image"
})

if not results['error']:
    for result in results['response']:
        print(result)
        print(result.get('url'))
        print("=======================")
else:
    print('error', results['error'])
print("#######################")
"""

#listing videos
#results = imagekit.list_files({'searchQuery': 'createdAt < "7d"'})
results = imagekit.list_files({
    "path": "/twojkomputerowiec/",
    "skip": 0,
    "limit": 10,
    "fileType": "non-image",
    "tags": "video",
})

if not results['error']:
    for result in results['response']:
        #print(result)
        print(result.get('url'))
        print("=======================")
else:
    print('error', results['error'])
print("#######################")