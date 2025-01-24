import streamlit as st
from scrape import scrape_website, split_dom_content, clean_body, extract_body_content
from parse import parse_with_ollama

st.header("AI Web Scrapper", divider="rainbow")

st.sidebar.write("""
### **How to Use**
1. **Enter a URL** to scrape.
2. Click **Scrape** to extract text.
3. View **AI-processed results** in markdown format.
""")

st.logo(
    "./logo.png",
    link="https://streamlit.io/gallery",
    icon_image="./logo.png",
)

url = st.text_input("Enter the URL")
if st.button("Scrap"):
    st.write("Scraping...")
    result = scrape_website(url)
    body_content = extract_body_content(result)
    cleaned_content = clean_body(body_content)
    st.session_state.dom_content = cleaned_content
    with st.expander("View DOM Content"):
        st.text_area("DOM content", cleaned_content, height=300)
    st.toast("Site Scrapped", icon="🔥")

if "dom_content" in st.session_state:
    parse_description = st.text_area("Describe what you want to parse")

    if st.button("Parse Content"):
        if parse_description:
            dom_chunks = split_dom_content(st.session_state.dom_content)
            with st.spinner("AI parsing..."):
                parsed_results = parse_with_ollama(dom_chunks, parse_description)
                st.markdown(parsed_results)
