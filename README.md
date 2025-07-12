# 💱 Currency AI Agent

> A multimodal AI agent that converts currency amounts, generates visual representations — powered by **LangGraph, LangChain, Vertex AI, and Google Text-to-Image**.

---

## 🚀 Features

- 🔁 LLM-powered currency code extraction
- 📈 Real-time exchange rate API integration
- 🧠 Deterministic flow using LangGraph
- 🎨 Image generation (e.g., “Japanese currency”) via Imagen
- ⚡ FastAPI backend + Streamlit frontend

---
## ⚙️ Step 1: Add Your GCP Config

Edit the existing `config.yaml` with your GCP project info:

```yaml
project_id: "your-gcp-project-id"
location: "us-central1"
model_name: "gemini-2.5-flash"
image_model: "imagegeneration@002"
````

---

## 📦 Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🚀 Step 3: Run the Project

### ▶️ Start the FastAPI Backend

```bash
python3 api.py
```

API docs will be available at:
👉 **{api\_link}**

### 🎯 Optional: Launch Streamlit App

```bash
streamlit run streamlit_app.py
```

---

## 🔌 API Example

```bash
curl -X 'POST' \
  '{api_link}/convert' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
    "usd_amount": 100,
    "user_input": "Convert to Indian currency."
}'
```

### ✅ Example Output:

```json
{
  "usd_amount": 100,
  "total_usd": 108,
  "target_currency": "INR",
  "total_amount": 9271
}
```
### 🧠 Sample  Output Visual

![Graph Flow](images/indian_currency.png)

---

## 🔁 LangGraph Workflow

This app uses **LangGraph** to build a deterministic AI flow with the following structure:

1. `START`
2. 🧠 `decide_currency_node` → Gemini LLM identifies the target currency
3. 💵 `calc_total_node` → USD to intermediate amount
4. 🔁 `convert_currency_node` → Converts to final currency using live rates
7. `END`

---

## 📘 License

MIT © 2025 Hemanta Kumar
Built with LangGraph, Gemini, Imagen, and Google Cloud.

---