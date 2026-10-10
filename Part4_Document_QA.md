# Part 4 — Document Q&A with Claude (Worksheet)

**Run:**
```
python doc_qa_claude.py
```

**Document used:** `doc.txt` — CS 450: Introduction to Artificial Intelligence course syllabus
**Model:** `claude-haiku-5-5` (the handout's `claude-3-haiku-20240307` was retired by Anthropic)
**Vector store:** Chroma with its default local embedding model (Anthropic has no embeddings API)

> Note: answers are generated live by Claude, so wording may vary slightly between runs.

---

## Question 1 — "What is the main idea of the document?"

**Source Snippet:**
```
--------------------------------------------------------------
3. REQUIRED AND RECOMMENDED MATERIALS
-------------------
```

**Answer:**

The document is a course outline for an artificial intelligence class. It lists the
required and recommended textbooks, the weekly schedule for the final weeks (natural
language processing and generative AI, then AI ethics, safety, and society, with final
project presentations), the comprehensive final exam, and several learning outcomes,
such as building machine learning models and discussing the ethical implications of AI.

(derived from the provided text)

---

## Question 2 — "List 2 important points discussed."

**Source Snippet:**
```
Week 11  Machine Learning Fundamentals
         Supervised learning, decision trees, regression,
         overfitting, c
```

**Answer:**

1. **Weeks 11–13 cover three AI topics:** machine learning fundamentals (supervised
   learning, decision trees, regression, overfitting, cross-validation), neural networks
   and deep learning (perceptrons, backpropagation, CNNs, optimization), and
   reinforcement learning (Q-learning, policy gradients, exploration vs. exploitation).

2. **Learning objectives include building and evaluating models and understanding AI's
   societal impact:** students should be able to build and evaluate supervised and
   unsupervised machine learning models, describe how neural networks and large language
   models work, and discuss the ethical, legal, and social implications of AI, including
   bias, privacy, safety, and accountability.

(derived from the provided text)

---

## Question 3 — "Who is the audience of the text?"

**Source Snippet:**
```
Week 14  Natural Language Processing and Generative AI
         Transformers, large language models, prompting,
```

**Answer:**

The document doesn't explicitly name its audience. However, its content is addressed to
students in the course, since it describes attendance expectations ("Students are
responsible for all material and announcements covered in class"), course schedule,
readings, final project presentations, and how projects are evaluated.

(derived from the provided text)

---

## Mini-tasks

### 1. Print the first 120 characters of the top retrieved chunk as "Source Snippet" — DONE

`doc_qa_claude.py:57`
```python
print("Source Snippet:", docs[0].page_content[:120])
```

The Source Snippet line printed above each answer shows the top retrieved chunk.

### 2. Modify the prompt so Claude ends each answer with "(derived from the provided text)" — DONE

`doc_qa_claude.py:42-43` (inside the QA prompt template)
```
Always end each answer with the line:
(derived from the provided text)
```

Every answer above ends with the required line.

---

## Extra check (grounding behavior)

Question not found in the document, e.g. *"What is the capital of France?"*:

> I don't know based on this document.
>
> (derived from the provided text)

This confirms Claude answers ONLY from the provided document, as the prompt requires.
