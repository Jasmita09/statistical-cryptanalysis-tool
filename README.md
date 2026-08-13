# Extended ASCII Cryptanalysis & Data Science Tool

This repository contains a Python-based data science project that transforms a traditional cybersecurity brute-force script into an optimized, automated Natural Language Processing (NLP) tool. 

Rather than requiring a user to manually scroll through 95 separate decrypted candidates to find readable English, this program applies a statistical **Chi-Squared Goodness-of-Fit test** to mathematically assess, rank, and identify the correct decryption key automatically.

---

## Architectural & Performance Highlights

This project was rebuilt to move past basic procedural Python and implement intermediate-level computer science and data science optimizations:

* **Big-O Complexity Optimization ($O(N)$ Time Complexity):** Replaced redundant, iterative string scans (which scanned the entire text 26 times using `.count()`) with a single-pass frequency map using Python's C-optimized `collections.Counter`. This reduces the computational operations on long texts by up to 26 times.
* **True Vectorization via Pandas:** Completely eliminated slow mathematical `for` loops inside the statistical calculation. By converting data into **Pandas Series**, the Chi-Squared formula `(Observed - Expected)^2 / Expected` is computed across all 26 character distributions simultaneously in compiled C.
* **Memory Optimization (String Immutability):** Replaced inefficient string-appending loops (which constantly reallocate memory in Python) with optimized list comprehensions and C-implemented `"".join()` operations.
* **Extended ASCII Keyspace:** Upgraded the cipher engine to encrypt and decrypt across the entire **95-character printable ASCII range** (ASCII 32 to 126). Punctuation, symbols, numbers, and spaces are actively scrambled into other ASCII characters during encryption.
* **Defensive Programming & Fail-Safes:** Implemented robust error handling with `try-except` blocks. If the external `english_frequency.csv` is missing, the program automatically loads a uniform fallback frequency dataset and uses safe `.get()` lookups to prevent fatal crashes.

---

## Key Features

* **Automated Cryptanalysis:** Uses probability and statistics to predict shift keys across a 95-character space without human intervention.
* **Text Normalization (Feature Extraction):** Cleans candidate decryptions in $O(N)$ time, isolating and converting only alphabetic characters to uppercase to filter out statistical "noise."
* **Visual Analytics:** Generates a custom **Matplotlib** line chart that automatically identifies the coordinate of the minimum statistical score and highlights it with a contrasting red marker, clean dashed gridlines, and a legend.

---

## How the Chi-Squared Evaluation Works

The program decrypts the ciphertext using all 95 possible keys. For each candidate decryption, it counts the occurrences of each letter and compares them to standard English frequencies using the formula:

`Chi-Squared = sum( (Observed - Expected)^2 / Expected )`

* **Observed:** The actual count of a letter in the decrypted candidate.
* **Expected:** The count we mathematically expect to see based on standard English percentages for a text of that length.

Gibberish candidates generate huge mathematical penalties, while the correct English decryption aligns with standard language patterns, generating the absolute lowest score.
