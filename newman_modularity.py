"""
Newman's Greedy Modularity Optimization Algorithm (Agglomerative Hierarchical Clustering)
Reference: M. E. J. Newman, "Fast algorithm for detecting community structure in networks",
           Physical Review E 69, 066133 (2004).

This module implements the algorithm strictly from first principles using:
  - Fraction of edges matrix: e_ij
  - Community degree fraction: a_i = sum_j(e_ij) = k_i / (2m)
  - Modularity change on merging community i and j: Delta Q = 2 * (e_ij - a_i * a_j)
  - Updates:
      e_ii <- e_ii + e_jj + 2 * e_ij
      e_ik = e_ki <- e_ik + e_jk  (for all k != i, j)
      a_i  <- a_i + a_j
      community j is removed
"""

from typing import List, Set, Tuple, Dict, Any, Optional
import networkx as nx


class NewmanGreedyCommunityDetection:
    """
    Greedy agglomerative modularity maximization algorithm (Newman, 2004).
    """

    def __init__(self, G: nx.Graph, weight: Optional[str] = None):
        """
        Initialize the detector with a NetworkX undirected graph.

        Parameters
        ----------
        G : nx.Graph
            An undirected graph.
        weight : Optional[str]
            Edge attribute name for weights. If None, treats graph as unweighted (all weights = 1.0).
        """
        self.G = G
        self.weight = weight
        self.nodes = list(G.nodes())
        self.node_to_idx = {node: i for i, node in enumerate(self.nodes)}
        self.idx_to_node = {i: node for i, node in enumerate(self.nodes)}
        self.n = len(self.nodes)

        # Compute total weight (m for unweighted, W for weighted)
        if weight is None:
            self.m = float(G.number_of_edges())
        else:
            self.m = float(sum(d.get(weight, 1.0) for _, _, d in G.edges(data=True)))

        if self.m == 0:
            raise ValueError("Graph has no edges; modularity cannot be optimized.")

        # Initialize e and a
        self._init_data_structures()

    def _init_data_structures(self):
        """
        Step 1 of Newman (2004):
        - Each node starts in its own community (n communities).
        - e_ij is the fraction of total edges between community i and j: e_ij = A_ij / (2m)
        - a_i is the fraction of edge ends in community i: a_i = sum_j e_ij = k_i / (2m)
        - Q_0 = sum_i (e_ii - a_i^2) = -sum_i a_i^2 (since e_ii = 0 initially)
        """
        n = self.n
        m = self.m
        
        # e matrix: e[i][j] stores fraction of edges between community i and community j
        self.e = [[0.0] * n for _ in range(n)]

        for u, v, data in self.G.edges(data=True):
            i, j = self.node_to_idx[u], self.node_to_idx[v]
            w = float(data.get(self.weight, 1.0)) if self.weight else 1.0
            frac = w / (2.0 * m)
            self.e[i][j] += frac
            self.e[j][i] += frac

        # a vector: fraction of edge endpoints attached to vertices in community i
        self.a = [sum(self.e[i]) for i in range(n)]

        # Active communities: track which indices represent currently active communities
        self.active_communities: Set[int] = set(range(n))

        # Community membership: maps active community index to set of original graph nodes
        self.community_members: Dict[int, Set[Any]] = {
            i: {self.idx_to_node[i]} for i in range(n)
        }

        # Initial Modularity: Q = sum_i (e_ii - a_i^2)
        # Initially e_ii = 0, so Q_0 = - sum_i (a_i^2)
        self.current_q = sum(self.e[i][i] - (self.a[i] ** 2) for i in self.active_communities)

    def run(self) -> Tuple[List[Set[Any]], float, int, List[Dict[str, Any]]]:
        """
        Executes Newman's agglomerative greedy modularity optimization.

        Iteratively merges the pair of communities that yields the greatest
        increase (or least decrease) in modularity Delta Q = 2 * (e_ij - a_i * a_j)
        until all vertices are in a single community.

        Returns
        -------
        best_partition : List[Set[Any]]
            The partition (list of node sets) that achieved the maximum modularity Q.
        best_q : float
            The maximum modularity value achieved.
        best_step : int
            The merge step index at which the maximum modularity occurred.
        history : List[Dict[str, Any]]
            Step-by-step merge record for dendrogram and plotting.
        """
        history: List[Dict[str, Any]] = []

        # Record initial state (step 0, n individual communities)
        history.append({
            "step": 0,
            "merged": None,
            "merged_indices": None,
            "delta_q": 0.0,
            "q": self.current_q,
            "num_communities": len(self.active_communities),
            "partition": [sorted(list(self.community_members[c])) for c in sorted(self.active_communities)],
        })

        best_q = self.current_q
        best_partition = [self.community_members[c].copy() for c in sorted(self.active_communities)]
        best_step = 0

        step = 0
        while len(self.active_communities) > 1:
            step += 1

            # Find connected pair (i, j) with highest Delta Q
            best_delta_q = -float("inf")
            best_pair: Optional[Tuple[int, int]] = None

            active_sorted = sorted(self.active_communities)
            for idx_a, i in enumerate(active_sorted):
                for j in active_sorted[idx_a + 1:]:
                    # Newman (2004): only consider pairs with an existing edge (e_ij > 0)
                    if self.e[i][j] > 0.0:
                        delta_q = 2.0 * (self.e[i][j] - self.a[i] * self.a[j])
                        if delta_q > best_delta_q:
                            best_delta_q = delta_q
                            best_pair = (i, j)

            # Fallback for disconnected components: if no connected pair remains,
            # pick pair minimizing decrease (delta_q = -2 * a_i * a_j)
            if best_pair is None:
                for idx_a, i in enumerate(active_sorted):
                    for j in active_sorted[idx_a + 1:]:
                        delta_q = -2.0 * self.a[i] * self.a[j]
                        if delta_q > best_delta_q:
                            best_delta_q = delta_q
                            best_pair = (i, j)

            i, j = best_pair  # type: ignore

            # Save nodes merged for readable reporting
            nodes_i = sorted(list(self.community_members[i]))
            nodes_j = sorted(list(self.community_members[j]))

            # -------------------------------------------------------------
            # Newman 2004 Update Rules:
            # 1. Update internal edge fraction for new merged community i:
            #    e_ii <- e_ii + e_jj + 2 * e_ij
            # 2. Update inter-community edge fractions for all other active k:
            #    e_ik = e_ki <- e_ik + e_jk
            # 3. Update degree fraction for merged community i:
            #    a_i  <- a_i + a_j
            # 4. Zero out community j in matrix e and vector a, remove j from active.
            # -------------------------------------------------------------
            self.e[i][i] = self.e[i][i] + self.e[j][j] + 2.0 * self.e[i][j]

            for k in self.active_communities:
                if k != i and k != j:
                    self.e[i][k] = self.e[i][k] + self.e[j][k]
                    self.e[k][i] = self.e[i][k]

            self.a[i] = self.a[i] + self.a[j]

            # Clear j's row and column
            for k in range(self.n):
                self.e[j][k] = 0.0
                self.e[k][j] = 0.0
            self.e[j][j] = 0.0
            self.a[j] = 0.0

            # Update community members and active set
            self.community_members[i] = self.community_members[i].union(self.community_members[j])
            del self.community_members[j]
            self.active_communities.remove(j)

            # Update Q
            self.current_q += best_delta_q

            # Verify numerical stability with direct Q calculation
            q_direct = sum(self.e[c][c] - (self.a[c] ** 2) for c in self.active_communities)

            current_partition = [self.community_members[c].copy() for c in sorted(self.active_communities)]

            history.append({
                "step": step,
                "merged": (nodes_i, nodes_j),
                "merged_indices": (i, j),
                "delta_q": best_delta_q,
                "q": self.current_q,
                "q_direct": q_direct,
                "num_communities": len(self.active_communities),
                "partition": [sorted(list(c)) for c in current_partition],
            })

            # Check if this step beats the maximum modularity so far
            if self.current_q > best_q:
                best_q = self.current_q
                best_partition = current_partition
                best_step = step

        return best_partition, best_q, best_step, history
