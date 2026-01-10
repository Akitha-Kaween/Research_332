
import json
import torch
from datasets import Dataset
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, Seq2SeqTrainingArguments, Seq2SeqTrainer, DataCollatorForSeq2Seq

# 1. Load Dataset
DATA_FILE = "sri_lanka_chat_data.json"
print(f"Loading dataset from {DATA_FILE}...")

with open(DATA_FILE, 'r') as f:
    raw_data = json.load(f)

# Convert to HuggingFace Dataset format
# Flan-T5 expects: "input_text" -> "target_text"
processed_data = []
for item in raw_data:
    processed_data.append({
        # INSTRUCTION TUNING WITH SYSTEM RULES
        # We inject the "Persona" and "Guidelines" directly into the input.
        # This teaches the model to behave according to these rules.
        "input_text": (
            "System: You are an expert Sri Lanka Travel Assistant. "
            "Guidelines: Be polite, factual, and strictly focused on Sri Lankan tourism. "
            "User: " + item["instruction"]
        ),
        "target_text": item["output"]
    })

dataset = Dataset.from_list(processed_data)
# Split
dataset = dataset.train_test_split(test_size=0.1)
print(f"Train size: {len(dataset['train'])}, Test size: {len(dataset['test'])}")

# 2. Model & Tokenizer
MODEL_NAME = "google/flan-t5-small"
print(f"Loading model: {MODEL_NAME}...")

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)

# 3. Preprocessing
def preprocess_function(examples):
    inputs = examples["input_text"]
    targets = examples["target_text"]
    
    model_inputs = tokenizer(inputs, max_length=128, truncation=True)
    labels = tokenizer(targets, max_length=128, truncation=True)
    
    model_inputs["labels"] = labels["input_ids"]
    return model_inputs

tokenized_datasets = dataset.map(preprocess_function, batched=True)

# 4. Training
print("Starting Fine-Tuning...")
training_args = Seq2SeqTrainingArguments(
    output_dir="./results",
    eval_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    weight_decay=0.01,
    save_total_limit=3,
    num_train_epochs=3, # Reduced for demo speed (increase for real research)
    predict_with_generate=True,
    logging_dir='./logs',
    logging_steps=100,
    report_to="none"  # Disable wandb
)

data_collator = DataCollatorForSeq2Seq(tokenizer, model=model)

trainer = Seq2SeqTrainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets["train"],
    eval_dataset=tokenized_datasets["test"],
    data_collator=data_collator,
    tokenizer=tokenizer,
)

trainer.train()

# 5. Save Model
SAVE_PATH = "./sri_lanka_flan_t5"
trainer.save_model(SAVE_PATH)
print(f"Model saved to {SAVE_PATH}")
