# UPSC AI Knowledge Assistant 🇮🇳

AI-powered chatbot for UPSC aspirants. Provides accurate, structured answers using **NCERT, Wikipedia (overview only), and Government sources**.

---

## Features
- Handles spelling mistakes automatically
- Suggests related and meaningful options
- Option-based response handling
- Supports Polity, History, and General subjects
- Provides UPSC-use guidance (Prelims, Mains, Interview)
- Shows structured content sections with references

---

## Tech Stack
- Python 3.8+  
- Streamlit (Frontend)  
- Wikipedia API & NCERT text files (Content)  
- TF-IDF & Difflib (Suggestions)  
- Regex (Content Cleaning)

---

## How to Run
1. Clone repo and navigate to project folder
2. (Optional) Create virtual environment:
   - Windows: `venv\Scripts\activate`
   - Linux/macOS: `source venv/bin/activate`
3. Install dependencies: `pip install -r requirements.txt`
4. Run: `streamlit run app.py`
5. Open: `http://localhost:8501`

---

## Example
**User Input:** `Article 360`  
**Bot Options:**  
1. Article 360 (Financial Emergency – India)  
2. Article 36 (DPSP)  
3. Emergency Provisions of Indian Constitution  

Selecting an option gives **topic-specific explanation with references**.

---

👨‍💻 Author: Gajanand Immannavar  
AI / ML & Full Stack Developer
