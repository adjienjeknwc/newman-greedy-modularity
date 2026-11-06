# Classroom Presentation Speaker Script: Newman's Greedy Modularity Optimization

**Estimated Total Presentation Time:** 7 – 10 minutes  
**Target Audience:** Professor & Classmates  
**File to Present:** [`presentation.html`](file:///Users/aditi/.gemini/antigravity/scratch/newman_modularity/2_presentation/presentation.html) (Open in Chrome/Safari, press `F` for Full Screen, use `Right Arrow` to advance)

---

### Slide 1: Title & Overview (0:00 – 1:00)
- **What to say:**
  > "Good morning Professor and classmates. Today I am presenting my project on *Newman’s Greedy Optimization of Modularity*—an agglomerative hierarchical algorithm for detecting community structures in complex networks published by Mark Newman in 2004, alongside the Clauset–Newman–Moore speedup.
  >
  > For this evaluation, I have implemented the algorithm strictly from first principles in Python, tested it on both an analytical 6-node toy graph and Zachary's classic 34-node Karate Club network, and verified our results against NetworkX's reference implementation."

---

### Slide 2: What is Modularity $Q$? (1:00 – 2:00)
- **What to say:**
  > "Before looking at the algorithm, what problem are we solving? In complex networks—whether social networks, biological networks, or the web—nodes naturally cluster into modules or communities that have dense internal links and sparser connections between groups.
  >
  > Modularity, denoted by $Q$, quantifies this edge density compared to a null model: a random graph with the same degree sequence. 
  >
  > As you see in the formula on the slide, $Q$ sums over all communities the actual fraction of internal edges, $L_c / m$, minus the expected fraction, $(k_c / 2m)^2$. If a network has strong community organization, $Q$ typically falls between $0.3$ and $0.7$. If $Q$ is near zero or negative, the edges are simply random noise or bipartite."

---

### Slide 3: Derivation of $\Delta Q = 2(e_{ij} - a_i a_j)$ (2:00 – 3:30)
- **What to say:**
  > "Newman’s brilliant insight was reformulating modularity in terms of an edge fraction matrix $e_{ij}$ and degree fraction vector $a_i$.
  >
  > When we consider merging two communities, $i$ and $j$, into a new community $k$, we don't need to recompute modularity over the entire graph.
  >
  > By expanding $(a_i + a_j)^2$, the change in modularity simplifies to:
  > $$\Delta Q = 2(e_{ij} - a_i a_j)$$
  >
  > Notice the crucial property here: if there is no edge between communities $i$ and $j$, $e_{ij}$ is zero, which makes $\Delta Q$ equal to $-2 a_i a_j$, which is strictly negative. This proves mathematically that we only ever need to evaluate pairs of communities that are already connected by an edge. This prunes our search space tremendously."

---

### Slide 4: Algorithm Workflow & Complexity (3:30 – 4:30)
- **What to say:**
  > "The algorithm proceeds in 5 clean steps:
  > 1. It initializes every vertex as its own community, meaning $n$ communities initially.
  > 2. In each iteration, it greedily picks the connected pair of communities that maximizes $\Delta Q$.
  > 3. It updates the internal edges $e_{ii}$ and neighbor edges $e_{ik}$ in $O(n)$ time.
  > 4. It repeats this for exactly $n-1$ merges until all vertices merge into one giant community, building a full dendrogram.
  > 5. Finally, we cut the dendrogram at the step that achieved the maximum modularity $Q^*$.
  >
  > In Newman's 2004 formulation, each step takes $O(m)$ to scan edges and $O(n)$ to update matrices, leading to an overall runtime of $O(n^2)$ on sparse networks."

---

### Slide 5: Benchmark 1 – 6-Node Toy Graph (4:30 – 5:30)
- **What to say:**
  > "Now let us examine the experimental results. First, I tested our implementation on a controlled 6-node toy graph consisting of two triangles connected by a single bridge edge between nodes 2 and 3.
  >
  > As shown in the table and plot:
  > - At step 0, with 6 isolated nodes, $Q$ is $-0.1735$.
  > - Steps 1 and 2 merge the first triangle, $\{0, 1, 2\}$.
  > - Steps 3 and 4 merge the second triangle, $\{3, 4, 5\}$.
  > - At Step 4, modularity peaks at $Q^* = 0.3571$ with exactly 2 communities.
  > - At Step 5, when the algorithm is forced to merge across the bridge into a single community, $Q$ drops sharply to $0.0000$.
  >
  > Our scratch implementation matches NetworkX's output identically."

---

### Slide 6: Benchmark 2 – Zachary's Karate Club (5:30 – 6:45)
- **What to say:**
  > "Next, I evaluated the algorithm on Zachary's classic Karate Club graph, containing 34 members and 78 edges.
  >
  > The algorithm executed all 33 merge steps:
  > - $Q$ climbs steadily from $-0.0498$ at step 0 all the way to **Step 31**, where it reaches the global peak modularity of **$Q^* = 0.38067$**.
  > - At this peak, it discovers **3 communities**:
  >   1. The Officer / John A faction with 17 members.
  >   2. Mr. Hi's core allies with 9 members.
  >   3. Mr. Hi's outer cohort with 8 members.
  > - Merging Mr. Hi's two subgroups at Step 32 drops $Q$ to $0.3718$.
  > - This precisely replicates the findings published in Mark Newman's 2004 paper."

---

### Slide 7: Verification & Comparison with NetworkX (6:45 – 7:45)
- **What to say:**
  > "To rigorously validate our code, I benchmarked our from-scratch outputs against NetworkX’s `greedy_modularity_communities`:
  > - For the toy graph: partitions and modularity match to 10 decimal places.
  > - For the Karate club: unweighted partitions and modularity match to 10 decimal places ($Q = 0.38067$).
  >
  > An interesting subtlety to highlight: NetworkX's Karate graph includes edge weights by default based on interaction frequencies. When run weighted, modularity is $0.4345$. When run unweighted—which is the canonical Newman 2004 benchmark—our results and NetworkX's match 100%."

---

### Slide 8: Clauset–Newman–Moore (CNM 2004) Speedup (7:45 – 8:45)
- **What to say:**
  > "Finally, let's address the Clauset–Newman–Moore speedup. While Newman 2004 operates in $O(n^2)$, CNM realized that we can maintain $\Delta Q$ directly without full matrix rescans:
  > 1. Each community maintains a max-heap of its neighbors' $\Delta Q$ values.
  > 2. A global max-heap tracks the highest $\Delta Q$ across all communities.
  > 3. Selecting the best pair to merge takes $O(1)$ time!
  > 4. Updating heaps takes $O(\log n)$ per neighbor.
  >
  > This dropped the overall time complexity from $O(n^2)$ to $O(n \log^2 n)$, allowing community detection to scale from thousands of nodes to millions of vertices."

---

### Slide 9: Conclusion & Viva Readiness (8:45 – 9:15)
- **What to say:**
  > "To conclude: we have derived, implemented, validated, and visualized Newman's greedy modularity optimization from scratch, demonstrated exact equivalence with standard libraries, and explored the algorithmic speedups that made it practical for massive networks.
  >
  > Thank you for your time. I am now happy to take any questions."
