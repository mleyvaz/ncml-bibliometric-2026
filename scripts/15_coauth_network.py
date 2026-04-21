"""Co-authorship network for NCML — static figures directly from Python.

Loads:
  reports/clean/network_nodes.csv  (id, label, weight=articles)
  reports/clean/network_edges.csv  (source, target, weight=coauth_count)

Produces:
  reports/clean/coauth_full.png       Full filtered graph (>=2 articles)
  reports/clean/coauth_core.png       Top producers only (>=4 articles)
  reports/clean/coauth_communities.md  Louvain communities summary
  reports/clean/network_stats.json    Basic graph metrics
"""
from __future__ import annotations
import sys
import json
from pathlib import Path
import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(r"C:/Users/HP/Documents/NCML_Bibliometric")
REP = ROOT / "reports" / "clean"
REP.mkdir(exist_ok=True, parents=True)

nodes = pd.read_csv(REP / "network_nodes.csv")
edges = pd.read_csv(REP / "network_edges.csv")

# Guard: drop rows with empty labels (residual clusters from empty-name authorships)
nodes = nodes[nodes["label"].notna() & (nodes["label"].astype(str).str.strip() != "")].copy()
edges = edges[edges["source"].isin(nodes["id"]) & edges["target"].isin(nodes["id"])].copy()
print(f"Nodes: {len(nodes)}   Edges: {len(edges)}")

# Build graph
G = nx.Graph()
for _, r in nodes.iterrows():
    G.add_node(int(r["id"]), label=str(r["label"]), weight=int(r["weight"]))
for _, r in edges.iterrows():
    G.add_edge(int(r["source"]), int(r["target"]), weight=int(r["weight"]))

# ---------- Basic metrics ----------
components = list(nx.connected_components(G))
gc = max(components, key=len)
Gc = G.subgraph(gc).copy()

stats = {
    "nodes": G.number_of_nodes(),
    "edges": G.number_of_edges(),
    "density": round(nx.density(G), 5),
    "avg_degree": round(sum(dict(G.degree()).values()) / G.number_of_nodes(), 2),
    "n_components": len(components),
    "largest_component_nodes": len(gc),
    "largest_component_share": round(len(gc) / G.number_of_nodes(), 3),
    "avg_clustering": round(nx.average_clustering(G), 3),
    "transitivity": round(nx.transitivity(G), 3),
    "avg_shortest_path_gc": round(nx.average_shortest_path_length(Gc), 2) if len(gc) < 2000 else "skipped",
    "diameter_gc": nx.diameter(Gc) if len(gc) < 2000 else "skipped",
}
(REP / "network_stats.json").write_text(json.dumps(stats, indent=2))
print(json.dumps(stats, indent=2))

# ---------- Louvain communities on full graph ----------
import community as community_louvain  # python-louvain
part = community_louvain.best_partition(G, weight="weight", random_state=42)
nx.set_node_attributes(G, part, "community")
mod = community_louvain.modularity(part, G, weight="weight")
print(f"Louvain communities: {len(set(part.values()))}  modularity={mod:.3f}")


def draw_subgraph(subG, fname, title, label_top_n=30, seed=42, figsize=(16, 12),
                  layout="spring", k_factor=2.5):
    if subG.number_of_nodes() == 0:
        print(f"[skip] empty graph for {fname}")
        return
    print(f"  drawing {fname}: {subG.number_of_nodes()} nodes, {subG.number_of_edges()} edges")
    n = subG.number_of_nodes()
    if layout == "kk":
        pos = nx.kamada_kawai_layout(subG, weight="weight")
    else:
        pos = nx.spring_layout(subG, weight="weight", seed=seed,
                               k=k_factor / np.sqrt(max(1, n)), iterations=200)
    node_comm = nx.get_node_attributes(subG, "community")
    uniq_c = sorted(set(node_comm.values()))
    cmap = plt.get_cmap("tab20", max(20, len(uniq_c)))
    color_map = {c: cmap(i % cmap.N) for i, c in enumerate(uniq_c)}
    node_colors = [color_map[node_comm[node]] for node in subG.nodes()]
    sizes = np.array([subG.nodes[node]["weight"] for node in subG.nodes()])
    sizes_scaled = 60 + 180 * np.sqrt(sizes)

    fig, ax = plt.subplots(figsize=figsize)
    edge_ws = [subG[u][v]["weight"] for u, v in subG.edges()]
    if edge_ws:
        scaled = 0.3 + 0.6 * np.array(edge_ws)
        nx.draw_networkx_edges(subG, pos, alpha=0.2, width=scaled, edge_color="#888888", ax=ax)
    nx.draw_networkx_nodes(subG, pos, node_size=sizes_scaled, node_color=node_colors,
                           linewidths=0.6, edgecolors="white", alpha=0.92, ax=ax)
    # Label only the TOP-N nodes by weight to avoid clutter
    nodes_sorted = sorted(subG.nodes(), key=lambda x: subG.nodes[x]["weight"], reverse=True)
    to_label = {node: subG.nodes[node]["label"] for node in nodes_sorted[:label_top_n]}
    nx.draw_networkx_labels(subG, pos, labels=to_label, font_size=8,
                            font_color="#111111", font_weight="bold", ax=ax,
                            bbox=dict(facecolor="white", edgecolor="none", alpha=0.65, pad=0.8))
    ax.set_title(title, fontsize=13)
    ax.axis("off")
    plt.tight_layout()
    plt.savefig(REP / fname, dpi=160, bbox_inches="tight")
    plt.close()


