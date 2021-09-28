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
        "tags": ["test file from script"],
        "is_private_file": False,
        "use_unique_file_name": True,
        "response_fields": ["is_private_file", "tags"],
    }
)
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
        print("=======================")
else:
    print('eror', results['error'])