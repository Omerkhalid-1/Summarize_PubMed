#                        PubMed Article Summarizer Web Application 
This web application allows users to input PubMed articles and receive summarized versions using a text summarization model. Additionally, users can sign up for accounts to access personalized features.
  Summarizes PubMed articles using a pre-trained Seq2Seq model from Hugging Face Transformers.
  Supports both extractive and abstractive summarization techniques.


## Task 1
Load the dataset pubmed-summarization from hugging face. [text]([url](https://huggingface.co/datasets/ccdv/pubmed-summarization?row=1))
Preprocess the dataset by changing the dataset into lowercase alphabets and removing the special characters.
Store some chunks of the original and summarized data in json files.

## Task 2 
Fine-tune the model according to the PubMed dataset. The model used was text_summarization
First the dataset was loaded using the following command
####           _ document_dataset = load_dataset("ccdv/pubmed-summarization", "document") _
####            _section_dataset = load_dataset("ccdv/pubmed-summarization", "section") _

Then the  tokenizer is loaded.
####                _tokenizer = AutoTokenizer.from_pretrained("Falconsai/text_summarization")_

AutoModelForSeq2SeqLM is used to fine tune the model.




##  Installation
#### 1. Clone the repository:
####                   _git clone https://github.com/OmerKhalid-1/Summarize_PubMed.git _
## cd Summarize_PubMed


### 2. Install dependencies:
Ensure you have Python 3 installed. Use pip (or pip3 for Python 3) to install packages:
####                      _pip install Flask transformers_

### 3. Download and run the application:
Navigate to the project directory and run the Flask application:
####                      _ python app.py _ 

All the Task are done using _Transforemers_ make sure to understand them before attempting using the repo.

##### Project Structure 
#### project-root/
#### │
#### ├── app.py             # Main Flask application file
#### ├── README.md          # This file, providing project documentation
#### ├── static/            # Static assets (CSS, JS, images)
#### └── templates/         # HTML templates for Flask
####   &nbsp;  ├── index.html     # Homepage template
####   &nbsp;  ├── login.html     # Login page template
####   &nbsp;  ├── signup.html    # Sign up page template
####   &nbsp;  ├── summary.html   # Summary page template
####     └── base.html      # Base template (shared header/footer)