# ---------- (A) Main connected component only — clearest structure ----------
gc_set = max(nx.connected_components(G), key=len)
Gmc = G.subgraph(gc_set).copy()
part_mc = community_louvain.best_partition(Gmc, weight="weight", random_state=42)
nx.set_node_attributes(Gmc, part_mc, "community")
mod_mc = community_louvain.modularity(part_mc, Gmc, weight="weight")
draw_subgraph(Gmc, "coauth_main.png",
              f"Componente conexo principal NCML — n={Gmc.number_of_nodes()} autores ({len(gc_set)/G.number_of_nodes():.0%} del total), modularidad={mod_mc:.2f}",
              label_top_n=25, figsize=(16, 12), layout="spring", k_factor=3.5)

# ---------- (B) Core productive authors (>=4 articles) ----------
core_nodes = [n for n, d in G.nodes(data=True) if d["weight"] >= 4]
Gcore = G.subgraph(core_nodes).copy()
# Drop isolated core nodes (no co-author with another core)
Gcore = Gcore.subgraph([n for n in Gcore.nodes() if Gcore.degree(n) > 0]).copy()
part3 = community_louvain.best_partition(Gcore, weight="weight", random_state=42)
nx.set_node_attributes(Gcore, part3, "community")
draw_subgraph(Gcore, "coauth_core.png",
              f"Nucleo productivo NCML — autores con ≥4 articulos conectados (n={Gcore.number_of_nodes()})",
              label_top_n=40, figsize=(14, 11), layout="kk")

# ---------- (C) Full filtered (>=2 articles) — for completeness ----------
kept = [n for n, d in G.nodes(data=True) if d["weight"] >= 2]
G2 = G.subgraph(kept).copy()
part2 = community_louvain.best_partition(G2, weight="weight", random_state=42)
nx.set_node_attributes(G2, part2, "community")
mod2 = community_louvain.modularity(part2, G2, weight="weight")
draw_subgraph(G2, "coauth_full.png",
              f"Red completa NCML — autores ≥2 articulos (n={G2.number_of_nodes()}, modularidad={mod2:.2f})",
              label_top_n=20, figsize=(18, 13), layout="spring", k_factor=4.5)

# ---------- Community summary ----------
comm_members = {}
for n, c in part2.items():
    comm_members.setdefault(c, []).append(n)

def label(n):
    return G.nodes[n]["label"]

def weight(n):
    return G.nodes[n]["weight"]

comm_rows = []
for c, members in comm_members.items():
    members_sorted = sorted(members, key=weight, reverse=True)
    top = members_sorted[:5]
    comm_rows.append({
        "community": c,
        "n_members": len(members),
        "total_articles": sum(weight(n) for n in members),
        "top_authors": " ;; ".join(f"{label(n)} ({weight(n)})" for n in top),
    })
comm_df = pd.DataFrame(comm_rows).sort_values("total_articles", ascending=False)
comm_df.to_csv(REP / "coauth_communities.csv", index=False, encoding="utf-8")

md = ["# Red de coautoria NCML — resultados", "",
      "## Estadisticas del grafo completo",
      "",
      "```json",
      json.dumps(stats, indent=2),
      "```",
      "",
      f"## Comunidades (Louvain, modularidad = {mod:.3f})",
      "",
      "### Top 15 comunidades",
      "",
      "| C | Miembros | Articulos | Top autores |",
      "|---|---|---|---|"]
for _, r in comm_df.head(15).iterrows():
    md.append(f"| C{int(r['community'])} | {int(r['n_members'])} | {int(r['total_articles'])} | {r['top_authors'][:160]} |")
md.extend(["", "![Red completa](coauth_full.png)", "",
           "![Nucleo](coauth_core.png)"])
(REP / "coauth_communities.md").write_text("\n".join(md), encoding="utf-8")

print(f"\nComunidades: {len(comm_members)}   modularidad: {mod:.3f}")
print("\nTop 5 comunidades:")
for _, r in comm_df.head(5).iterrows():
    print(f"  C{int(r['community'])}: {int(r['n_members'])} miembros, {int(r['total_articles'])} articulos")
    print(f"    {r['top_authors'][:180]}")
print(f"\nFiguras: {REP / 'coauth_full.png'} y {REP / 'coauth_core.png'}")
