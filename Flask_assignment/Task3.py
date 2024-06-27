from datasets import load_dataset
import re
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, Seq2SeqTrainer, Seq2SeqTrainingArguments, DataCollatorForSeq2Seq

# Load both parts of the dataset
document_dataset = load_dataset("ccdv/pubmed-summarization", "document")
section_dataset = load_dataset("ccdv/pubmed-summarization", "section")

# Load tokenizer
tokenizer = AutoTokenizer.from_pretrained("Falconsai/text_summarization")

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
        dataset[split] = dataset[split].map(lambda x: {
            'article': preprocess_text(x['article']),
            'abstract': preprocess_text(x['abstract'])
        })
    return dataset

# Preprocess both datasets
preprocessed_document_dataset = preprocess_dataset(document_dataset)
preprocessed_section_dataset = preprocess_dataset(section_dataset)

# Tokenize the datasets
def tokenize_function(examples):
    inputs = examples['article']
    targets = examples['abstract']
    model_inputs = tokenizer(inputs, max_length=1024, truncation=True)
    with tokenizer.as_target_tokenizer():
        labels = tokenizer(targets, max_length=150, truncation=True)
    model_inputs["labels"] = labels["input_ids"]
    return model_inputs

tokenized_document_dataset = preprocessed_document_dataset.map(tokenize_function, batched=True)
tokenized_section_dataset = preprocessed_section_dataset.map(tokenize_function, batched=True)

# Define training arguments
training_args = Seq2SeqTrainingArguments(
    output_dir="./results",
    evaluation_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    weight_decay=0.01,
    save_total_limit=3,
    num_train_epochs=3,
    predict_with_generate=True
)

# Load model
model = AutoModelForSeq2SeqLM.from_pretrained("Falconsai/text_summarization")

# Data collator
data_collator = DataCollatorForSeq2Seq(tokenizer, model=model)

# Initialize the Trainer
trainer = Seq2SeqTrainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_document_dataset['train'],
    eval_dataset=tokenized_document_dataset['validation'],
    data_collator=data_collator,
    tokenizer=tokenizer
)

# Train the model
trainer.train()

# Save the fine-tuned model
model.save_pretrained("./fine-tuned-model")
tokenizer.save_pretrained("./fine-tuned-model")
