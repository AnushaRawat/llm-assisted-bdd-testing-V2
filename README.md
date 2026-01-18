# 🧪 LLM-Driven BDD Test Automation Pipeline

This project demonstrates an end-to-end automation pipeline that converts plain-English software requirements into executable BDD (Behavior-Driven Development) tests using a locally deployed, fine-tuned LLM and runs them automatically against a real web application.
<br/>
The goal is to reduce the manual effort involved in writing, reviewing, and executing BDD test cases while preserving human approval and deterministic execution.

---

## ✨ Key Capabilities
- Convert natural language requirements into valid Gherkin feature files
- Enforce positive (happy-path) and negative (failure) scenarios
- Human-in-the-loop approval before test execution
- Automatically execute approved BDD tests using pytest-bdd + Playwright
- Uses a locally hosted TinyLLaMA model fine-tuned with LoRA
- No external API calls or paid LLM services required

---
 
## 🏗️ High-Level Architecture
` ` `scss
requirements.txt
      ↓
LLM (TinyLLaMA + LoRA)
      ↓
Gherkin (.feature)
      ↓
User Approval
      ↓
Happy-Path Selection
      ↓
pytest-bdd + Playwright
      ↓
Automated UI Tests
` ` ` 

---

## Project Structure
```
sample_bdd_app/
│
├── app/ # Flask application
|
├── llm/
│   ├── generate_scenarios.py        # Generates Gherkin from requirements
│   ├── llm_client.py                # Loads TinyLLaMA + LoRA adapter
│   └── gherkin_lora/                # Trained LoRA adapter (lightweight)
│
├── tests/
│   ├── features/
│   │   └── user_authentication.feature
│   ├── steps/
│   │   └── auth_steps.py             # Step definitions (Playwright)
│   ├── run_happy_paths.py            # Test orchestration
│   └── test_runner.py                # pytest-bdd scenario loader
│
├── requirements.txt                  # Plain-English requirements
├── pytest.ini
├── README.md
├── run.py # Flask app entry point
└── requirements.txt

```
---

## 🔁 Execution Flow

1. User writes requirements in plain English
2. LLM generates Gherkin scenarios
3. User approves generated scenarios
4. Feature files are saved
5. Happy-path scenarios are automatically executed

---

## ▶️ Main Execution Commands

### 1️. Install dependencies
```bash
pip install -r requirements.txt
```
###  2. Start Flask App
```bash
python run.py
```
### 3. Generate Gherkin Scenario
```bash
python llm/generate_scenarios.py
```
### 4. Run automated BDD tests
```bash
python tests/run_happy_paths.py
```
---

## 🤖 LLM Details
- **Base Model**: TinyLLaMA-1.1B-Chat
- **Fine-tuning Method**: LoRA (Low-Rank Adaptation)
- **Training Objective**:
  - Always generate a `Feature`
  - Produce exactly one successful and one failed scenario
  - Output valid, executable Gherkin syntax

Only the **LoRA adapter weights** are stored in this repository.
The base model is loaded dynamically at runtime.

---

## 🧰 Tech Stack

### Backend Application
- **Python**
- **Flask** – sample web application under test

### LLM & ML
- **TinyLLaMA (1.1B)**
- **Hugging Face Transformers**
- **PEFT (LoRA)**
- **PyTorch**

### BDD & Test Automation
- **pytest**
- **pytest-bdd**
- **Playwright (Python)**

---

## 📄 License

This project is licensed under the MIT License.