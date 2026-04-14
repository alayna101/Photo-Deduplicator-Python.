# AI-Powered Photo Deduplicator & Quality Auditor

## Project Overview
This project was developed to solve a real-world data management problem: identifying and removing thousands of duplicate images across a complex mobile file system. Utilizing **Perceptual Hashing**, the tool identifies visually identical images regardless of filename changes or compression levels.

## Key Features
* **Visual Deduplication:** Uses the `Pillow` library to generate 64-bit average hashes, allowing for size-independent image comparison.
* **Data Integrity Audit:** A secondary "Quality Audit" script that cross-references duplicates against originals to ensure the highest-resolution version is preserved while lower-quality thumbnails are moved for deletion.
* **Recursive Scanning:** Automated traversal of complex Android directory structures (DCIM, Pictures, etc.).

## Technical Implementation
* **Language:** Python 3
* **Libraries:** `PIL` (Pillow), `hashlib`, `os`, `shutil`
* **Environment:** Developed and executed on Android via Termux using the Gemini CLI.

## Professional Background
Coming from a background in **English and Loan Documentation**, I prioritize data accuracy and thorough documentation. This project demonstrates my ability to bridge the gap between technical automation and meticulous data integrity.

