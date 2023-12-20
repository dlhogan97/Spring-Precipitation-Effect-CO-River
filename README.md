# Recent Colorado River Streamflow Deficits Explained by Decreased Spring Precipitation

## Overview

Welcome to the repository for my manuscript. This repository contains the code, data, and analysis tools used in my research paper titled "Colorado River Streamflow Declines Explained By Decreased Spring Precipitation."
[![DOI](zenodo.10413407.svg)](https://zenodo.org/account/settings/github/repository/dlhogan97/Spring-Precipitation-Effect-CO-River)
## Repository Structure

The repository is organized as follows:

- **Upper_CO_Analysis**: Contains all notebooks and data (see **Data Preparation** below) used in the analysis.
    - **notebooks**: Contains all files used in the analysis, in the form of Jupyter Notebooks.
    - **scripts**: Contains helper scripts used during data preparation, but not necessary for analysis
- **exploratory_scripts**: Contains other scripts used during data exploration
- **LICENSE**: The license file for this repository.

## Data

The data used in this research can be obtained [here](10.5281/zenodo.10056373). Please download the data and place it in the `data/` directory before running the analysis.

## Analysis Steps

To replicate or build upon the research, follow these steps:

1. **Clone the Repository:**
`git clone https://github.com/dlhogan97/Spring-Precipitation-Effect-CO-River.git`

2. **Install Dependencies:**
Use the `ucrb_analysis_env.yml` file to create an environment which will install all necessary dependencies for this analysis.

3. **Data Preparation:**
All data can be downloaded from [this zenodo repository](10.5281/zenodo.10056373)

4. **Run the Analysis:**
Navigate to the `notebooks` folder within `Upper_CO_Analysis`. A README is available within the `notebooks` folder to provide information about what each file is meant to do. Descriptions of each file are also available within the notebooks themselves. In summary, this folder contains a collection of Jupyter Notebooks, each serving a specific purpose in the analysis and development of products related to the study of the Upper Colorado River Basin (UCRB), PRISM data, Hydro-Climatic Data Network (HCDN), and associated investigations. Notebooks are categorized into numbered analysis files (e.g., `01_UCRB_exploratory_analysis_20230425.ipynb`) and development files (e.g., `dev_00_snowcourse_investigation.ipynb`).


5. **Citation:**
If you use or build upon this research, please provide proper attribution and cite the original paper (citation to be updataed upon publication).

## License

This repository is open-source and available under the MIT License. Please review the license for terms and conditions of use.

## Contact

If you have any questions or need further information, feel free to contact me at dlhogan@uw.edu.

