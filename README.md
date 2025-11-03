# 🏋️‍♀️ ActiveFinder — Sports Facilities LBS Web Application

**ActiveFinder** is a Location-Based Services (LBS) web application built with **Django, PostGIS, and Leaflet**.  
It allows users to visualize and explore nearby sports facilities (e.g., gyms, rinks, pools) on an interactive map, filter them by sport type, and perform advanced spatial queries such as *nearest*, *within radius*, and *within bounding box*.

---

## 🚀 Features

### 🗺️ Mapping & Visualization
- Interactive **Leaflet.js** map using **OpenStreetMap** tiles  
- Facility markers with color-coded sport types and popups  
- “📍 Show My Location” button  
- Adjustable **radius slider** to find nearby facilities  

### 🧠 Spatial Functionality
- PostgreSQL + **PostGIS** spatial database  
- Stores facilities as geographic `Point` objects  
- **Spatial queries implemented:**
  - `nearest` → find the closest facility to given coordinates  
  - `within_radius` → find all facilities within a distance (km)  
  - `in_bbox` → find facilities within a bounding box  

### ⚙️ API (RESTful)
Built with **Django REST Framework (DRF)**  
Returns **GeoJSON FeatureCollections** (Leaflet-compatible)

**Endpoints:**
| Method | Endpoint | Description |
|:--:|:--|:--|
| `GET` | `/api/facilities/` | All facilities (GeoJSON) |
| `GET` | `/api/facilities/nearest/?lat=&lon=` | Nearest facility |
| `GET` | `/api/facilities/within_radius/?lat=&lon=&km=` | Facilities within km radius |
| `GET` | `/api/facilities/in_bbox/?minx=&miny=&maxx=&maxy=` | Facilities in bounding box |

---

## 🧩 Architecture

| Layer | Technology | Purpose |
|-------|-------------|----------|
| Database | **PostgreSQL + PostGIS** | Store and query spatial data |
| Backend | **Django 5 + Django REST Framework** | REST API and MVC logic |
| Frontend | **Leaflet + Bootstrap 5** | Interactive responsive map |
| Admin | **Django Admin + Leaflet Widget** | Manage facilities visually |
| Bonus | *(optional)* **Docker + Nginx + PgAdmin4** | Local production deployment |

---

## 🧱 Tech Stack

- Python 3.12  
- Django 5.2.7  
- Django REST Framework  
- Django REST Framework GIS  
- Django Leaflet  
- PostgreSQL 17 + PostGIS 3.5  
- Leaflet 1.9.4  
- Bootstrap 5.3  

---

## 💻 Local Setup Instructions

### 1️⃣ Clone the repository

```bash
git clone https://github.com/<your-username>/ActiveFinder.git
cd ActiveFinder
