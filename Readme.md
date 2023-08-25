# LLM Training Data Editor

LLM Training Data Editor is a Streamlit-based web application that allows users to easily edit and visualize training data saved in a `.jsonl` format.

## Features

- Upload and preview `.jsonl` training data.
- Edit individual data points, both plain text and structured JSON content.
- Detects rows in JSON data and presents them in an editable table format.
- Saves changes back to the file or allows for download as a new `.jsonl` file.

## Installation & Usage

### Prerequisites

- Python 3.7 or newer
- pip

### Steps

1. Clone this repository:

```bash
git clone https://github.com/leonjvr/ai-training-editor.git
cd ai-training-editor
```

2. Install the required dependencies:

```bash
pip install streamlit json
```

3. Run the Streamlit application:

```bash
streamlit run app.py
```

_Note: Ensure your file is named `app.py` or replace `app.py` with your filename in the command._

4. Open the Streamlit app link in your browser, usually `http://localhost:8501`.

5. Use the uploader widget to upload your `.jsonl` file and start editing.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)
