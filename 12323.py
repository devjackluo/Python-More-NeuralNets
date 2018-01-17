import datetime
a = datetime.datetime.now()
for x in range(0,5000):
    print(x)
b = datetime.datetime.now()
delta = b - a


if int(delta.total_seconds() * 1000) > 1950:
    print(int(delta.total_seconds() * 1000))
    print("yup")

