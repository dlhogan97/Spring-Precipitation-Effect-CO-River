# Notebooks Repository Readme

## Overview

This repository contains a collection of Jupyter Notebooks, each serving a specific purpose in the analysis and development of products related to the study of the Upper Colorado River Basin (UCRB), PRISM data, Hydro-Climatic Data Network (HCDN), and associated investigations. Notebooks are categorized into numbered analysis files (e.g., `01_UCRB_exploratory_analysis_20230425.ipynb`) and development files (e.g., `dev_00_snowcourse_investigation.ipynb`).

## Numbered Analysis Notebooks

### 01_UCRB_exploratory_analysis_20230425.ipynb
- **Description:** Exploratory analysis of key variables in the Upper Colorado River Basin.
- **Purpose:** Understand the patterns and trends in UCRB data and begin to focus on the HCDN basins used in the analysis

### 02_UCRB_PRISM_analysis_20230905.ipynb
- **Description:** In-depth analysis of UCRB data with respect to PRISM precipitation and temperature data.
- **Purpose:** Investigate relationships and correlations between UCRB variables and PRISM precipitation data. This script builds some figures used in the manuscript.

### 02B_UCRB_PRISM_analysis_20230905.ipynb
- **Description:** Comparison of PRISM with 2 other precipitation products, ERA5 and NClimgrid.
- **Purpose:** The purpose of this notebook is to establish the reliability of PRISM data for this analysis by looking for similar trends and information in other gridded precipitation products. 

### 03_HCDN_elevation_analysis_20230729.ipynb
- **Description:** Analysis focused on elevation-related variables in the Hydro-Climatic Data Network.
- **Purpose:** Explore the impact of elevation on hydro-climatic patterns in HCDN. This is where the brunt of the analysis is performed to look for significant changes in precipitation patterns and streamflow in the HCDN basins we analyzed. This script builds some figures used in the manuscript.

### 04_PRISM_ppt_gage_evaluation_20231017.ipynb
- **Description:** Evaluation of PRISM precipitation data against gauge measurements distributed throughout UCRB headwater basins.
- **Purpose:** Assess the accuracy and reliability of PRISM precipitation estimates. 

### 05_HCDN_additional_analysis_20230822.ipynb
- **Description:** Additional analysis of Hydro-Climatic Data Network streamflow, its distribution throughout the basins and changes in specific basins.
- **Purpose:** Investigate specific aspects of the streamflow changes during the Millennium Drought and the differences seen with elevation. This script builds some figures used in the manuscript.

### 06_UCRB_PET_20230907.ipynb
- **Description:** Analysis of Potential Evapotranspiration (PET) in the Upper Colorado River Basin.
- **Purpose:** Understand the patterns and factors influencing PET in the UCRB. Also, explores the relationship between spring precipitation and spring temperature/PET. This script builds some figures used in the manuscript.

### 06B_ERA5_ENERGY_ONLY_20240121.ipynb
- **Description:** Analysis and creation of the PET energy-only dataset in the Upper Colorado River Basin using ERA5-Land data.
- **Purpose:** Here we use radiation components from ERA5 to calculate the Energy-Only PET between 1964-2022. We first look into the radiation components themselves and see how they relate to one another. Then, we adjust the PET-EO values for snow covered area from MODIS observations between 2001-2017. Lastly, we look at how PET changes with snow cover and elevation between wet and dry springs.

### 07_UCRB_SENSITIVITY_20240130.ipynb
- **Description:** This notebook will look at how sensitive potential evapotranspiration is to changes in precipitation over the Upper Colorado River basin between 1964 and 2022. We employ a strategy of looking at the average gradient in the relationship to determine how sensitive one variable is to another, since they both estimate the same quanity (water).
- **Purpose:** Understand the patterns and factors influencing PET in the UCRB. Also, explores the relationship between spring precipitation and spring temperature/PET. This script builds some figures used in the manuscript.

## Development Notebooks

### dev_00_snowcourse_investigation.ipynb
- **Description:** Notebook for development and investigation related to snowcourse data.
- **Purpose:** Experiment with ideas and concepts incorporated into formal analyses.This script builds some figures used in the manuscript.

### dev_01_UCRB_DEM.ipynb
- **Description:** Development notebook for creating Digital Elevation Models (DEMs) specific to the UCRB.
- **Purpose:** Test and refine methods for DEM creation.

### dev_01B_get_basins.ipynb
- **Description:** Development notebook for selecting headwater basins from the Gages II dataset and HCDN.
- **Purpose:** Organize the selection of headwater basins in an explicit and reproducible manner.

### dev_02_UCRB_reservoir_ET_and_snow.ipynb
- **Description:** Development notebook for estimating evaporation over UCRB reservoirs and exploring general changes in UCRB snow metrics.
- **Purpose:** Develop methods for ET estimation applicable to reservoirs. Also look into trends in snow metrics across the UCRB. Not used in formal analysis.

### dev_03_HCDN_snomelt_dates.ipynb
- **Description:** Development notebook for investigating snowmelt dates in HCDN.
- **Purpose:** Experiment with methodologies for determining snowmelt timing. Output is used in 05.

### dev_04_riparian_et_estimates.ipynb
- **Description:** Development notebook for estimating Evapotranspiration (ET) in riparian areas.
- **Purpose:** Explore techniques for ET estimation in riparian zones. Not used in formal analysis.

### dev_05_asos_cld.ipynb
- **Description:** Development notebook for looking at cloud cover observations from UCRB ASOS stations.
- **Purpose:** Explore the relationship between cloud cover observations and modeled output from ERA5.

### dev_06_modis_sca_elevation.ipynb
- **Description:** Development notebook for where we use a cleaned, cloud free daily MODIS snow covered extent product from a 2019 publication in Nature to quantify the change of snow covered extent during anomalously wet and dry spring seasons defined between March and May.
- **Purpose:** Explore how snow covered area changes with elevation over the season and between wet and dry years.

### dev_07_build_tables.ipynb
- **Description:** Builds some basic tables for summarizing streamflow data.
- **Purpose:** To get simple metrics for streamflow.