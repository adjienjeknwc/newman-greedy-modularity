"""
Experiments and Validation Script for Newman's Greedy Modularity Optimization
1. 6-node toy graph (two triangles + bridge)
2. Zachary's Karate Club
3. Comparison with NetworkX greedy_modularity_communities
4. Matplotlib plots generation
"""

import os
import networkx as nx
import matplotlib.pyplot as plt
from networkx.algorithms.community import greedy_modularity_communities, modularity
from newman_modularity import NewmanGreedyCommunityDetection


def create_toy_graph() -> nx.Graph:
    """
    Creates a 6-node toy graph:
    Triangle 1: nodes 0, 1, 2
    Triangle 2: nodes 3, 4, 5
    Bridge: edge (2, 3)
    Total nodes: 6, Total edges: 7
    """
    G = nx.Graph()
    # Triangle 1
    G.add_edges_from([(0, 1), (1, 2), (2, 0)])
    # Bridge
    G.add_edge(2, 3)
    # Triangle 2
    G.add_edges_from([(3, 4), (4, 5), (5, 3)])
    return G


def run_toy_experiment():
    print("=" * 80)
    print("EXPERIMENT 1: 6-NODE TOY GRAPH (TWO TRIANGLES + BRIDGE)")
    print("=" * 80)
    G = create_toy_graph()
    n = G.number_of_nodes()
    m = G.number_of_edges()
    print(f"Graph stats: {n} nodes, {m} edges")
    print(f"Edges: {sorted(G.edges())}")

    detector = NewmanGreedyCommunityDetection(G)
    best_partition, best_q, best_step, history = detector.run()

    print("\n--- STEP-BY-STEP MERGE HISTORY ---")
    header = f"{'Step':<5} | {'Merged Communities':<25} | {'Delta Q':<10} | {'Modularity Q':<12} | {'# Comms':<7} | {'Partition'}"
    print(header)
    print("-" * len(header))

    for h in history:
        step = h["step"]
        if step == 0:
            merged_str = "Initial state"
        else:
            merged_str = f"{h['merged'][0]} + {h['merged'][1]}"
        delta_q_str = f"{h['delta_q']:+.4f}" if step > 0 else "   -   "
        q_str = f"{h['q']:+.4f}"
        num_c = h["num_communities"]
        part_str = str(h["partition"])
        print(f"{step:<5} | {merged_str:<25} | {delta_q_str:<10} | {q_str:<12} | {num_c:<7} | {part_str}")

    print("\n--- SUMMARY FOR TOY GRAPH ---")
    print(f"Best Modularity Q* : {best_q:.5f} (achieved at Step {best_step})")
    print(f"Best Partition     : {[sorted(list(c)) for c in best_partition]} ({len(best_partition)} communities)")

    # NetworkX verification
    nx_partition = list(greedy_modularity_communities(G))
    nx_q = modularity(G, nx_partition)
    print(f"\n--- NETWORKX VALIDATION ---")
    print(f"NetworkX Partition : {[sorted(list(c)) for c in nx_partition]}")
    print(f"NetworkX Modularity: {nx_q:.5f}")
    match = sorted([sorted(list(c)) for c in best_partition]) == sorted([sorted(list(c)) for c in nx_partition])
    print(f"Partitions Match Exactly? {'YES! [PERFECT MATCH]' if match else 'NO'}")

    return G, history, best_partition, best_step, best_q


