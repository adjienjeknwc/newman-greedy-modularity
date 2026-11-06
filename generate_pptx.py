"""
PowerPoint Generator for Newman's Modularity Optimization Presentation
Creates a professional, clean 16:9 widescreen presentation.pptx with charts and speaker notes.
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# Initialize 16:9 widescreen presentation
prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

# Color Palette (Modern Academic Tech Theme)
NAVY_DARK = RGBColor(15, 23, 42)      # #0f172a
CARD_BG = RGBColor(30, 41, 59)        # #1e293b
ACCENT_BLUE = RGBColor(56, 189, 248)  # #38bdf8
ACCENT_PURPLE = RGBColor(168, 85, 247)# #a855f7
ACCENT_GOLD = RGBColor(245, 158, 11)  # #f59e0b
TEXT_WHITE = RGBColor(248, 250, 252)  # #f8fafc
TEXT_MUTED = RGBColor(148, 163, 184)  # #94a3b8
BORDER_COLOR = RGBColor(51, 65, 85)   # #334155
GREEN_SUCCESS = RGBColor(16, 185, 129)# #10b981

blank_layout = prs.slide_layouts[6]

def create_base_slide(title_text, category_badge="CLASS PRESENTATION"):
    slide = prs.slides.add_slide(blank_layout)
    
    # Background full-bleed
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg.fill.solid()
    bg.fill.fore_color.rgb = NAVY_DARK
    bg.line.color.rgb = NAVY_DARK
    
    # Header container
    header_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(1.1))
    tf = header_box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    
    # Badge
    p_badge = tf.paragraphs[0]
    p_badge.text = f"● {category_badge.upper()}"
    p_badge.font.size = Pt(11)
    p_badge.font.bold = True
    p_badge.font.color.rgb = ACCENT_PURPLE
    
    # Title
    p_title = tf.add_paragraph()
    p_title.text = title_text
    p_title.font.size = Pt(26)
    p_title.font.bold = True
    p_title.font.color.rgb = TEXT_WHITE
    p_title.space_before = Pt(4)
    
    return slide

def add_card(slide, left, top, width, height, bg_color=CARD_BG, border_color=BORDER_COLOR):
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
    card.fill.solid()
    card.fill.fore_color.rgb = bg_color
    card.line.color.rgb = border_color
    card.line.width = Pt(1.5)
    return card

# -------------------------------------------------------------
# SLIDE 1: TITLE SLIDE
# -------------------------------------------------------------
slide1 = prs.slides.add_slide(blank_layout)
bg1 = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
bg1.fill.solid()
bg1.fill.fore_color.rgb = NAVY_DARK
bg1.line.color.rgb = NAVY_DARK

# Card container
card1 = add_card(slide1, 1.2, 1.2, 10.933, 5.1)

tb1 = slide1.shapes.add_textbox(Inches(1.8), Inches(1.6), Inches(9.7), Inches(4.3))
tf1 = tb1.text_frame
tf1.word_wrap = True

p = tf1.paragraphs[0]
p.text = "ACADEMIC PROJECT EVALUATION & DEFENSE"
p.font.size = Pt(12)
p.font.bold = True
p.font.color.rgb = ACCENT_PURPLE

p = tf1.add_paragraph()
p.text = "Newman's Greedy Optimization of Modularity"
p.font.size = Pt(36)
p.font.bold = True
p.font.color.rgb = TEXT_WHITE
p.space_before = Pt(12)

p = tf1.add_paragraph()
p.text = "Agglomerative Community Detection (Newman 2004) & Clauset–Newman–Moore Speedup"
p.font.size = Pt(18)
p.font.color.rgb = ACCENT_BLUE
p.space_before = Pt(8)

p = tf1.add_paragraph()
p.text = "• Implementation from Scratch: ΔQ = 2(e_ij - a_i * a_j) with exact e and a updates\n• Validated on: 6-Node Bridge Toy Graph & Zachary's Karate Club Network\n• 100% Exact Verification with NetworkX reference library\n• Student Evaluation Criteria: (a) Implementation, (b) Presentation, (c) Q&A"
p.font.size = Pt(14)
p.font.color.rgb = TEXT_MUTED
p.space_before = Pt(24)

# Speaker Notes
slide1.notes_slide.notes_text_frame.text = (
    "Good morning Professor and classmates. Today I will present Newman's Greedy Modularity Optimization "
    "algorithm for community detection in networks, explaining how modularity is maximized agglomeratively, "
    "and how Clauset, Newman, and Moore later achieved near-linear scaling."
)

# -------------------------------------------------------------
# SLIDE 2: THE INTUITION (THE DINNER PARTY STORY)
# -------------------------------------------------------------
slide2 = create_base_slide("Core Intuition: What is Community Detection?", "The Big Picture")
add_card(slide2, 0.8, 1.7, 5.7, 5.2)
add_card(slide2, 6.8, 1.7, 5.7, 5.2)

# Left Column: The Problem
tb2_l = slide2.shapes.add_textbox(Inches(1.1), Inches(1.9), Inches(5.1), Inches(4.7))
tf2_l = tb2_l.text_frame
tf2_l.word_wrap = True

p = tf2_l.paragraphs[0]
p.text = "The Network Challenge"
p.font.size = Pt(18)
p.font.bold = True
p.font.color.rgb = ACCENT_BLUE

p = tf2_l.add_paragraph()
p.text = "Complex networks (social, biological, web) naturally organize into clusters called communities.\n\n• Communities have dense internal edges.\n• They have comparatively sparser connections to the rest of the network.\n\nKey Question: How can an algorithm automatically discover these groupings without being told the number of communities in advance?"
p.font.size = Pt(14)
p.font.color.rgb = TEXT_WHITE
p.space_before = Pt(14)

# Right Column: The Analogy
tb2_r = slide2.shapes.add_textbox(Inches(7.1), Inches(1.9), Inches(5.1), Inches(4.7))
tf2_r = tb2_r.text_frame
tf2_r.word_wrap = True

p = tf2_r.paragraphs[0]
p.text = "The 'Dinner Party' Analogy"
p.font.size = Pt(18)
p.font.bold = True
p.font.color.rgb = ACCENT_PURPLE

p = tf2_r.add_paragraph()
p.text = "Imagine a dinner party with 34 guests:\n\n1. At the start (Step 0): Everyone sits alone at 34 small tables.\n2. Modularity (Q): Measures the 'happiness' of the seating arrangement.\n3. The Greedy Choice: At each step, we merge the two tables whose union provides the biggest boost to party happiness (ΔQ).\n4. The Peak: For Karate Club, happiness peaks at Step 31 with 3 natural friend groups!\n5. The Collapse: If we force enemies/strangers together, happiness drops back to zero."
p.font.size = Pt(13)
p.font.color.rgb = TEXT_WHITE
p.space_before = Pt(12)

slide2.notes_slide.notes_text_frame.text = (
    "To understand the intuition before looking at the formulas: imagine 34 guests at a party. "
    "At step 0, everyone sits alone. Modularity measures how happy the room is when friends sit together. "
    "We greedily merge tables that give the biggest jump in happiness until the score peaks!"
)

# -------------------------------------------------------------
# SLIDE 3: DEFINING MODULARITY (Q)
# -------------------------------------------------------------
slide3 = create_base_slide("Mathematical Formulation: Modularity (Q)", "Theoretical Foundation")
add_card(slide3, 0.8, 1.7, 11.7, 5.2)

tb3 = slide3.shapes.add_textbox(Inches(1.2), Inches(1.9), Inches(10.9), Inches(4.7))
tf3 = tb3.text_frame
tf3.word_wrap = True

p = tf3.paragraphs[0]
p.text = "Modularity Formula (Newman & Girvan 2004)"
p.font.size = Pt(18)
p.font.bold = True
p.font.color.rgb = ACCENT_BLUE

p = tf3.add_paragraph()
p.text = "Q = Σ [ (L_c / m) - (k_c / 2m)² ]"
p.font.size = Pt(24)
p.font.bold = True
p.font.color.rgb = ACCENT_GOLD
p.space_before = Pt(12)

p = tf3.add_paragraph()
p.text = (
    "Where:\n"
    "  • m: Total number of edges in the network\n"
    "  • L_c: Number of internal edges inside community c\n"
    "  • k_c = Σ_{u ∈ c} k_u: Sum of degrees of all vertices in community c\n"
    "  • L_c / m: Actual fraction of edges inside community c\n"
    "  • (k_c / 2m)²: Expected fraction of edges in community c under random null model\n\n"
    "Interpretation of Modularity Q values:\n"
    "  • Range: -1/2 ≤ Q ≤ 1.0\n"
    "  • Q > 0: More internal edges than expected by chance (community structure exists)\n"
    "  • Q ∈ [0.3, 0.7]: Strong, genuine community cohesion in real-world networks\n"
    "  • Q ≤ 0: Edges are random noise or bipartite structure"
)
p.font.size = Pt(14)
p.font.color.rgb = TEXT_WHITE
p.space_before = Pt(14)

slide3.notes_slide.notes_text_frame.text = (
    "Modularity quantifies whether a partition has more internal connections than a random null model. "
    "A high Q means genuine community cohesion. Real-world networks typically peak between 0.3 and 0.7."
)

# -------------------------------------------------------------
# SLIDE 4: DERIVATION OF DELTA Q
# -------------------------------------------------------------
slide4 = create_base_slide("Derivation of ΔQ = 2(e_ij - a_i a_j)", "Mathematical Proof")
add_card(slide4, 0.8, 1.7, 11.7, 5.2)

tb4 = slide4.shapes.add_textbox(Inches(1.2), Inches(1.9), Inches(10.9), Inches(4.7))
tf4 = tb4.text_frame
tf4.word_wrap = True

p = tf4.paragraphs[0]
p.text = "Newman's Matrix Formulation and Merge Step Proof"
p.font.size = Pt(18)
p.font.bold = True
p.font.color.rgb = ACCENT_BLUE

p = tf4.add_paragraph()
p.text = (
    "1. Define e_ij = fraction of edges between community i and j (e_ii = internal edge fraction)\n"
    "2. Define a_i = Σ_j e_ij = k_i / (2m) (fraction of edge ends in community i)\n"
    "3. Total modularity is Q = Σ_c (e_cc - a_c²)\n\n"
    "When merging two communities i and j into a new merged community k = i ∪ j:\n"
    "  • New internal edges: e_kk = e_ii + e_jj + 2*e_ij\n"
    "  • New degree fraction: a_k = a_i + a_j\n"
    "  • New contribution: e_kk - a_k² = (e_ii + e_jj + 2*e_ij) - (a_i + a_j)²\n"
    "  • Expanding: e_ii + e_jj + 2*e_ij - a_i² - a_j² - 2*a_i*a_j\n"
    "  • Old contribution was: (e_ii - a_i²) + (e_jj - a_j²)\n\n"
    "Subtracting old from new yields:"
)
p.font.size = Pt(13)
p.font.color.rgb = TEXT_WHITE
p.space_before = Pt(8)

p = tf4.add_paragraph()
p.text = "ΔQ = 2(e_ij - a_i * a_j)"
p.font.size = Pt(22)
p.font.bold = True
p.font.color.rgb = ACCENT_GOLD
p.space_before = Pt(8)

p = tf4.add_paragraph()
p.text = "Critical Pruning Rule: If e_ij = 0 (no edge), ΔQ = -2*a_i*a_j ≤ 0. Therefore, the greedy algorithm ONLY needs to check connected pairs!"
p.font.size = Pt(13)
p.font.bold = True
p.font.color.rgb = ACCENT_BLUE
p.space_before = Pt(8)

slide4.notes_slide.notes_text_frame.text = (
    "Notice that when two communities share no edges, e_ij is 0, making delta Q strictly negative. "
    "This mathematically proves why we only evaluate connected pairs, saving tremendous compute time."
)

# -------------------------------------------------------------
# SLIDE 5: NEWMAN ALGORITHM WORKFLOW
# -------------------------------------------------------------
slide5 = create_base_slide("The Greedy Agglomerative Algorithm", "Implementation Details")
add_card(slide5, 0.8, 1.7, 7.5, 5.2)
add_card(slide5, 8.6, 1.7, 3.9, 5.2)

tb5_l = slide5.shapes.add_textbox(Inches(1.1), Inches(1.9), Inches(6.9), Inches(4.7))
tf5_l = tb5_l.text_frame
tf5_l.word_wrap = True

p = tf5_l.paragraphs[0]
p.text = "Step-by-Step Execution Workflow"
p.font.size = Pt(18)
p.font.bold = True
p.font.color.rgb = ACCENT_BLUE

p = tf5_l.add_paragraph()
p.text = (
    "1. Initialization (Step 0):\n"
    "   • Every node is its own community (n active communities).\n"
    "   • e_ij = A_ij / (2m), e_ii = 0, a_i = k_i / (2m).\n"
    "   • Initial modularity Q_0 = - Σ (a_i²) < 0.\n\n"
    "2. Candidate Selection:\n"
    "   • Evaluate ΔQ = 2(e_ij - a_i*a_j) for all active connected pairs.\n"
    "   • Pick the pair (i*, j*) that maximizes ΔQ.\n\n"
    "3. Fast Matrix Updates (O(n) time):\n"
    "   • Internal edges: e_ii ← e_ii + e_jj + 2*e_ij\n"
    "   • Neighbor edges: e_ik ← e_ik + e_jk  (for all k ≠ i, j)\n"
    "   • Degree fraction: a_i ← a_i + a_j\n"
    "   • Community j is removed; Q ← Q + ΔQ.\n\n"
    "4. Build Dendrogram:\n"
    "   • Repeat for n-1 merges until 1 community remains (Q_final = 0).\n"
    "   • Cut dendrogram at the step achieving peak modularity Q*."
)
p.font.size = Pt(13)
p.font.color.rgb = TEXT_WHITE
p.space_before = Pt(10)

tb5_r = slide5.shapes.add_textbox(Inches(8.9), Inches(1.9), Inches(3.3), Inches(4.7))
tf5_r = tb5_r.text_frame
tf5_r.word_wrap = True

p = tf5_r.paragraphs[0]
p.text = "Complexity Analysis"
p.font.size = Pt(18)
p.font.bold = True
p.font.color.rgb = ACCENT_PURPLE

p = tf5_r.add_paragraph()
p.text = (
    "Newman (2004):\n\n"
    "• Number of merges: n - 1\n"
    "• Max ΔQ scan: O(m)\n"
    "• Matrix updates: O(n)\n\n"
    "Total Time Complexity:\n"
    "O((m + n) n)\n"
    "≈ O(n²) on sparse graphs\n\n"
    "Space Complexity:\n"
    "O(n²) matrix e\n\n"
    "Feasible for:\n"
    "Networks up to ~10,000 vertices."
)
p.font.size = Pt(13)
p.font.color.rgb = TEXT_MUTED
p.space_before = Pt(14)

slide5.notes_slide.notes_text_frame.text = (
    "The algorithm builds a complete agglomerative tree. At each step, we update the e matrix and a vector "
    "in O(n) time. Total runtime is O(n^2), which works well for networks up to 10,000 nodes."
)

# -------------------------------------------------------------
# SLIDE 6: BENCHMARK 1 - 6-NODE TOY GRAPH
# -------------------------------------------------------------
slide6 = create_base_slide("Benchmark 1: 6-Node Toy Graph (Two Triangles + Bridge)", "Experimental Validation")
add_card(slide6, 0.8, 1.7, 5.7, 5.2)
add_card(slide6, 6.8, 1.7, 5.7, 5.2)

tb6 = slide6.shapes.add_textbox(Inches(1.1), Inches(1.9), Inches(5.1), Inches(4.7))
tf6 = tb6.text_frame
tf6.word_wrap = True

p = tf6.paragraphs[0]
p.text = "6-Node Toy Graph Results"
p.font.size = Pt(18)
p.font.bold = True
p.font.color.rgb = ACCENT_BLUE

p = tf6.add_paragraph()
p.text = (
    "Structure: Triangle 1 {0,1,2}, Bridge (2,3), Triangle 2 {3,4,5}\n"
    "Nodes: 6, Edges: 7\n\n"
    "Step 0: Initial state | Q = -0.1735 (6 comms)\n"
    "Step 1: Merge [0] + [1] | ΔQ = +0.1020, Q = -0.0714\n"
    "Step 2: Merge [0,1] + [2] | ΔQ = +0.1633, Q = +0.0918\n"
    "Step 3: Merge [4] + [5] | ΔQ = +0.1020, Q = +0.1939\n"
    "Step 4: Merge [3] + [4,5] | ΔQ = +0.1633, Q = +0.3571 ★\n"
    "Step 5: Merge [0,1,2] + [3,4,5] | ΔQ = -0.3571, Q = 0.0000\n\n"
    "Optimal Peak Q*: 0.35714 (achieved at Step 4)\n"
    "Optimal Partition: 2 communities [[0, 1, 2], [3, 4, 5]]\n\n"
    "NetworkX Match: EXACT (100% agreement)"
)
p.font.size = Pt(12)
p.font.color.rgb = TEXT_WHITE
p.space_before = Pt(8)

# Add plot image
plot_toy_path = "/Users/aditi/Desktop/newman_modularity/plots/toy_graph_modularity.png"
if os.path.exists(plot_toy_path):
    slide6.shapes.add_picture(plot_toy_path, Inches(7.0), Inches(2.0), width=Inches(5.3))

slide6.notes_slide.notes_text_frame.text = (
    "On the 6-node toy graph, the curve peaks at step 4 where the two triangles are separated. "
    "When step 5 merges across the bridge, Q drops abruptly back to 0."
)

# -------------------------------------------------------------
# SLIDE 7: BENCHMARK 2 - ZACHARY'S KARATE CLUB
# -------------------------------------------------------------
slide7 = create_base_slide("Benchmark 2: Zachary's Karate Club (34 Nodes, 78 Edges)", "Experimental Validation")
add_card(slide7, 0.8, 1.7, 5.7, 5.2)
add_card(slide7, 6.8, 1.7, 5.7, 5.2)

tb7 = slide7.shapes.add_textbox(Inches(1.1), Inches(1.9), Inches(5.1), Inches(4.7))
tf7 = tb7.text_frame
tf7.word_wrap = True

p = tf7.paragraphs[0]
p.text = "Karate Club Results (Newman 2004)"
p.font.size = Pt(18)
p.font.bold = True
p.font.color.rgb = ACCENT_BLUE

p = tf7.add_paragraph()
p.text = (
    "Wayne Zachary (1977) Karate Club Network:\n"
    "• Nodes: 34 members, Edges: 78 friendships\n\n"
    "Key Merge Milestones:\n"
    "• Step 0: Q_0 = -0.04980 (34 individual communities)\n"
    "• Steps 1–30: Consistent ΔQ > 0 growth as cliques form\n"
    "• Step 31: GLOBAL PEAK Q* = 0.38067 (3 Communities) ★\n"
    "• Step 32: Faction merge causes ΔQ = -0.0089, Q drops to 0.3718\n"
    "• Step 33: Single group yields Q = 0.0000\n\n"
    "Final 3 Detected Communities at Peak Q = 0.3807:\n"
    "  1. Officer Faction (17 nodes): [8, 14, 15, 18, 20, 22–33]\n"
    "  2. Mr. Hi Inner Core (9 nodes): [1, 2, 3, 7, 9, 12, 13, 17, 21]\n"
    "  3. Mr. Hi Outer Circle (8 nodes): [0, 4, 5, 6, 10, 11, 16, 19]"
)
p.font.size = Pt(12)
p.font.color.rgb = TEXT_WHITE
p.space_before = Pt(8)

# Add plot image
plot_karate_path = "/Users/aditi/Desktop/newman_modularity/plots/karate_modularity.png"
if os.path.exists(plot_karate_path):
    slide7.shapes.add_picture(plot_karate_path, Inches(7.0), Inches(2.0), width=Inches(5.3))

slide7.notes_slide.notes_text_frame.text = (
    "For Zachary's Karate Club, Q rises steadily through 31 merges, reaching a maximum of 0.38067 with 3 communities. "
    "This exactly reproduces Newman's 2004 published findings and matches NetworkX to all decimal places."
)

# -------------------------------------------------------------
# SLIDE 8: VISUAL NETWORK PARTITIONS
# -------------------------------------------------------------
slide8 = create_base_slide("Network Community Partitions Visualized", "Visual Verification")
add_card(slide8, 0.8, 1.7, 11.7, 5.2)

plot_net_path = "/Users/aditi/Desktop/newman_modularity/plots/network_communities_visualization.png"
if os.path.exists(plot_net_path):
    slide8.shapes.add_picture(plot_net_path, Inches(1.1), Inches(1.9), width=Inches(11.1))

slide8.notes_slide.notes_text_frame.text = (
    "Here we visualize the detected partitions. On the left, the toy graph splits cleanly across the bridge. "
    "On the right, Karate Club reveals 3 distinct clusters where internal edge density is maximized."
)

# -------------------------------------------------------------
# SLIDE 9: COMPARISON WITH NETWORKX
# -------------------------------------------------------------
slide9 = create_base_slide("Comparison with NetworkX greedy_modularity_communities", "Benchmarking")
add_card(slide9, 0.8, 1.7, 11.7, 5.2)

tb9 = slide9.shapes.add_textbox(Inches(1.2), Inches(1.9), Inches(10.9), Inches(4.7))
tf9 = tb9.text_frame
tf9.word_wrap = True

p = tf9.paragraphs[0]
p.text = "Side-by-Side Verification Table"
p.font.size = Pt(18)
p.font.bold = True
p.font.color.rgb = ACCENT_BLUE

p = tf9.add_paragraph()
p.text = (
    "------------------------------------------------------------------------------------------------------------------------\n"
    "Benchmark / Metric                 Our From-Scratch Algorithm        NetworkX Library                    Verification Status\n"
    "------------------------------------------------------------------------------------------------------------------------\n"
    "Toy Graph Partition                [[0, 1, 2], [3, 4, 5]]            [[0, 1, 2], [3, 4, 5]]              100% EXACT MATCH\n"
    "Toy Graph Modularity Q             0.357142857                       0.357142857                         EXACT TO ALL DECIMALS\n"
    "Karate Club Partition              3 comms (8, 9, 17 members)        3 comms (8, 9, 17 members)          100% EXACT MATCH\n"
    "Karate Club Q (Unweighted)         0.380670611                       0.380670611                         EXACT TO ALL DECIMALS\n"
    "Karate Club Q (Weighted)           Supported                         0.434521467                         Consistent\n"
    "Time Complexity                    O(n²)                             O(n log² n) (CNM speedup)           CNM uses heaps\n"
    "------------------------------------------------------------------------------------------------------------------------\n\n"
    "Crucial Distinction on Edge Weights:\n"
    "• NetworkX's karate_club_graph() includes edge weights from Zachary's field notes by default.\n"
    "• When evaluated with weight=None (the unweighted canonical Newman 2004 benchmark), NetworkX produces\n"
    "  the exact same partition and Q = 0.38067 as our scratch implementation down to all decimal digits!"
)
p.font.size = Pt(12)
p.font.color.rgb = TEXT_WHITE
p.space_before = Pt(8)

slide9.notes_slide.notes_text_frame.text = (
    "Both the toy graph and the Karate club partitions match NetworkX's greedy_modularity_communities with 100% precision. "
    "Notice the nuance on edge weights: unweighted gives 0.3807, while weighted gives 0.4345."
)

# -------------------------------------------------------------
# SLIDE 10: CLASET-NEWMAN-MOORE (CNM 2004) SPEEDUP
# -------------------------------------------------------------
slide10 = create_base_slide("The Clauset–Newman–Moore (CNM 2004) Speedup", "Algorithm Optimization")
add_card(slide10, 0.8, 1.7, 11.7, 5.2)

tb10 = slide10.shapes.add_textbox(Inches(1.2), Inches(1.9), Inches(10.9), Inches(4.7))
tf10 = tb10.text_frame
tf10.word_wrap = True

p = tf10.paragraphs[0]
p.text = "Scaling from O(n²) to O(n log² n) Using Max-Heaps"
p.font.size = Pt(18)
p.font.bold = True
p.font.color.rgb = ACCENT_PURPLE

p = tf10.add_paragraph()
p.text = (
    "Newman's 2004 bottleneck: Scanning all edges each step takes O(m) time, totaling O((m+n)n) ≈ O(n²).\n"
    "Aaron Clauset, Mark Newman, and Cristopher Moore (2004) introduced three specialized data structures:\n\n"
    "1. Sparse ΔQ Matrix: Only stores ΔQ_ij values for adjacent communities.\n"
    "2. Per-Community Max-Heaps: Each community i maintains a max-heap of its neighbor ΔQ values and stores row max M_i.\n"
    "3. Global Max-Heap: Stores row maximums {M_i} for all communities.\n"
    "   → Finding the global best pair (i, j) now takes O(1) time!\n\n"
    "Direct ΔQ Update Equations (no matrix recalculation):\n"
    "  • Common neighbor k connected to both i and j:   ΔQ'_jk = ΔQ_jk + ΔQ_ik\n"
    "  • Neighbor k connected to i only:                 ΔQ'_jk = ΔQ_ik - 2*a_j*a_k\n"
    "  • Neighbor k connected to j only:                 ΔQ'_jk = ΔQ_jk - 2*a_i*a_k\n"
    "  • Heap updates take O(log n) per neighbor.\n\n"
    "Outcome: Total time drops to O(m * d * log n) ≈ O(n log² n). Enabled networks of millions of nodes!"
)
p.font.size = Pt(13)
p.font.color.rgb = TEXT_WHITE
p.space_before = Pt(8)

slide10.notes_slide.notes_text_frame.text = (
    "CNM replaces the exhaustive matrix search with max-heaps. The search becomes O(1) and updates become logarithmic, "
    "which allowed community detection to scale to millions of nodes."
)

# -------------------------------------------------------------
# SLIDE 11: CONCLUSION & VIVA SUMMARY
# -------------------------------------------------------------
slide11 = create_base_slide("Summary & Viva Defense Takeaways", "Conclusion & Q&A")
add_card(slide11, 0.8, 1.7, 11.7, 5.2)

tb11 = slide11.shapes.add_textbox(Inches(1.2), Inches(1.9), Inches(10.9), Inches(4.7))
tf11 = tb11.text_frame
tf11.word_wrap = True

p = tf11.paragraphs[0]
p.text = "Key Takeaways for Evaluation & Defense"
p.font.size = Pt(18)
p.font.bold = True
p.font.color.rgb = ACCENT_BLUE

p = tf11.add_paragraph()
p.text = (
    "1. Core Implementation: Successfully built Newman (2004) from first principles using e and a updates.\n"
    "2. Experimental Validation: 100% exact numerical match with NetworkX reference on Toy Graph and Karate Club.\n"
    "3. NP-Hardness: Modularity maximization is NP-hard (Brandes 2006); Newman's greedy approach is an effective heuristic.\n"
    "4. Resolution Limit: Fortunato & Barthélemy (2007) proved modularity cannot resolve communities smaller than ~(2m)^0.5.\n"
    "5. Scalability: CNM 2004 heap speedup brought modularity optimization to massive web-scale networks.\n\n"
    "Project Artifacts Created & Ready:\n"
    "  • Python source code: newman_modularity.py & demo.py\n"
    "  • Visual interactive tool: interactive_visualizer.html (with live auto-merge animation)\n"
    "  • Complete defense guide: viva_questions_and_answers.md (15 Q&As with full proofs)"
)
p.font.size = Pt(13)
p.font.color.rgb = TEXT_WHITE
p.space_before = Pt(10)

p = tf11.add_paragraph()
p.text = "Thank you! I am ready to answer any questions."
p.font.size = Pt(18)
p.font.bold = True
p.font.color.rgb = ACCENT_GOLD
p.space_before = Pt(16)
p.alignment = PP_ALIGN.CENTER

slide11.notes_slide.notes_text_frame.text = (
    "In conclusion, we have derived, implemented, validated, and visualized Newman's algorithm from first principles. "
    "Thank you, and I look forward to your questions."
)

# Save presentations
out_desktop_pptx = "/Users/aditi/Desktop/newman_modularity/presentation.pptx"
prs.save(out_desktop_pptx)

out_pres_pptx = "/Users/aditi/Desktop/newman_modularity/2_presentation/presentation.pptx"
prs.save(out_pres_pptx)

print(f"Saved PowerPoint presentation to {out_desktop_pptx} and {out_pres_pptx} successfully!")
