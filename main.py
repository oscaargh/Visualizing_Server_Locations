from urllib.parse import urlparse
import socket
import ipinfo
from concurrent.futures import ThreadPoolExecutor, as_completed
import matplotlib
matplotlib.use('Agg')  # CRITICAL: Use non-GUI backend to avoid TkInter errors
import matplotlib.pyplot as plt
from matplotlib import animation
from mpl_toolkits.basemap import Basemap
import json
import csv_to_txt
import os
from dotenv import load_dotenv

"""
This program is my first matplotlib project. Mostly built using the tutorial https://practicalpython.yasoob.me/chapter9.
It uses the google chrome extension https://chromewebstore.google.com/detail/export-chrome-history/dihloblpkeiddiaojbagoecedbfpifdj 
to export a csv file, and then parses all of the urls to a text document. Sockets is then used to get an ip adress from each domain. 
This ip adress is passed through ipinfo.io to get the approximate geo location of our adresses. Then matplotlib and basemap are 
used to make a map/animation plotting the locations of our visited adresses on a world map.
"""

with open("History.txt", "r") as f:
    data = f.readlines()

domain_names = set() # Using a set as to only store unique domain names.

for url in data:
    # Shaves the urls down to domain only ex. www.google.com or facebook.com.
    final_url = urlparse(url).netloc
    final_url = final_url.split(":")[0]
    domain_names.add(final_url)

ip_set = set() # We only want unique ip-adresses

for domain in domain_names:
    # Gets us an initial ip adress.
    try:
        ip_addr = socket.gethostbyname(domain)
        ip_set.add(ip_addr)
    except:
        print(domain)


load_dotenv() # Loads the .env file
access_token = os.getenv("IPINFO_API_KEY") # API KEY for Ipinfo.io in a .env file!
handler = ipinfo.getHandler(access_token)

def get_details(ipadress):
    # Using Ipinfo.io API key to get the real location out of our ip adress
    try:
        details = handler.getDetails(ipadress)
        return details.all
    except:
        return None

complete_details = []

with ThreadPoolExecutor(max_workers=10) as e: # Multithreading to get the ip details faster, stores them as futures.
    for ip_adress in list(ip_set):
        complete_details.append(e.submit(get_details, ip_adress))

lat = []
lon = []
results_list = []

for loc in as_completed(complete_details):
    """
    We get a list of futures in complete_details, and use as_completed to process each future. result() to get
    the contents of each dictionary returned from ipinfo.io. The latitute and longitude are saved in our result
    dict by splitting "loc": "37.7621,-122.3971" and appending these to a seperate list for each ip adress
    for later use when plotting points to our basemap.
    
    """
    result = loc.result()
    if result and "loc" in result:
        lat_str, lon_str = result["loc"].split(",")
        lat.append(float(lat_str))
        lon.append(float(lon_str))
    if result:
        results_list.append(result)
        
with open("complete_details.txt", "w") as f: # Stores all of the details we get from ipinfo in a text file
    json.dump(results_list, f, indent=4)


fig, ax = plt.subplots(figsize=(40,20)) # Size of our plot

map = Basemap()

map.fillcontinents(color="#008000", lake_color="#57B9FF")

map.drawmapboundary(fill_color="#57B9FF") # Background color aka all of the seas

map.drawcountries(linewidth=0.15, color="w")

map.drawstates(linewidth=0.1, color="w")

def init(): # Voluntary textbox in the bottomleft corner of our map/animation
    plt.text( -170, -72,'Server locations of my most visited websites'
        ' (by traffic)\nPlot realized with Python and the Basemap library'
        '\n\n~Oscaargh', ha='left', va='bottom',
        size=28, color='gold')

def update(frame_number): # Plots our points onto the map
    map.plot(lon[frame_number], lat[frame_number], linestyle='none', marker="o",
    markersize=20, alpha=0.5, c="white", markeredgecolor="silver",
    markeredgewidth=1)

ani = animation.FuncAnimation(fig, update, interval=1, # Animates the map and updates it with points each second.
    frames=len(lat), init_func= init)

writer = animation.writers['ffmpeg']
writer = writer(fps=20, metadata=dict(artist='Me'), bitrate=1800)
ani.save('anim.mp4', writer=writer)
# Generates all frames of the animation and passes them to the ffmpeg writer,
# which encodes the frames into an MP4 video using the specified fps and bitrate.