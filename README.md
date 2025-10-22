---
title: Project Specification

---

# Overview

### HAZAMA

**Combining multi-source remote sensing imagery and for reconstruction of spatio-temporal flood extent and depth database**

### Objectives

1. **Build multi-sourced event-based flood extent database**

:::info
**Integrate data from satellite, DEM, glofas, text record, etc.**
::: 
    
2. **Explore data-driven method potential for historical flood extent reconstruction**

:::info
**Apply ML on flood extent reconstruction**
:::

# Goals & Deliverables

### **I. Flood extent detection on GEE**
- [ ] **Practice basic flood detection methods**
    - [ ] Change detection: S1 SAR
    - [ ] Image classification: S2/Landsat
- [ ] Extrapolate using *FLEXTH*
- [ ] Event-based study for specific areas

### **II. ML workflow design**
- [ ] Hand-on practice of *ML4Flood*

### **III. AI approach: Apply ML in hisorical flood extent reconstructing**
- [ ] **Literature review**: state-of-the-art  **AI application** for flood detection
- [ ] Design experiments to test the performance of **different input** (e.g. DEM) or **model structure**

### **IV. Building event-based flood database**
- [ ] Collect flood extent data from existing dataset
- [ ] Explore data from satellite, DEM, glofas, text record, etc
- [ ] Integrate multi-sourced data for further research

### **V. GEE App visualization**
- [ ] Build a viualization app with GEE app


# Resources

### Slides
https://docs.google.com/presentation/d/1sLopNjr3TdTDjE2u11mk9vXsgPQm07Gr2cjEPIDE3BM/edit?usp=sharing

### Google drive
https://drive.google.com/drive/folders/1Y34PzrjlTWpENcRUFSVVVylxa8NOC-7e?usp=sharing

### ML4Flood

https://github.com/spaceml-org/ml4floods.git

## Datasets
### The WorldFloods database (ML4Flood)

https://spaceml-org.github.io/ml4floods/content/worldfloods_dataset.html

### core-five: Multi-Modal Geospatial Dataset with Perfectly Harmonized Time & Space for Foundation Models

https://huggingface.co/datasets/gajeshladhar/core-five?fbclid=IwZXh0bgNhZW0CMTEAAR4OF-vvawD4tzB5ECFzvCoO9Mn0upF-dbeVAmD-DIoZ0rWyh39vKdPyc_hnrA_aem_l9idjH0W_YbdP3kZuPbFkw

## Papers
Fakhri, F., & Gkanatsios, I. (2025). Quantitative evaluation of flood extent detection using attention U-Net case studies from Eastern South Wales Australia in March 2021 and July 2022. Scientific Reports, 15(1), 12377. https://doi.org/10.1038/s41598-025-92734-x
Mateo-Garcia, G., Veitch-Michaelis, J., Purcell, C., Longepe, N., Reid, S., Anlind, A., Bruhn, F., Parr, J., & Mathieu, P. P. (2023). In-orbit demonstration of a re-trainable machine learning payload for processing optical imagery. Scientific Reports, 13(1), 10391. https://doi.org/10.1038/s41598-023-34436-w
Portalés-Julià, E., Bountos, N. I., Sdraka, M., Mateo-García, G., Papoutsis, I., & Gómez-Chova, L. (2024). Multimodal and Multitemporal Data Fusion for Flood Extent Segmentation Exploiting Kurosiwo and WorldFloods Sentinel Datasets. IGARSS 2024 - 2024 IEEE International Geoscience and Remote Sensing Symposium, 950–953. https://doi.org/10.1109/IGARSS53475.2024.10690461
Portalés-Julià, E., Mateo-García, G., Purcell, C., & Gómez-Chova, L. (2023). Global flood extent segmentation in optical satellite images. Scientific Reports, 13(1), 20316. https://doi.org/10.1038/s41598-023-47595-7
Sharma, N. K., & Saharia, M. (2025). DeepSARFlood: Rapid and automated SAR-based flood inundation mapping using vision transformer-based deep ensembles with uncertainty estimates. Science of Remote Sensing, 11, 100203. https://doi.org/10.1016/j.srs.2025.100203
Tsutsumida, N., Tanaka, T., & Sultana, N. (2025). Automated flood detection from Sentinel-1 GRD time series using Bayesian analysis for change point problems (No. arXiv:2504.19526). arXiv. https://doi.org/10.48550/arXiv.2504.19526



# Data list
## Spatial data

| **Data**                                                                              | **Type**       | **Source** | **Details**             |
| ------------------------------------------------------------------------------------- | -------------- | ---------- | ----------------------- |
| Sentinel-1 SAR GRD: C-band Synthetic Aperture Radar Ground Range Detected,log scaling | SAR C-band     | GEE        | 2014-                   |
| GPM: Global Precipitation Measurement (GPM) Release 07                                | Precipitation  | GEE        | 2000-                   |
| Sentinel-2                                                                            | Multispectral  | GEE        | 2015-, revisit: 5 days  |
| Landsat 1-5                                                                           | Multispectral  | GEE        | 1972-, revisit: 16 days |
| River discharge and related historical data                                           | Discharge rate | GloFAS     |                         |

## Flood event data
| **Data**                             | **Type** | **Details** |
| ------------------------------------ | -------- | ----------- |
| EM-DAT                               | .csv     |             |
| Global Flood Database v1 (2000-2018) | GEE      |             |
|ML4flood world flood database         |          |https://spaceml-org.github.io/ml4floods/content/worldfloods_dataset.html |
# Overview

