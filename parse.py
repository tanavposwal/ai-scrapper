from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

template = (
    "You are tasked with extracting, summarizing, and providing specific information from the given text content: {dom_content}. "
    "Please follow these instructions carefully:\n\n"
    "1. Extract the information that directly matches or closely aligns with the provided description: {parse_description}.\n"
    "2. If exact information is not available, provide details that are closely related to the description or inferred based on the context.\n"
    "3. Ensure the information is accurate, well-organized, and easy to understand.\n"
    "4. If possible, include additional insights or relevant details that add value to the extracted information.\n\n"
    "Output the result in the following format:\n"
    "- **Direct Match**: (if found)\n"
    "- **Related Information**: (if no exact match is found or additional context is needed)\n"
    "- **Summary**: (optional high-level overview, if applicable)\n"
)


model = OllamaLLM(model="llama3.2")


def parse_with_ollama(dom_chunks, parse_description):
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model

    parsed_results = []

    # print("Parsing contents with ai...")
    for i, chunks in enumerate(dom_chunks, start=1):
        response = chain.invoke(
            {"dom_content": chunks, "parse_description": parse_description}
        )
        # print(f"Parsed batch {i} / {len(dom_chunks)}")
        parsed_results.append(response)
    # print("Parsing completed.")

    return "/n".join(parsed_results)
