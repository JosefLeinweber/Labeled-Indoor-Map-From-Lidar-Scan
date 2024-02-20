  [![Automated Tests](https://github.com/JosefLeinweber/scan_processing/actions/workflows/automated-tests.yml/badge.svg?branch=trunk)](https://github.com/JosefLeinweber/scan_processing/actions/workflows/automated-tests.yml) [![Build & Push to GAR and Deploy to Cloud Run](https://github.com/JosefLeinweber/scan_processing/actions/workflows/cd_google_cloud_run.yml/badge.svg?branch=trunk)](https://github.com/JosefLeinweber/scan_processing/actions/workflows/cd_google_cloud_run.yml) [![Check Service Status](https://github.com/JosefLeinweber/scan_processing/actions/workflows/check_service_status.yml/badge.svg?branch=trunk)](https://github.com/JosefLeinweber/scan_processing/actions/workflows/check_service_status.yml) 

# scan_processing
The goal of the client application of Map-x-Markets is it to make generating a map of a store and storing categories such as vegetables, milk, pasta etc. on this map as easy as taking a video.

scan_processing is a microservice for Mapx-x-Market with the following funcitonality:

- Generate a floorplan from the data of a point cloud scan from the 3DScanner app (https://3dscannerapp.com/) for iOS devices

- Compute intersection points of the floor plan and the camera views to later map values to coordinates of the floorplan

# Setup

### Disclaimer: it does not make much sense to run this application localy without having the data from a scan and the point cloud of that scan uploaded to cloud storage

Prerequisits:

- [x] Docker instalation
- [x] Local Postgres server
- [x] Python 3.10
- [x] Cloud Storage & Service Account Key file

Steps to get it running

1. Clone the repo

2. Copy the service accout key file into your local repo, MAKE SURE TO ADD IT TO .git-ignore!

3. Use example.env to generate a .env file, change the POSTGRES values & the path to the service account key file

4. Run ```docker-compose build```

5. Run ```docker-compos up```

The Application should should now run!




