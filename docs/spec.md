**Project:** HAZAMA - A Flood Event Intelligent Information Acquisition System

# 1. Objective

Develop am automatic pipeline to cross-reference flood event lists with satellite imagery catalogs (Copernicus/ESA and Google Earth Engine), The system must identify and log available imagery that capture the flood location within a specific temporal and spatial windows.

# 2. Functional Requirements

## 2.1 Data Ingestion

The system must parse the input .csv with mandatory fields

- `event_id` : ID (String)
- `date` : Disaster occurrence date (ISO 8601: YYYY-MM-DD)
- `latitude` (Float, WGS84)
- `longitude` (Float, WGS84)
- `bbox`

## 2.1 Validation
