# 🧠 Cognitive Code Copilot

An AI-powered assistant built with Python and Streamlit that analyzes, refactors, documents, and tests code, featuring an interactive, code-aware chatbot to serve as your development partner.

---

### ✨ Live Demo
*[**Pro Tip:** Record a short GIF of your app in action and place it here. You can use a free tool like LICEcap or GIPHY Capture. A visual demo makes your project much more impressive.]*



---
## ## 🚀 Key Features

* **Multi-Style Code Refactoring:** Refactor Python code to improve **readability**, **conciseness**, or just add **documentation and type hints**.
* **AI-Powered Unit Test Generation:** Automatically generate `pytest` unit tests for the refactored code, ensuring correctness and saving development time.
* **Automated Code Analysis:** Get instant feedback on your code's **cyclomatic complexity** and potential security vulnerabilities using `bandit`.
* **Interactive Chat Copilot:** Have a conversation with a code-aware AI. Ask it to explain changes, make further modifications, or answer questions about your code.
* **Modern, Professional UI:** A clean, intuitive, and visually appealing interface built with Streamlit.

---
## ## 🛠️ Tech Stack

* **Backend:** Python, FastAPI
* **Frontend:** Streamlit
* **Core AI/ML:** Generative AI via Groq (Llama 3), Retrieval-Augmented Generation (RAG)
* **Code Analysis:** `radon`, `bandit`
* **Data Validation:** Pydantic
* **Key Libraries:** `requests`, `pandas`

---
## ## ⚙️ Setup and Installation

Follow these steps to get the project running on your local machine.

### ### 1. Clone the Repository
```bash
git clone [https://github.com/Namanraj-v/Cognitive-Code-Copilot.git](https://github.com/Namanraj-v/Cognitive-Code-Copilot.git)
cd Cognitive-Code-Copilot
```

### ### 2. Create and Activate a Virtual Environment
```bash
# For Windows
python -m venv venv
.\venv\Scripts\activate
```

### ### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### ### 4. Configure Environment Variables
Create a file named `.env` in the root of the project directory and add your Groq API key:
```
GROQ_API_KEY="YOUR_API_KEY_HERE"
```

---
## ## ▶️ How to Run

You need to run the backend and frontend servers in two separate terminals.

### ### Terminal 1: Start the Backend Server
```bash
# Make sure your virtual environment is active
uvicorn backend.main:app --reload
```
The API will be available at `http://127.0.0.1:8000`.

### ### Terminal 2: Start the Frontend App
```bash
# Make sure your virtual environment is active
streamlit run frontend/app.py
```
Open your browser and go to `http://localhost:8501` to use the application.

---
## ## 🔮 Future Improvements

* **VS Code Extension Integration:** Package the tool as an IDE extension for a seamless developer workflow.
* **Semantic Code Search:** Implement a natural language search to find code snippets within an entire repository.
* **Support for More Languages:** Extend the functionality beyond Python to languages like JavaScript or Java.

---
## ## 📄 License

This project is licensed under the MIT License. See the `LICENSE` file for details.
