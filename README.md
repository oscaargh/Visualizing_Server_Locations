# Visualizing Server Locations from Chrome History

This is my first Matplotlib project, inspired by [this tutorial from Practical Python](https://practicalpython.yasoob.me/chapter9).

This project visualizes the approximate geographic locations of the servers from my Google Chrome browsing history. It takes a CSV file exported from the "Export Chrome History" extension, extracts the domains, finds their IP addresses, uses the `ipinfo.io` API to get geolocation data (latitude/longitude), and then plots these locations on an animated world map using Matplotlib and Basemap.

## Final Result

The script generates an `anim.mp4` file.

---

## How it Works (Pipeline)

The project is split into two main parts:

1.  **Data Processing (`csv_to_txt.py`)**
    * Uses `pandas` to read a `history.csv` file exported from [this Chrome extension](https://chromewebstore.google.com/detail/export-chrome-history/dihloblpkeiddiaojbagoecedbfpifdj).
    * Extracts the 6th column (which contains the URLs).
    * Saves all URLs to `History.txt`.
    * Cleans `History.txt` by removing any empty or meaningless lines (like `""`).

2.  **Visualization (`main.py`)**
    * Reads the cleaned `History.txt`.
    * Uses `urlparse` to extract unique domain names (e.g., `google.com`).
    * Uses `socket.gethostbyname` to look up the IP address for each domain.
    * Uses the `ipinfo.io` API to fetch geolocation data (latitude and longitude) for each unique IP. This is done with multithreading (`ThreadPoolExecutor`) to speed up the process.
    * All raw data from the API is saved to `complete_details.txt`.
    * Finally, `Matplotlib` and `Basemap` are used to plot each location on a world map.
    * The animation is saved as `anim.mp4` using `ffmpeg`.

---

## Setup and Installation

Follow these steps to run the project on your own machine.

### 1. Prerequisites

* Python 3.x
* The **[Export Chrome History](https://chromewebstore.google.com/detail/export-chrome-history/dihloblpkeiddiaojbagoecedbfpifdj)** extension for Google Chrome.
* **FFmpeg:** Required by Matplotlib to save the animation.
    * *On Windows (recommended):* `choco install ffmpeg`
    * *On Mac:* `brew install ffmpeg`

### 2. Clone the Repo

```bash
git clone [https://github.com/oscaargh/Visualizing_Server_Locations.git](https://github.com/oscaargh/Visualizing_Server_Locations.git)
cd Visualizing_Server_Locations
