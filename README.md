ActiveFinder: Sports Facilities Location-Based Web Application

ActiveFinder is a location-based web app built with Django, PostGIS, and Leaflet.
It helps users explore nearby sports facilities like gyms, pools, and rinks on an interactive map.
Users can search for facilities within a set distance, find the closest one, or browse by area.

Main Features
Mapping and Interaction

Interactive map using Leaflet.js and OpenStreetMap

Markers show facility types with popups for more info

Option to find nearby facilities or show user location

Spatial Functionality

Uses PostgreSQL + PostGIS for spatial data

Stores facilities as geographic points

Implements key spatial queries:

Nearest – returns the closest facility

Within radius – finds facilities within a set distance

Bounding box – filters facilities inside a map area

API

Built with Django REST Framework and DRF-GIS, returning data in GeoJSON (works with Leaflet).

Method	Endpoint	Description
GET	/api/facilities/	All facilities
GET	/api/facilities/nearest/?lat=&lon=	Nearest facility
GET	/api/facilities/within_radius/?lat=&lon=&km=	Facilities within a radius
GET	/api/facilities/in_bbox/?minx=&miny=&maxx=&maxy=	Facilities in a bounding box
Tech Overview
Layer	Tools
Database	PostgreSQL + PostGIS
Backend	Django + Django REST Framework
Frontend	Leaflet + Bootstrap 5
Deployment	Docker + Nginx + PgAdmin

Stack: Python 3.12, Django 5.2.7, PostGIS 3.5, Leaflet 1.9.4, Bootstrap 5.3

Setup (Local)

Clone the repository

git clone https://github.com/TUD-AWM/week-1-lab-full-stack-web-mapping-environment-setup-roxanarakhmatullina.git
cd ActiveFinder


Run the project

docker-compose up --build


Access the app

Web app → http://localhost

Admin panel → http://localhost/admin

PgAdmin → http://localhost:5050

Default login:

Username: admin

Password: admin   

Project Summary

ActiveFinder follows the MVC architecture and uses PostGIS to manage spatial data.
Users can view facilities on a map, filter them by distance or area, and interact with popups.
The project runs fully in Docker with Django, PostgreSQL, and Nginx containers.

Future Improvements

Add user authentication and facility reviews

Improve map styling and mobile layout

Optional: deploy to a cloud platform (AWS or Render)es/nearest/?lat=&lon=	Finds the nearest facility
GET	/api/facilities/within_radius/?lat=&lon=&km=	Finds facilities within a radius
GET	/api/facilities/in_bbox/?minx=&miny=&maxx=&maxy=	Finds facilities within a bounding box
System Architecture
Layer	Technology	Description
Database	PostgreSQL with PostGIS	Stores and manages spatial data
Backend	Django and Django REST Framework	Application logic and REST API
Frontend	Leaflet.js and Bootstrap 5	Map visualization and interface
Administration	Django Admin with Leaflet integration	Facility management interface
Deployment	Docker, Nginx, PgAdmin4	Local containerized deployment environment
Technology Stack

Python 3.12

Django 5.2.7

Django REST Framework

Django REST Framework GIS

Django Leaflet

PostgreSQL 17 with PostGIS 3.5

Leaflet 1.9.4

Bootstrap 5.3

Nginx (reverse proxy)

Docker and Docker Compose

Local Setup Instructions

Clone the repository
git clone https://github.com/TUD-AWM/week-1-lab-full-stack-web-mapping-environment-setup-roxanarakhmatullina.git

cd ActiveFinder

Start the Docker environment
docker-compose up --build

This command launches:

PostgreSQL with PostGIS

Django web application

Nginx reverse proxy

PgAdmin4 for database management

Access the application

Web app: http://localhost

Django admin: http://localhost/admin

PgAdmin: http://localhost:5050

Application Overview

The system implements a complete MVC structure with a spatially enabled database and a web-based map interface.
Users can browse available facilities and interact with spatial queries through an integrated REST API.
All components are containerized for local deployment using Docker, providing a stable and reproducible environment.
<img width="935" height="465" alt="image" src="https://github.com/user-attachments/assets/ba0e7a4d-6dab-438e-b3df-1329fb9b35c6" />     
<img width="940" height="467" alt="image" src="https://github.com/user-attachments/assets/7f7bf132-f925-4ace-9320-38ddccdca902" />



Test Credentials:
Username: admin
Password: admin123

Known Issues or Future Improvements

Minor CSS styling inconsistencies between devices

Could be extended with user authentication and facility reviews

Potential future deployment to a cloud environment (e.g., AWS or Render)

Assignment Alignment
Database Layer

PostgreSQL configured with PostGIS extension

Facilities stored as spatial points with indexes for efficient querying

Three spatial queries implemented: nearest, within radius, and bounding box

Middle Tier (Django)

Follows the MVC architecture using Django models, views, and serializers

RESTful API built with Django REST Framework and DRF-GIS

Input validation and proper serialization for GeoJSON outputs

Front-End and User Interface

Responsive design created with Bootstrap 5

Leaflet.js provides an interactive map interface with facility markers and filters

Works effectively across desktop and mobile screens

Mapping Integration

OpenStreetMap used as a base map layer

Interactive Leaflet components include popups, radius search, and dynamic facility updates

GeoJSON responses displayed seamlessly on the map

Deployment

Fully containerized using Docker Compose

Includes separate containers for Django, PostgreSQL (with PostGIS), PgAdmin, and Nginx

Nginx acts as a reverse proxy for the web application

Environment variables used for configuration

Code Quality and Documentation

Clear file structure and code comments throughout

Requirements specified in requirements.txt

Comprehensive README file for setup, architecture, and usage instructions

Bonus: Advanced Docker Deployment

Uses a custom Docker network with isolated containers

Nginx configured as a reverse proxy to handle static files and API routing

Demonstrates production-oriented structure for local deployment
