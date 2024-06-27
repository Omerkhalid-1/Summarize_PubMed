from datasets import load_dataset
import re
import json

# Load the PubMed Summarization dataset from Hugging Face
dataset = load_dataset("ccdv/pubmed-summarization", "document")

# Function to preprocess text data
def preprocess_text(text):
    # Lowercase the text
    text = text.lower()
    # Remove special characters and digits
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    return text

# Function to apply preprocessing to the dataset
def preprocess_dataset(dataset):
    for split in dataset.keys():
        dataset[split] = dataset[split].map(lambda x: {'article': preprocess_text(x['article']),
                                                       'abstract': preprocess_text(x['abstract'])})
    return dataset

# Preprocess the dataset
preprocessed_dataset = preprocess_dataset(dataset)

# Function to save a subset of the dataset to a JSON file
def save_subset_to_json(dataset, file_name, num_examples=100):
    subset = {}
    for split in dataset.keys():
        subset[split] = {key: value[:num_examples] for key, value in dataset[split].to_dict().items()}
    with open(file_name, 'w') as f:
        json.dump(subset, f, indent=4)

# Save a subset of the original and preprocessed datasets
save_subset_to_json(dataset, 'subset_original_pubmed_dataset.json', num_examples=100)
save_subset_to_json(preprocessed_dataset, 'subset_preprocessed_pubmed_dataset.json', num_examples=100)

# Display the first few preprocessed samples from the dataset
print(preprocessed_dataset['train'][0])
