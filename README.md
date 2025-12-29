# Work in Progress

# 💰 Financial Chatbot - README

## 📌 Project Overview
The **Financial Chatbot** is an AI-powered chatbot designed to **answer financial queries** by leveraging:
- **FAISS (Facebook AI Similarity Search)** for unstructured text retrieval (PDFs, CSVs, PPTX)
- **Neo4j Graph Database** for structured data search (financial transactions, tax rates, etc.)
- **Tesseract OCR** to extract text from images in PowerPoint slides
- **Flask API** for backend processing
- **HTML, CSS, JavaScript Frontend** for a simple user interface

---

## 🚀 Features
- 🔍 **Semantic Search**: Uses FAISS to retrieve the most relevant financial data
- 📊 **Structured Querying**: Neo4j graph database for tax & financial lookups
- 🌐 **Web UI**: Simple HTML + JavaScript frontend for user interaction

---

## 🔧 Setup neo4j
#### Install:
```
brew install neo4j
```
#### Start the server:
```
neo4j start
```
###### Note: Update neo4j username and password in code. Currently we are using default creds 

---
## 🔧 Installation & Setup
### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/yourusername/financial-chatbot.git
cd financial-chatbot
```

### **2️⃣ Install Dependencies**
```bash
pip install -r requirements.txt
```

### **3️⃣ Install Tesseract OCR**
```bash
brew install tesseract
```

### **4️⃣ Start the Flask Backend**
```bash
python app.py
```

### **5️⃣ Start the Web UI**
#### **Option 1: Open in Browser**
Visit: [http://127.0.0.1:5000](http://127.0.0.1:5000)

#### **Option 2: Run Streamlit UI**
```bash
streamlit run chatbot_ui.py
```

### Demo:
#### Command Line:
```
curl -X POST http://127.0.0.1:5000/api/chat -H "Content-Type: application/json" -d '{"query": "what is the tax rate for CA ?"}'
{
  "response": [
    {
      "document_index": 1,
      "score": 1.2849109172821045,
      "text": "TITLE 26\u2014INTERNAL REVENUE CODE\nACT AUG. 16, 1954, CH. 736, 68A STAT. 3\nThe following tables have been prepared as aids in comparing provisions of the Internal Revenue Code of\n1954 (redesignated the Internal Revenue Code of 1986 by Pub. L. 99\u2013514, \u00a72, Oct. 22, 1986, 100 Stat. 2095)\nwith provisions of"
    },
    {
      "document_index": "neo4j_result",
      "score": 1.0,
      "text": "Tax rate in CA for 2023: 0.2360348412354693"
    },
    {
      "document_index": 1611,
      "score": 0.5556479096412659,
      "text": "For the tax year 2023, a Individual in CA earned $726,621.05 from Capital Gains, with deductions of $147,002.83 under Business Expenses. The taxable income was $579,618.22 at a tax rate of 21.50%, resulting in $124,631.94 in taxes owed."
    }
  ]
}
```

#### UI:
![alt text](<Screenshot 2025-02-11 at 4.53.41 PM.png>)


