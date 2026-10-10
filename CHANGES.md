# Deviation Notes — LangChain with Claude Lab

Student lab handout: *LangChain with Claude (Anthropic)*, Parts 1–5.
Environment: Windows 11, Python 3.12.0, created 10 Oct 2026.

These are the exact changes made to the lab code, why each was necessary, and the
evidence (error messages) that forced each change. Deviations from the handout are
**compatibility fixes only** — the only prompt change is the Part 4 mini-task that the
handout itself requires.

---

## Package versions installed

| Package | Version | Notes |
|---|---|---|
| langchain | 1.4.4 | Lab expected a 0.x-era version |
| langchain-core | 1.6.9 | |
| langchain-anthropic | 1.7.5 | |
| langchain-community | 0.4.2 | Not installed by the lab's pip command (see Change 3) |
| langchain-text-splitters | 1.1.3 | Not installed by the lab's pip command (see Change 3) |
| faiss-cpu | 1.15.1 | Installed successfully, but FAISS replaced by Chroma (Change 5) |
| chromadb | 1.5.9 | The handout's own fallback vector store |
| onnxruntime | 1.31.0 | Runs Chroma's local default embedding model |

The lab's `pip install langchain langchain-anthropic python-dotenv faiss-cpu tiktoken`
pulls the **latest** LangChain, which is now v1.x. The handout was written against the
older 0.x API, so four APIs used in the handout no longer exist.

---

## Change 1 — Model name (both `hello_claude.py` and `doc_qa_claude.py`)

**Lab code:**
```python
llm = ChatAnthropic(model="claude-3-haiku-20240307")
```

**New code:**
```python
llm = ChatAnthropic(model="claude-haiku-5-5")
```

**Reason:** The model `claude-3-haiku-20240307` has been retired by Anthropic. Running
the lab script produced:

```
anthropic.NotFoundError: Error code: 404 -
{'type': 'error', 'error': {'type': 'not_found_error',
'message': 'model: claude-3-haiku-20240307'}}
```

**Evidence the new model exists:** the models were listed directly from the Anthropic
API with the lab account's key (`client.models.list()`), which returned:

```
claude-haiku-5-5, claude-sonnet-5-5, claude-opus-5-5, claude-fable-5-1,
claude-opus-5, claude-sonnet-5, claude-fable-5, claude-opus-4-8,
claude-opus-4-7, claude-sonnet-4-6, claude-opus-4-6, claude-opus-4-5-20251101,
claude-haiku-4-5-20251001
```

`claude-haiku-5-5` was chosen because it is the closest equivalent to the lab's
intent (the smallest/cheapest Haiku model). The script was then re-run and answered
the guide question *"What is LangChain?"* successfully.

---

## Change 2 — Text splitter import path (`doc_qa_claude.py`)

**Lab code:**
```python
from langchain.text_splitter import RecursiveCharacterTextSplitter
```

**New code:**
```python
from langchain_text_splitters import RecursiveCharacterTextSplitter
```

**Reason:** Text splitters were moved out of the core `langchain` package into the
standalone `langchain-text-splitters` package. The old path no longer exists:

```
ModuleNotFoundError: No module named 'langchain.text_splitter'
```

The class name and usage (`RecursiveCharacterTextSplitter(chunk_size=500,
chunk_overlap=100)`) are unchanged.

---

## Change 3 — Two extra packages installed

**Lab command:**
```
pip install langchain langchain-anthropic python-dotenv faiss-cpu tiktoken
```

**Also installed:**
```
pip install langchain-text-splitters langchain-community
```

**Reason:** The lab script imports `from langchain_community.vectorstores import
FAISS`, but `langchain-community` is no longer pulled in automatically by the
`langchain` package (Change 2 explains why `langchain-text-splitters` is needed).
Without them:

```
ModuleNotFoundError: No module named 'langchain_community'
```

---

## Change 4 — Retriever API (`doc_qa_claude.py`)

**Lab code:**
```python
retriever = vectorstore.as_retriever()
...
docs = retriever.get_relevant_documents(question, k=3)
```

**New code:**
```python
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
...
docs = retriever.invoke(question)
```

**Reason:** `get_relevant_documents()` was deprecated and then removed from
`langchain-core` 1.x in favour of the standard `invoke()` interface (verified by
checking `BaseRetriever`, which no longer defines `get_relevant_documents`). The
`k=3` parameter is now passed through `search_kwargs` so retrieval behaviour is
identical to the lab (top 3 chunks).

---

## Change 5 — Replaced `AnthropicEmbeddings` with Chroma's default embeddings

**Lab code:**
```python
from langchain_anthropic import AnthropicEmbeddings
...
embeddings = AnthropicEmbeddings()
vectorstore = FAISS.from_texts(chunks, embedding=embeddings)
```

