import datetime
import requests

products = [
    "G18-ABI-CONUS-BAND07", # GOES-16 West
    "G16-ABI-FD-BAND07", # GOES-18 East
]
width = 128
height = 128
long = 34.1
lat = -118.4
zoom = 7
baseurl = "http://realearth.ssec.wisc.edu/api/image"

# UTC
time_start = datetime.datetime(2025, 1, 12, 19, 46, 0, 0)
time_end = datetime.datetime(2025, 1, 13, 21, 6, 0, 0)
time_step = datetime.timedelta(minutes=5)

time = time_start
while time < time_end:
    time += time_step
    time_string = time.isoformat().replace("T","+")

    for product in products:
        url = f"{baseurl}?products={product},&width={width}&height={height}&client=RealEarth&basemap=-&labels=-&center={long},{lat}&zoom={zoom}&time={time_string}"
        path = f"raw/{product}/{time}.png"

        with open(path, 'wb') as handle:
            response = requests.get(url, stream=True)

            if not response.ok:
                print(response)

            for block in response.iter_content(1024):
                if not block:
                    break

                handle.write(block)

    print(time_string)
