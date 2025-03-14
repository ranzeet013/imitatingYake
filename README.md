# ImitatingYAKE

## Overview

This project implements a keyword extraction system inspired by YAKE (Yet Another Keyword Extractor). The approach relies on NLP techniques such as tokenization, n-gram generation, frequency analysis, and contextual features to identify important keywords from HTML documents.

## Features

- **Tokenization**: Preprocesses text by removing stopwords and extracting relevant words.
- **HTML Parsing**: Extracts meaningful content from HTML files using BeautifulSoup.
- **N-Gram Generation**: Forms candidate keyword phrases of lengths 1 to 3.
- **Feature Extraction**:
  - **Casing Feature**: Checks for capitalized words.
  - **Word Position**: Rewards words appearing early in the document.
  - **Word Frequency**: Counts the occurrences of a word.
  - **Word Relatedness**: Analyzes co-occurrences in a windowed context.
  - **Context Dispersion**: Measures how widely a keyword is spread across the document.
- **Scoring & Ranking**: Uses a weighted sum of extracted features to score candidates.
- **Pickle File Loading**: Loads preprocessed tokens for comparison and evaluation.
- **Customizable N-gram Length**: Users can specify the maximum n-gram length for keyword extraction.
- **Robust Error Handling**: Ensures smooth execution by handling missing files and invalid inputs gracefully.

## Installation

To set up the project, install the required dependencies:

```bash
pip install -r requiremenzs.txt
```

Ensure that you download the necessary NLTK resources:

```python
import nltk
nltk.download('stopwords')
```

## Usage

1. **Prepare Input Files**:

   - Place an HTML document in the designated directory.
   - A pickle file containing chapter tokens (if available) can be used for comparison.

2. **Run the Script**:

   ```bash
   python inference.py
   ```

3. **Output**:

   - Extracted keywords ranked by score.
   - Tokens from both HTML and the stored pickle file.
   - Top keyword candidates along with their calculated scores.

## Example Output

```
Sample HTML Tokens: ['adventure', 'mystery', 'exploration', ...]
Top 15 Scored Candidates: [('mystery adventure', 2.5), ('great exploration', 2.3), ...]
Top 15 Ranked Keywords: [('adventure', 10), ('mystery', 8), ...]
```

## Future Improvements

- **Enhancing Context Awareness**: Using word embeddings to better capture relationships.
- **Optimization**: Implementing parallel processing for large documents.
- **GUI Integration**: Creating a user-friendly interface for non-programmers.
- **Automated Stopword Filtering**: Expanding the stopword list dynamically based on document frequency.
- **Multi-language Support**: Extending keyword extraction to non-English texts.
- **Integration with Machine Learning**: Using trained models to refine keyword ranking.

## License

This project is licensed under the MIT License.

