import requests

bird_bytes = requests.get(
    "https://upload.wikimedia.org/wikipedia/commons/thumb/4/45/Eopsaltria_australis_-_Mogo_Campground.jpg/640px-Eopsaltria_australis_-_Mogo_Campground.jpg"
).content

print("Sending Request...")
resp = requests.post("http://127.0.0.1:8000/", data=bird_bytes)
cls = resp.json()
print("Class number: " + str(cls))
classes = ('plane', 'car', 'bird', 'cat', 'deer',
           'dog', 'frog', 'horse', 'ship', 'truck')
print("Class name: %s" % classes[cls['class_index']])

