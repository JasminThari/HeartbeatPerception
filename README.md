# Heartbeat Perception - Understanding the Influence of Body Movement and Facial Features When Identifying the Owner of a Heartbeat

This repository contains the necessary code to conduct, analyze, and visualize the results of our experiment. Below is an overview of the repository's structure and functionality.

## Repository Structure

```
.
├── Data/
│   ├── Answers/        # Contains answers provided by each participant
│   ├── Results/        # Combined results merged with the correct responses
├── src/
│   ├── run_experiment.py       # Script to run the experiment using PsychoPy
│   ├── power_analysis.py       # Script to perform power analysis and calculate sample size
│   ├── statistical_analysis.py # Script for statistical computations and hypothesis testing
│   ├── ...                     # Other scripts for additional analysis and plotting
```

## Description of Key Scripts

### `run_experiment.py`
This script is used to execute the experiment in **PsychoPy**. It requires specific video stimuli and EEG signal data, which are not included in this repository to ensure compliance with GDPR. 

### `power_analysis.py`
This script performs a **power analysis** to determine the required sample size for the experiment. 

### `statistical_analysis.py`
This script computes the **dependent variable**, conducts statistical analyses, and performs hypothesis testing, including:
- **Descriptive statistics**
- **Parametric tests**
- **T-tests**
- **ANOVA tests**

### Other Scripts
The repository also includes additional scripts for various analyses and plotting purposes. These can be used to further explore and visualize the experiment's data.

## Data Privacy
To protect participant confidentiality and comply with GDPR regulations, sensitive data such as video stimuli and EEG signals are not included in this repository. Please contact us for data access requests.