### HAZAMA

**Reconstruction of Historical Flood Extents Based on Synthetic Aperture Radar and Multi-Source Data Applications**


### Objectives

1. **Build multi-sourced event-based flood extent database**

:::info
**Integrate data from satellite, DEM, glofas, text record, etc.**
::: 
    
2. **Explore data-driven method potential for historical flood extent reconstruction**

:::info
**Apply ML on flood extent reconstruction**
:::

# Goals & Deliverables

### **I. Flood extent detection on GEE**
- [ ] **Practice basic flood detection methods**
    - [ ] Change detection: S1 SAR
    - [ ] Image classification: S2/Landsat
- [ ] Extrapolate using *FLEXTH*
- [ ] Event-based study for specific areas

### **II. ML workflow design**
- [ ] Hand-on practice of *ML4Flood*

### **III. AI approach: Apply ML in hisorical flood extent reconstructing**
- [ ] **Literature review**: state-of-the-art  **AI application** for flood detection
- [ ] Design experiments to test the performance of **different input** (e.g. DEM) or **model structure**

### **IV. Building event-based flood database**
- [ ] Collect flood extent data from existing dataset
- [ ] Explore data from satellite, DEM, glofas, text record, etc
- [ ] Integrate multi-sourced data for further research

### **V. GEE App visualization**
- [ ] Build a viualization app with GEE app


# Resources

### Slides
https://docs.google.com/presentation/d/1sLopNjr3TdTDjE2u11mk9vXsgPQm07Gr2cjEPIDE3BM/edit?usp=sharing

### Google drive
https://drive.google.com/drive/folders/1Y34PzrjlTWpENcRUFSVVVylxa8NOC-7e?usp=sharing

### ML4Flood

https://github.com/spaceml-org/ml4floods.git

## Datasets
### The WorldFloods database (ML4Flood)

https://spaceml-org.github.io/ml4floods/content/worldfloods_dataset.html

### core-five: Multi-Modal Geospatial Dataset with Perfectly Harmonized Time & Space for Foundation Models

https://huggingface.co/datasets/gajeshladhar/core-five?fbclid=IwZXh0bgNhZW0CMTEAAR4OF-vvawD4tzB5ECFzvCoO9Mn0upF-dbeVAmD-DIoZ0rWyh39vKdPyc_hnrA_aem_l9idjH0W_YbdP3kZuPbFkw

## Papers
Fakhri, F., & Gkanatsios, I. (2025). Quantitative evaluation of flood extent detection using attention U-Net case studies from Eastern South Wales Australia in March 2021 and July 2022. Scientific Reports, 15(1), 12377. https://doi.org/10.1038/s41598-025-92734-x
Mateo-Garcia, G., Veitch-Michaelis, J., Purcell, C., Longepe, N., Reid, S., Anlind, A., Bruhn, F., Parr, J., & Mathieu, P. P. (2023). In-orbit demonstration of a re-trainable machine learning payload for processing optical imagery. Scientific Reports, 13(1), 10391. https://doi.org/10.1038/s41598-023-34436-w
Portalés-Julià, E., Bountos, N. I., Sdraka, M., Mateo-García, G., Papoutsis, I., & Gómez-Chova, L. (2024). Multimodal and Multitemporal Data Fusion for Flood Extent Segmentation Exploiting Kurosiwo and WorldFloods Sentinel Datasets. IGARSS 2024 - 2024 IEEE International Geoscience and Remote Sensing Symposium, 950–953. https://doi.org/10.1109/IGARSS53475.2024.10690461
Portalés-Julià, E., Mateo-García, G., Purcell, C., & Gómez-Chova, L. (2023). Global flood extent segmentation in optical satellite images. Scientific Reports, 13(1), 20316. https://doi.org/10.1038/s41598-023-47595-7
Sharma, N. K., & Saharia, M. (2025). DeepSARFlood: Rapid and automated SAR-based flood inundation mapping using vision transformer-based deep ensembles with uncertainty estimates. Science of Remote Sensing, 11, 100203. https://doi.org/10.1016/j.srs.2025.100203
Tsutsumida, N., Tanaka, T., & Sultana, N. (2025). Automated flood detection from Sentinel-1 GRD time series using Bayesian analysis for change point problems (No. arXiv:2504.19526). arXiv. https://doi.org/10.48550/arXiv.2504.19526



# Data list
## Spatial data

| **Data**                                                                              | **Type**       | **Source** | **Details**             |
| ------------------------------------------------------------------------------------- | -------------- | ---------- | ----------------------- |
| Sentinel-1 SAR GRD: C-band Synthetic Aperture Radar Ground Range Detected,log scaling | SAR C-band     | GEE        | 2014-                   |
| GPM: Global Precipitation Measurement (GPM) Release 07                                | Precipitation  | GEE        | 2000-                   |
| Sentinel-2                                                                            | Multispectral  | GEE        | 2015-, revisit: 5 days  |
| Landsat 1-5                                                                           | Multispectral  | GEE        | 1972-, revisit: 16 days |
| River discharge and related historical data                                           | Discharge rate | GloFAS     |                         |

## Flood event data
| **Data**                             | **Type** | **Details** |
| ------------------------------------ | -------- | ----------- |
| EM-DAT                               | .csv     |             |
| Global Flood Database v1 (2000-2018) | GEE      |             |
|ML4flood world flood database         |          |https://spaceml-org.github.io/ml4floods/content/worldfloods_dataset.html |
