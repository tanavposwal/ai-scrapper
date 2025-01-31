import streamlit as st
from scrape import scrape_website, split_dom_content, clean_body, extract_body_content
from parse import parse_with_ollama

st.set_page_config(
    page_icon="✨",
    page_title="Scrap with AI",
    initial_sidebar_state="expanded",
)


def main():
    if "dom_content" not in st.session_state:
        st.session_state["dom_content"] = ""

    if "message" not in st.session_state:
        st.session_state["message"] = []

    with st.sidebar:
        st.write("""
        # **🔥✨ Scrap with AI**
        """)
        st.write("---")
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
        st.write("---")
        st.write("""
        **How to Use**
        1. **Enter a URL** to scrape.
        2. Click **Scrape** to extract text.
        3. View **AI-processed results** in markdown format.
        """)

    for message in st.session_state["message"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("what is up?"):
        st.session_state["message"].append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            dom_chunks = split_dom_content(st.session_state.dom_content)
            message = parse_with_ollama(dom_chunks, prompt)
            st.session_state["message"].append(
                {"role": "assistant", "content": message}
            )
            st.markdown(message)


if __name__ == "__main__":
    main()