**New code:**
```python
from langchain_community.vectorstores import Chroma
...
vectorstore = Chroma.from_texts(chunks, collection_name="doc_qa")
```

**Install (the handout's own fallback command):**
```
pip install chromadb
```

**Reason:** Anthropic does not offer a text-embeddings API, so `AnthropicEmbeddings`
does not exist in `langchain-anthropic` — running the lab script failed with:

```
ImportError: cannot import name 'AnthropicEmbeddings' from 'langchain_anthropic'
```

The handout anticipates a vector-store fallback ("If FAISS fails to install, replace
with Chroma: `pip install chromadb`"), so **Chroma was used with its built-in default
local embedding model (all-MiniLM-L6-v2)** — no extra API key needed. The rest of the
lab logic (chunking with `RecursiveCharacterTextSplitter`, top-3 retrieval, QA prompt)
is unchanged. The downloaded model is cached at
`C:\Users\<user>\.cache\chroma\onnx_models\all-MiniLM-L6-v2\` (~79 MB, one time).

Note: a `DeprecationWarning` about `langchain-community` may appear; it is informational
(the package is being sunset) and does not affect the lab.

---

## Change 6 — Response content blocks (`doc_qa_claude.py`)

**Problem:** some answers printed raw API structures instead of the answer text:

```
Answer: [{'signature': '...', 'thinking': '', 'type': 'thinking'},
         {'text': 'The document is ...', 'type': 'text'}]
```

**New code:**
```python
content = response.content
if isinstance(content, list):
    content = "\n".join(
        block["text"] for block in content if block.get("type") == "text"
    )
return content
```

**Reason:** newer Claude models can return content as a **list of typed blocks**
(e.g. a `thinking` block followed by a `text` block) rather than a plain string. The
fix keeps only the `text` blocks, so students always see a clean answer.

---

## Change 7 — Lab mini-tasks implemented (`doc_qa_claude.py`)

Part 4 requires two modifications; both were added:

1. **Source snippet** — print the first 120 characters of the top retrieved chunk:
   ```python
   print("Source Snippet:", docs[0].page_content[:120])
   ```
2. **Prompt suffix** — the QA prompt now instructs Claude to end every answer with
   `(derived from the provided text)`.

---

## Files created (lab deliverables)

| File | Purpose | Status |
|---|---|---|
| `.env` | Stores `ANTHROPIC_API_KEY` (never committed/shared) | Created; real key added by student |
| `test_env.py` | Part 2 sanity check of the API key | Passes |
| `hello_claude.py` | Part 3 basic LangChain + Claude chain | Works (model changed, Change 1) |
| `doc.txt` | Part 4 sample document (Step 4.1: "any 1–3 page text") | Student's CS 450 AI syllabus |
| `doc_qa_claude.py` | Part 4 document Q&A + both mini-tasks | Works (Changes 2, 4, 5, 6, 7) |
| `Part4_Document_QA.md` | Part 4 worksheet — answered questions with Source Snippets | Completed from a live run |
| `Part5_Reflection.md` | Part 5 reflection + wrap-up checklist | Completed |
| `part4_run_output.txt` | Raw transcript of the Part 4 test run (evidence) | Saved |

No handout files were deleted or renamed; FAISS remains installed even though the
vector store was switched to Chroma.

---

## Verification results (what was actually tested)

| Test | Command | Result |
|---|---|---|
| Key loaded | `python test_env.py` | Prints key prefix — OK |
| Part 3 | `python hello_claude.py` → *"What is LangChain?"* | Correct answer returned after Change 1 |
| Part 4 build | import/compile of `doc_qa_claude.py` | OK after Changes 2–5 |
| Part 4 Q1 | *"What is the main idea of the document?"* | Answered from syllabus + Source Snippet printed |
| Part 4 Q2 | *"List 2 important points discussed."* | Weeks 11–13 topics + learning objectives |
| Part 4 Q3 | *"Who is the audience of the text?"* | Identified enrolled students; noted audience not explicit |
| Mini-task 2 | Every answer checked | All end with `(derived from the provided text)` |
| Grounding | *"What is the capital of France?"* | `I don't know based on this document.` — no hallucination |

---

## Final status

| Item | Status |
|---|---|
| Anthropic account + API key set up (Part 1) | Done |
| Environment configured (Part 2) | Done — venv + all packages installed |
| `test_env.py` sanity check | Passes |
| Part 3 `hello_claude.py` | Works with `claude-haiku-5-5` |
| Part 4 `doc_qa_claude.py` | Works — Chroma default embeddings (Change 5); all three questions answered correctly |
| Part 4 mini-tasks | Both implemented and verified |
| Part 4 worksheet | `Part4_Document_QA.md` |
| Part 5 reflection | `Part5_Reflection.md` |
| FAISS install | Succeeded; replaced by Chroma per handout fallback |
