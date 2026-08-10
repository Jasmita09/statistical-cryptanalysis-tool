# Statistical Cryptanalysis Tool

This repository contains a Python-based data science project that pivots a traditional cybersecurity brute-force script into an automated Natural Language Processing (NLP) tool. 

Rather than forcing a user to manually scroll through dozens of decrypted outputs to find readable English, this program applies a Chi-Squared Goodness-of-Fit test to mathematically assess and identify the most likely decryption key. 

### Key Features
* **Automated Cryptanalysis:** Uses probability and statistics to predict shift keys without human intervention.
* **Data-Driven Evaluation:** Compares candidate letter frequency distributions against standard English frequencies.
* **Structured Data Processing:** Analyzes and ranks candidate decryptions using Pandas and NumPy.
* **Visual Analytics:** Plots the statistical divergence of each key using Matplotlib to show the mathematical proof of the correct key.
