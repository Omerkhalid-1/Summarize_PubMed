#                       ** PubMed Article Summarizer Web Application **
#### This web application allows users to input PubMed articles and receive summarized versions using a text summarization model. Additionally, users can sign up for accounts to access personalized features.
####  Summarizes PubMed articles using a pre-trained Seq2Seq model from Hugging Face Transformers.
####  Supports both extractive and abstractive summarization techniques.


## This project includes Task1 and Task3. The details about the tasks are mentioned below:
### Task 1
#### Load the dataset pubmed-summarization from hugging face. [text]([url](https://huggingface.co/datasets/ccdv/pubmed-summarization?row=1))
#### Preprocess the dataset by chaning the dataset into lowercase alphabets and removing the special characters.
#### Store some chunks of the original and summarized data in json files.

### Task 2 
#### Fine tune the model according to the PubMed dataset. The model used was text_summarization
#### First the dataset was loaded using the following command
###                  document_dataset = load_dataset("ccdv/pubmed-summarization", "document")
###                  section_dataset = load_dataset("ccdv/pubmed-summarization", "section")

#### Then the  tokenizer is loaded.
###                   tokenizer = AutoTokenizer.from_pretrained("Falconsai/text_summarization")

#### AutoModelForSeq2SeqLM is used to fine tune the model.




### Installation
#### 1.Clone the repository:
##                      git clone https://github.com/OmerKhalid-1/Summarize_PubMed.git 
## cd Summarize_PubMed


### 2. Install dependencies:
#### Ensure you have Python 3.x installed. Use pip (or pip3 for Python 3) to install required packages:
##                       pip install Flask transformers

### 3. Download and run the application:
#### Navigate to the project directory and run the Flask application:
##                       python app.py  

### All the 
