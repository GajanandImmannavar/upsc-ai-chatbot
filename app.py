import streamlit as st
import wikipedia
import difflib
import re
from wikipedia.exceptions import DisambiguationError, PageError

wikipedia.set_lang("en")

# ------------------ TEXT CLEANING ------------------

def clean_content(content):
    content = re.sub(r"\n{3,}", "\n\n", content)
    return content.strip()


def get_sections(content, max_sections=4):
    sections = re.split(r"\n==\s*(.*?)\s*==\n", content)
    result = []

    intro = sections[0].strip()
    if intro:
        result.append(("Introduction", intro))

    for i in range(1, len(sections), 2):
        heading = sections[i].strip()
        text = sections[i + 1].strip()
        if text:
            result.append((heading, text))
        if len(result) >= max_sections + 1:
            break

    return result


# ------------------ UPSC-AWARE SEARCH BOOSTING ------------------

def boost_indian_context(results, query):
    indian_keywords = [
        "india", "indian", "constitution", "article",
        "freedom", "movement", "dynasty",
        "ancient", "medieval", "modern",
        "ncert", "parliament", "supreme court",
        "emergency", "president", "prime minister"
    ]

    boosted = []
    for r in results:
        score = 0
        for kw in indian_keywords:
            if kw in r.lower():
                score += 1
        boosted.append((score, r))

    boosted.sort(reverse=True)
    return [r for _, r in boosted]


def best_match(query, results):
    matches = difflib.get_close_matches(query, results, n=1, cutoff=0.4)
    return matches[0] if matches else None


# ------------------ SUBJECT DETECTION ------------------

def detect_subject(title):
    polity = [
        "article", "constitution", "amendment",
        "parliament", "emergency", "president",
        "supreme court"
    ]
    history = [
        "revolt", "freedom", "movement",
        "dynasty", "rayanna", "chennamma",
        "harappa", "mohenjo"
    ]

    t = title.lower()
    if any(k in t for k in polity):
        return "Polity"
    if any(k in t for k in history):
        return "History"
    return "General"


# ------------------ REFERENCES ------------------

def get_references(subject, title):
    base_wiki = f"https://en.wikipedia.org/wiki/{title.replace(' ', '_')}"

    if subject == "Polity":
        return [
            ("Constitution of India – Ministry of Law & Justice",
             "https://legislative.gov.in/constitution-of-india/"),
            ("NCERT – Indian Constitution at Work (Class XI)",
             "https://ncert.nic.in/textbook.php?keps1=0-11"),
            ("Parliament of India",
             "https://www.parliamentofindia.nic.in/"),
            ("Wikipedia (Overview only)", base_wiki)
        ]

    if subject == "History":
        return [
            ("NCERT – Our Pasts (History)",
             "https://ncert.nic.in/textbook.php"),
            ("Ministry of Culture – Govt of India",
             "https://indianculture.gov.in/"),
            ("Wikipedia (Overview only)", base_wiki)
        ]

    return [
        ("NCERT Textbooks", "https://ncert.nic.in/textbook.php"),
        ("Wikipedia (Overview only)", base_wiki)
    ]


# ------------------ STREAMLIT UI ------------------

st.set_page_config(page_title="📘 UPSC Knowledge Assistant 🇮🇳", layout="wide")

st.title("📘 UPSC Knowledge Assistant 🇮🇳")
st.caption("NCERT • Wikipedia • Government Sources")

st.write("Ask any UPSC topic (Exact or approximate spelling and)")

if "results" not in st.session_state:
    st.session_state.results = []

question = st.text_input(
    "Enter your question:",
    placeholder="e.g., Article 360 / Olympic Games / Constitution of India / Geography of India"
)

# ------------------ SEARCH ------------------

if st.button("Search"):
    if question.strip():
        try:
            results = wikipedia.search(question, results=50)

            boosted = boost_indian_context(results, question)
            match = best_match(question, boosted)

            if match:
                boosted.remove(match)
                boosted.insert(0, match)

            st.session_state.results = boosted[:20]

        except Exception:
            st.error("Search failed. Try another keyword.")

# ------------------ DISPLAY OPTIONS ------------------

if st.session_state.results:
    st.subheader("🔍 Select the most relevant topic")

    choice = st.radio(
        "Options:",
        range(len(st.session_state.results)),
        format_func=lambda x: st.session_state.results[x]
    )

    if st.button("Get Answer"):
        title = st.session_state.results[choice]

        try:
            page = wikipedia.page(title, auto_suggest=False)

        except DisambiguationError as e:
            st.warning("This topic has multiple meanings. Choose one:")

            options = boost_indian_context(e.options, question)

            selected = st.radio("Possible meanings:", options)

            if st.button("Load Selected Topic"):
                page = wikipedia.page(selected, auto_suggest=False)
            else:
                st.stop()

        except PageError:
            st.error("Page not found.")
            st.stop()

        # ------------------ DISPLAY ANSWER ------------------

        content = clean_content(page.content)
        sections = get_sections(content)

        subject = detect_subject(page.title)
        references = get_references(subject, page.title)

        st.markdown(f"## 📘 {page.title}")

        for h, t in sections:
            st.markdown(f"### {h}")
            st.write(t)

        st.markdown("### 📝 UPSC USE")
        if subject == "Polity":
            st.markdown("""
            - **Prelims:** Articles, amendments, facts  
            - **Mains:** GS-II constitutional analysis  
            - **Interview:** Governance clarity
            """)
        elif subject == "History":
            st.markdown("""
            - **Prelims:** Chronology, personalities  
            - **Mains:** Freedom struggle & themes  
            - **Interview:** Historical significance
            """)
        else:
            st.markdown("""
            - **Prelims:** Core facts  
            - **Mains:** Conceptual clarity  
            - **Interview:** General awareness
            """)

        st.markdown("## 🔗 References")
        for name, link in references:
            st.markdown(f"- [{name}]({link})")
