from dotenv import load_dotenv
import os

from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma

# Load API key
load_dotenv()
api_key = os.getenv("ANTHROPIC_API_KEY")
if not api_key:
    raise ValueError("Missing ANTHROPIC_API_KEY . ")

# LLM
llm = ChatAnthropic(model="claude-haiku-5-5")

# Load document
with open("doc.txt", "r", encoding="utf-8") as f:
    text = f.read()

# Split into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)
chunks = text_splitter.split_text(text)

# Embeddings + Vector Store
# Anthropic has no embeddings API, so Chroma's built-in default local
# embedding model (all-MiniLM-L6-v2) is used instead — the handout's fallback.
vectorstore = Chroma.from_texts(chunks, collection_name="doc_qa")
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

# QA Prompt
qa_prompt = ChatPromptTemplate.from_template("""
You are a helpful assistant answering questions ONLY from the document.

If the answer is not found in the context, reply:
"I don't know based on this document."

Always end each answer with the line:
(derived from the provided text)

Context:
{context}

Question: {question}

Answer:
""")

def answer_question(question: str) -> str:
    docs = retriever.invoke(question)
    context = "\n\n".join(d.page_content for d in docs)

    print("Source Snippet:", docs[0].page_content[:120])

    chain = qa_prompt | llm
    response = chain.invoke({
        "context": context,
        "question": question
    })

    # Newer Claude models may return content as a list of blocks
    # (e.g. "thinking" + "text"); keep only the answer text.
    content = response.content
    if isinstance(content, list):
        content = "\n".join(
            block["text"] for block in content if block.get("type") == "text"
        )
    return content

if __name__ == "__main__":
    print("Claude Document Q&A — type 'exit' to stop.\n")

    while True:
        q = input("Your question: ")
        if q.lower() in ["exit", "quit"]:
            break

        ans = answer_question(q)
        print("\nAnswer:", ans, "\n")
