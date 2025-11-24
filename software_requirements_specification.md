**Project:** HADIS (Holistic Automated Disaster Intelligence System) **Standard:** IEEE 29148:2018

## 1. Introduction

### 1.1 Purpose

The purpose of this document is to define the functional and non-functional requirements for the HADIS framework. It serves as the primary reference for development, testing, and validation of the automated flood monitoring pipeline.

### 1.2 Scope

The system will automate the retrieval of satellite imagery (SAR/Optical) based on semantic triggers, perform AI-based flood extent and depth estimation, and output risk assessment matrices.

- **In-Scope:** EM-DAT parsing, GEE/Sentinel API integration, U-Net inference, Depth estimation, GeoParquet export.
- **Out-of-Scope:** Real-time hardware sensor integration, hydraulic infrastructure control.

### 1.3 Definitions & Acronyms

- **ARD:** Analysis-Ready Data.
- **ROI:** Region of Interest.
- **GEE:** Google Earth Engine.

---

## 2. Overall Description

### 2.1 Product Perspective

HADIS is a modular, cloud-native pipeline. It operates independently but interfaces with external systems:

1. **Input:** EM-DAT (Database), Copernicus/GEE (Satellite Providers).
2. **Output:** Risk Maps (consumed by GIS dashboards or Analysts).

### 2.2 User Characteristics

- **Primary User (Researcher/Data Engineer):** Configures pipeline parameters, monitors ETL logs.
- **Secondary User (Disaster Analyst):** Consumes the final GeoParquet/GeoTIFF outputs for decision making.

### 2.3 Assumptions and Dependencies

- **Dependency:** Continuous availability of Sentinel-1/2 data via GEE or Copernicus APIs.
- **Assumption:** The target area has a valid DEM (SRTM) available.

---

## 3. Specific Requirements

### 3.1 Functional Requirements (FR)

#### 3.1.1 Event Trigger & Parsing

- **FR-1:** The system **shall** parse text inputs to extract the "Geocoding," "Location," and "Time" attributes of each event.
- **FR-2:** If geocoding data is not present in the text input, the system **shall** query the Google Maps API to resolve the location coordinates.

#### 3.1.2 Data Retrieval

- **FR-3:** The system **shall** query Google Earth Engine for Sentinel-2 L2A images (with <20% cloud cover) and the Copernicus Data Space Ecosystem API for Sentinel-1 GRD/SLC images.
- **FR-4 (Hybrid Fallback):** If GEE data retrieval fails or is unavailable, the system **shall** automatically switch to the Copernicus Data Space Ecosystem API as a fallback source.
- **FR-5:** The system **shall** perform spatial alignment (co-registration) of Sentinel-1 and Sentinel-2 images and export the fused stack as a Zarr store.

#### 3.1.3 Inference Engine (CIE)

- **FR-6 (Extent):** The system **shall** generate a binary flood mask and a corresponding probability map.
- **FR-7 (Depth):** The system **shall** calculate water depth exclusively for pixels where the `flood_mask` value equals 1.
- **FR-8 (Uncertainty):** The system **shall** generate a standard deviation map quantifying uncertainty for both extent and depth predictions.

### 3.2 External Interface Requirements

- **User Interface:** A Command Line Interface (CLI) utilizing `argparse` for batch processing control.
- **Hardware Interface:** N/A (Cloud Environment).
- **Software Interface:**
    - **Input Format:** JSON (for event metadata).
    - **Output Format:** GeoParquet (for Vector data), COG (Cloud Optimized GeoTIFF for Raster data).

---

## 4. Non-Functional Requirements (Quality Attributes)

_This is critical for the "System" aspect of your research._

### 4.1 Performance

- **Latency:** The pipeline shall complete processing for a 100km2 ROI within 15 minutes of data availability.
- **Throughput:** The system shall support concurrent processing of at least 5 distinct disaster events.

### 4.2 Reliability

- **Failure Rate:** The ETL process must handle API timeouts (HTTP 503) with an exponential backoff retry mechanism (max 3 retries).

### 4.3 Accuracy (Specific to AI Projects)

- **Metric:** The Flood Extent Model shall achieve an Intersection over Union (IoU) > 0.75 on the validation set.
- **Metric:** The Depth Estimation MAE (Mean Absolute Error) shall be < 0.5 meters against validation benchmarks.