def run_karate_experiment():
    print("\n" + "=" * 80)
    print("EXPERIMENT 2: ZACHARY'S KARATE CLUB GRAPH (34 NODES, 78 EDGES)")
    print("=" * 80)
    G = nx.karate_club_graph()
    n = G.number_of_nodes()
    m = G.number_of_edges()
    print(f"Graph stats: {n} nodes, {m} edges")

    detector = NewmanGreedyCommunityDetection(G, weight=None)
    best_partition, best_q, best_step, history = detector.run()

    print("\n--- STEP-BY-STEP MERGE HISTORY (SELECTED KEY STEPS) ---")
    header = f"{'Step':<5} | {'Merged Communities (Sample)':<30} | {'Delta Q':<10} | {'Modularity Q':<12} | {'# Comms':<7}"
    print(header)
    print("-" * len(header))

    for h in history:
        step = h["step"]
        if step == 0:
            merged_str = "Initial (34 individual nodes)"
        else:
            m0 = str(h["merged"][0]) if len(h["merged"][0]) <= 4 else f"{h['merged'][0][:3]}...+{len(h['merged'][0])}n"
            m1 = str(h["merged"][1]) if len(h["merged"][1]) <= 4 else f"{h['merged'][1][:3]}...+{len(h['merged'][1])}n"
            merged_str = f"{m0} + {m1}"
        delta_q_str = f"{h['delta_q']:+.5f}" if step > 0 else "    -    "
        q_str = f"{h['q']:+.5f}"
        num_c = h["num_communities"]
        
        # Print first 5 steps, around best step, and final 4 steps
        if step <= 5 or abs(step - best_step) <= 2 or step >= len(history) - 3:
            mark = " <--- MAX Q (Peak)" if step == best_step else ""
            print(f"{step:<5} | {merged_str:<30} | {delta_q_str:<10} | {q_str:<12} | {num_c:<7}{mark}")

    print("\n--- SUMMARY FOR KARATE CLUB ---")
    print(f"Best Modularity Q* : {best_q:.5f} (achieved at Step {best_step})")
    print(f"Best Partition ({len(best_partition)} communities):")
    for idx, comm in enumerate(best_partition, start=1):
        print(f"  Community {idx} ({len(comm)} members): {sorted(list(comm))}")

    # NetworkX verification (unweighted)
    nx_partition_unweighted = list(greedy_modularity_communities(G, weight=None))
    nx_q_unweighted = modularity(G, nx_partition_unweighted, weight=None)
    print(f"\n--- NETWORKX VALIDATION (UNWEIGHTED - NEWMAN 2004) ---")
    print(f"NetworkX Partition : {[sorted(list(c)) for c in nx_partition_unweighted]}")
    print(f"NetworkX Modularity: {nx_q_unweighted:.5f}")
    match = sorted([sorted(list(c)) for c in best_partition]) == sorted([sorted(list(c)) for c in nx_partition_unweighted])
    print(f"Partitions Match Exactly? {'YES! [PERFECT MATCH]' if match else 'NO'}")

    # Also report weighted if interested
    nx_partition_weighted = list(greedy_modularity_communities(G, weight="weight"))
    nx_q_weighted = modularity(G, nx_partition_weighted, weight="weight")
    print(f"\n--- NETWORKX COMPARISON (WEIGHTED - ZACHARY INTERACTION FREQUENCIES) ---")
    print(f"Weighted Modularity: {nx_q_weighted:.5f} (Partition: {[sorted(list(c)) for c in nx_partition_weighted]})")

    return G, history, best_partition, best_step, best_q


