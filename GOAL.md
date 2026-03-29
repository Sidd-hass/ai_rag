# 🚀 Phase 3: Universal Ingestion (Multi-Format Support)

### 🎯 Goal

Move beyond PDFs to support a complete digital office environment.

---

## 🔹 Universal Parsing

* Replace **PyPDFLoader** with **Unstructured.io**
* Support multiple formats:

  * `.pdf`
  * `.docx`
  * `.doc`
  * `.html`
  * `.txt`
  * `.md`

---

## 🔹 Structured Data (Excel / CSV)

* Integrate:

  * **Pandas**
  * **OpenPyXL**
* Logic:

  * Convert rows into descriptive sentences
  * Preserve relationships between headers and values during vectorization

---

## 🔹 Vision & OCR

* Implement **Tesseract OCR** for scanned documents
* Use **Llama3-Vision (via Ollama)** for:

  * Image understanding (`.jpg`, `.png`)
  * Generating text descriptions before indexing

---

## 🔹 The Pipeline

### 1. Detection

* Automatically detect file type using extension

### 2. Specialized Extraction

* Branch logic based on file type

### 3. Unified Vectorization

* Normalize all outputs into a global FAISS index

---

# 🚀 Phase 4: Agentic Reasoning & Tool Use

### 🎯 Goal

Shift from a **"Passive Reader" → "Active Analyst"**

---

## 🔹 Self-Correction (Self-RAG)

* Agent evaluates its own response
* If incomplete:

  * Triggers refined second search automatically

---

## 🔹 Multi-Step Reasoning

* Handle complex queries like:

  * *"Compare 2023 vs 2025 roles"*
* Break into sub-tasks
* Combine into final answer

---

## 🔹
