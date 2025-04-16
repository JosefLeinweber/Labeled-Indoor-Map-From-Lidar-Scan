  [![Automated Tests](https://github.com/JosefLeinweber/scan_processing/actions/workflows/automated-tests.yml/badge.svg?branch=trunk)](https://github.com/JosefLeinweber/scan_processing/actions/workflows/automated-tests.yml) [![Build & Push to GAR and Deploy to Cloud Run](https://github.com/JosefLeinweber/scan_processing/actions/workflows/cd_google_cloud_run.yml/badge.svg)](https://github.com/JosefLeinweber/scan_processing/actions/workflows/cd_google_cloud_run.yml)[![Check Service Status](https://github.com/JosefLeinweber/scan_processing/actions/workflows/check_service_status.yml/badge.svg?branch=trunk)](https://github.com/JosefLeinweber/scan_processing/actions/workflows/check_service_status.yml) 

# Labeled Indoor Map From Lidar Scan
This is a microservice created for the university project Maps-x-Markets. The idea of Maps-x-Markets was to provide users with searchable indoor maps of hardware stores, making it easier for them to find what they are looking for.

During the development, this microservice was named scan_processing. The purpose of scan_processing is to make generating a map of a store and storing categories, such as vegetables, milk, pasta, etc., on this map as easy as taking a video.

## Functionality:

- Generate a floorplan from the data of a point cloud scan from the 3DScanner app (https://3dscannerapp.com/) for iOS devices.
- Compute intersection points of the floor plan and the camera views of the images taken during the lidar scan.
- An ML model can then classify the images, and the classification value can be mapped to the intersection point.

## Setup

#### Disclaimer: it does not make much sense to run this application locally without having the data from a scan and the point cloud of that scan uploaded to cloud storage

### Prerequisites:

- [x] Docker installation
- [x] Local Postgres server
- [x] Python 3.10
- [x] Cloud Storage & Service Account Key file

### Steps to get it running

1. Clone the repo

2. Copy the service accout key file into your local repo, MAKE SURE TO ADD IT TO .git-ignore!

3. Use example.env to generate a .env file, change the POSTGRES values & the path to the service account key file

4. Run ```docker-compose build```

5. Run ```docker-compos up```

The Application should now run!

## CI/CD Visualisation

![alt text](https://github.com/JosefLeinweber/scan_processing/blob/671e22003068d3bd202388bd748d92c7c1889037/docs/images/cicd_visualization.png)

## Running Automated Tests

1. Start the application with ```docker-compose up```

2. Run ```docker-compose exec scan_processing_service pytest```