def generate_plots(toy_G, toy_history, toy_best_step, toy_partition,
                   karate_G, karate_history, karate_best_step, karate_partition):
    """
    Generates and saves visual plots for presentation:
    1. Modularity Q vs Merge Step for Toy Graph
    2. Modularity Q vs Merge Step for Karate Club
    3. Community structure network drawings for both graphs
    """
    os.makedirs("plots", exist_ok=True)
    plt.rcParams.update({"font.size": 11, "figure.autolayout": True})

    # 1. Toy Graph Modularity Curve
    steps_toy = [h["step"] for h in toy_history]
    q_toy = [h["q"] for h in toy_history]

    fig, ax = plt.subplots(figsize=(7, 4.5), dpi=300)
    ax.plot(steps_toy, q_toy, marker='o', color='#1f77b4', linewidth=2.2, markersize=7, label="Modularity $Q$")
    ax.scatter([toy_best_step], [toy_history[toy_best_step]["q"]], color='#d62728', s=140, zorder=5, label=f"Max $Q = {toy_history[toy_best_step]['q']:.4f}$ (Step {toy_best_step})")
    ax.axvline(toy_best_step, color='#d62728', linestyle='--', alpha=0.6)
    ax.axhline(0, color='gray', linestyle=':', alpha=0.7)

    # Annotate peak
    ax.annotate(f"Optimal 2 Communities\nStep {toy_best_step}: $Q = {toy_history[toy_best_step]['q']:.4f}$",
                xy=(toy_best_step, toy_history[toy_best_step]["q"]),
                xytext=(toy_best_step - 1.8, toy_history[toy_best_step]["q"] + 0.05),
                arrowprops=dict(arrowstyle="->", color='#d62728', lw=1.5),
                fontweight='bold', color='#d62728',
                bbox=dict(boxstyle="round,pad=0.3", fc="#ffeedd", ec="#d62728", lw=1))

    ax.set_title("Newman Modularity Optimization: 6-Node Toy Graph", fontsize=13, fontweight='bold')
    ax.set_xlabel("Merge Step", fontsize=12)
    ax.set_ylabel("Modularity $Q$", fontsize=12)
    ax.set_xticks(steps_toy)
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.legend(loc="lower right")
    toy_plot_path = "plots/toy_graph_modularity.png"
    plt.savefig(toy_plot_path)
    plt.close()
    print(f"Saved: {toy_plot_path}")

    # 2. Karate Club Modularity Curve
    steps_k = [h["step"] for h in karate_history]
    q_k = [h["q"] for h in karate_history]

    fig, ax = plt.subplots(figsize=(8, 5), dpi=300)
    ax.plot(steps_k, q_k, marker='.', color='#2ca02c', linewidth=2.0, markersize=6, label="Modularity $Q$")
    ax.scatter([karate_best_step], [karate_history[karate_best_step]["q"]], color='#d62728', s=150, zorder=5,
               label=f"Peak $Q^* = {karate_history[karate_best_step]['q']:.4f}$ (Step {karate_best_step})")
    ax.axvline(karate_best_step, color='#d62728', linestyle='--', alpha=0.6)
    ax.axhline(0, color='gray', linestyle=':', alpha=0.7)

    # Annotations
    ax.annotate(f"Initial: 34 comms\n$Q_0 = {q_k[0]:.4f}$",
                xy=(0, q_k[0]), xytext=(2, q_k[0] + 0.08),
                arrowprops=dict(arrowstyle="->", color='#1f77b4', lw=1.2),
                bbox=dict(boxstyle="round,pad=0.3", fc="#eef4fb", ec="#1f77b4", lw=1))

    ax.annotate(f"Peak (3 Communities)\nStep {karate_best_step}: $Q = {q_k[karate_best_step]:.4f}$",
                xy=(karate_best_step, q_k[karate_best_step]),
                xytext=(karate_best_step - 14, q_k[karate_best_step] - 0.05),
                arrowprops=dict(arrowstyle="->", color='#d62728', lw=1.5),
                fontweight='bold', color='#d62728',
                bbox=dict(boxstyle="round,pad=0.3", fc="#ffeedd", ec="#d62728", lw=1))

    ax.annotate(f"Final 1 Community\n$Q_{{33}} = 0.0000$",
                xy=(33, 0), xytext=(24, 0.08),
                arrowprops=dict(arrowstyle="->", color='gray', lw=1.2),
                bbox=dict(boxstyle="round,pad=0.3", fc="#f5f5f5", ec="gray", lw=1))

    ax.set_title("Newman Modularity Optimization: Zachary's Karate Club", fontsize=13, fontweight='bold')
    ax.set_xlabel("Merge Step (Agglomerations)", fontsize=12)
    ax.set_ylabel("Modularity $Q$", fontsize=12)
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.legend(loc="upper left")
    karate_plot_path = "plots/karate_modularity.png"
    plt.savefig(karate_plot_path)
    plt.close()
    print(f"Saved: {karate_plot_path}")

    # 3. Network graph visualizations colored by detected communities
    fig, axes = plt.subplots(1, 2, figsize=(14, 6), dpi=300)

    # Left: Toy graph
    pos_toy = {
        0: (-1.5, 0.86), 1: (-1.5, -0.86), 2: (-0.5, 0.0),
        3: (0.5, 0.0), 4: (1.5, 0.86), 5: (1.5, -0.86)
    }
    # Color map for toy graph (2 communities)
    toy_node_color = {}
    toy_palette = ['#ff7f0e', '#1f77b4']
    for idx, c in enumerate(toy_partition):
        for node in c:
            toy_node_color[node] = toy_palette[idx % len(toy_palette)]
    colors_toy = [toy_node_color[n] for n in toy_G.nodes()]

    nx.draw_networkx_nodes(toy_G, pos_toy, ax=axes[0], node_color=colors_toy, node_size=700, edgecolors='black', linewidths=1.5)
    nx.draw_networkx_edges(toy_G, pos_toy, ax=axes[0], width=2.0, alpha=0.7, edge_color='#444444')
    nx.draw_networkx_labels(toy_G, pos_toy, ax=axes[0], font_size=12, font_family='sans-serif', font_weight='bold', font_color='white')
    axes[0].set_title(f"Toy Graph Partition (Peak $Q = {toy_history[toy_best_step]['q']:.4f}$)\nComm 1: {{0,1,2}} | Comm 2: {{3,4,5}}", fontsize=12, fontweight='bold')
    axes[0].axis('off')

    # Right: Karate Club
    pos_k = nx.spring_layout(karate_G, seed=42)
    karate_palette = ['#e41a1c', '#377eb8', '#4daf4a']
    karate_node_color = {}
    for idx, c in enumerate(karate_partition):
        for node in c:
            karate_node_color[node] = karate_palette[idx % len(karate_palette)]
    colors_k = [karate_node_color[n] for n in karate_G.nodes()]

    nx.draw_networkx_nodes(karate_G, pos_k, ax=axes[1], node_color=colors_k, node_size=400, edgecolors='black', linewidths=1.2)
    nx.draw_networkx_edges(karate_G, pos_k, ax=axes[1], width=1.2, alpha=0.5, edge_color='#666666')
    nx.draw_networkx_labels(karate_G, pos_k, ax=axes[1], font_size=9, font_family='sans-serif', font_weight='bold', font_color='white')
    axes[1].set_title(f"Karate Club Detected Partition (Peak $Q = {karate_history[karate_best_step]['q']:.4f}$)\n3 Communities (8, 9, and 17 members)", fontsize=12, fontweight='bold')
    axes[1].axis('off')

    combined_plot_path = "plots/network_communities_visualization.png"
    plt.savefig(combined_plot_path)
    plt.close()
    print(f"Saved: {combined_plot_path}")


if __name__ == "__main__":
    os.environ["MPLCONFIGDIR"] = "/tmp/matplotlib_cache"
    toy_G, toy_hist, toy_part, toy_best_step, toy_best_q = run_toy_experiment()
    karate_G, karate_hist, karate_part, karate_best_step, karate_best_q = run_karate_experiment()
    generate_plots(toy_G, toy_hist, toy_best_step, toy_part,
                   karate_G, karate_hist, karate_best_step, karate_part)
    print("\nAll experiments, validations, and plots completed successfully!")

