# Project Specification
## Overview

**HAZAMA: Reconstruction of Historical Flood Extents Based on Synthetic Aperture Radar and Multi-Source Data Applications**
**Objective:** Utilize existing remote sensing satellite data, in combination with numerical hydrological models, weather data, and historical disaster records, and apply machine learning or deep learning techniques to reconstruct global historical flood extent spatial data.

## Goals & Deliverables

- [ ] An **event-based** **spatial** global flood database
- [ ] AI model for reconstructing **historical flood extent map (1972-now)**
- [ ] Apply **Physics-informed ML** or **DL**
- [ ] Systematic error and output uncertainty analysis
- [ ] Build interactive web visualization

# Task Breakdown

## 1. Data Preparation (pipeline)

- [ ] **T 1.1:** GEE API tutorial(.ipynb, .md)
- [ ] **T 1.2:** Data downloader with XEE, save to local (pipeline)
- [ ] **T 1.3:** Event-based 
- [ ] **T 1.4:** Data structure
## 2. Data Preprocessing

- [ ] **T 2.1:** Derive SAR inundation map
- [ ] **T 2.2:** 
- [ ] **T 2.3:**
## 3. Case Studies

- [ ] **T 3.1:** 
- [ ] **T 3.2:** 
- [ ] **T 3.3:**
## 4. Database Building

- [ ] **T 4.1:** 
- [ ] **T 4.2:** 
- [ ] **T 4.3:**
## 5. Literature review

- [ ] **T 5.1:** 
- [ ] **T 5.2:** 
- [ ] **T 5.3:**

## Data sources

### Spatial data

| **Data**                                                                              | **Type**       | **Source** | **Details**             |
| ------------------------------------------------------------------------------------- | -------------- | ---------- | ----------------------- |
| Sentinel-1 SAR GRD: C-band Synthetic Aperture Radar Ground Range Detected,log scaling | SAR C-band     | GEE        | 2014-                   |
| GPM: Global Precipitation Measurement (GPM) Release 07                                | Precipitation  | GEE        | 2000-                   |
| Sentinel-2                                                                            | Multispectral  | GEE        | 2015-, revisit: 5 days  |
| Landsat 1-5                                                                           | Multispectral  | GEE        | 1972-, revisit: 16 days |
| River discharge and related historical data                                           | Discharge rate | GloFAS     |                         |

### Flood event data
| **Data**                             | **Type** | **Details** |
| ------------------------------------ | -------- | ----------- |
| EM-DAT                               | .csv     |             |
| Global Flood Database v1 (2000-2018) | GEE      |             |
|ML4flood world flood database         |          |https://spaceml-org.github.io/ml4floods/content/worldfloods_dataset.html |
