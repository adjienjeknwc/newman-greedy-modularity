# Newman's Greedy Modularity Optimization: Complete Course Submission

**Student Project Submission & Evaluation Package**  
**Topic:** Agglomerative Community Detection (Newman 2004) & Clauset–Newman–Moore Speedup  

---

## Evaluation Mapping Guide for Teacher

Your submission is organized strictly according to your teacher's three evaluation criteria:

```text
newman_modularity/
│
├── 1_implementation/              <--- EVALUATION CRITERION (A): Programming Platform
│   ├── newman_modularity.py       # Core from-scratch algorithm using e and a updates
│   ├── run_experiments.py        # Complete validation on Toy Graph & Karate Club + plot generator
│   └── demo.py                    # Fast 3-second live execution script for teacher evaluation
│
├── 2_presentation/                <--- EVALUATION CRITERION (B): Class Presentation
│   ├── presentation.html          # Interactive, browser-based full-screen slide deck
│   ├── speaker_presentation_script.md # Slide-by-slide spoken script with timings (7-10 min)
│   └── images/                    # High-resolution plots embedded in presentation
│       ├── toy_graph_modularity.png
│       ├── karate_modularity.png
│       └── network_communities_visualization.png
│
├── 3_question_answers/            <--- EVALUATION CRITERION (C): Q&A / Viva Voce Defense
│   └── viva_questions_and_answers.md # 15 high-scoring viva questions, derivations & trap answers
│
├── plots/                         # Master copy of high-resolution plots
│   ├── toy_graph_modularity.png
│   ├── karate_modularity.png
│   └── network_communities_visualization.png
│
└── README.md                      # This master submission index
```

---

## 1-Minute Quick Start Guide

### For Criterion (a): Live Implementation Demo
Run the live demo script from the terminal:
```bash
python 1_implementation/demo.py
```
*Expected Output:*
- 6-Node Toy Graph: Peak $Q = 0.35714$ at Step 4, partition `[[0, 1, 2], [3, 4, 5]]` (100% match with NetworkX).
- Zachary's Karate Club: Peak $Q = 0.38067$ at Step 31, 3 communities of size 8, 9, and 17 (100% match with NetworkX).

### For Criterion (b): Class Presentation
1. Double-click or open `2_presentation/presentation.html` in Google Chrome or Safari.
2. Press **`F`** for Full-Screen mode.
3. Use the **Right Arrow** / **Left Arrow** to change slides.
4. Read along with the speaker cues at the bottom of each slide or follow `2_presentation/speaker_presentation_script.md`.

### For Criterion (c): Q&A / Viva Voce
Open `3_question_answers/viva_questions_and_answers.md` to review the 15 questions and answers covering:
- The exact derivation of $\Delta Q = 2(e_{ij} - a_i a_j)$.
- Why disconnected pairs have $\Delta Q < 0$.
- Why initial $Q_0 < 0$ and final $Q = 0$.
- Clauset–Newman–Moore's heap data structures and $O(n \log^2 n)$ speedup.
- The Fortunato–Barthélemy resolution limit.
