import numpy as np
from matplotlib.lines import Line2D
from shutil import copyfile
import os
import matplotlib.pyplot as plt
from time import gmtime, strftime
import plotly.graph_objects as go

# Simulation Parameters
MONTE_CARLOS = 1
SIM_TIME = 800
STEP = 0.01
# Network Parameters
NU = 20
NUM_NODES = 20
NUM_NEIGHBOURS = 4
START_TIMES = 10*np.ones(NUM_NODES)
GRAPH = 'regular'
REPDIST = 'zipf'
if REPDIST=='zipf':
    # IOTA data rep distribution - Zipf s=0.9
    REP50 = [(51)/((NodeID+1)**0.9) for NodeID in range(50)]
    REPN = [(NUM_NODES+1)/((NodeID+1)**0.9) for NodeID in range(NUM_NODES)]
    REP = [(sum(REP50)/sum(REPN))*rep for rep in REPN]
elif REPDIST=='uniform':
    # Permissioned System rep system?
    REP = np.ones(NUM_NODES, dtype=int)

# Modes: 0 = inactive, 1 = content, 2 = best-effort, 3 = malicious
#MODE = [3-(NodeID+1)%4 for NodeID in range(NUM_NODES)] # multiple malicious
MODE = [2-(NodeID)%3 for NodeID in range(NUM_NODES)] # All honest
#MODE = [1 for _ in range(NUM_NODES)] # All content (95%)
MODE[2] = 3 # Make node 2 malicious
# MODE[4] = 3
# MODE[6] = 3 # Make node 2 malicious
# MODE[8] = 3





def per_node_barplot(data, xlabel: str, ylabel: str, title: str, dirstr: str, legend_loc: str = 'upper right', modes=None):
    fig, ax = plt.subplots(figsize=(8,4))
    ax.grid(linestyle='--')
    ax.set_xlabel(xlabel)
    ax.title.set_text(title)
    ax.set_ylabel(ylabel)
    if modes is None:
        modes = list(set(MODE))
    mode_names = ['Inactive', 'Content','Best-effort', 'Malicious', 'Multi-rate']
    colors = ['tab:gray', 'tab:blue', 'tab:red', 'tab:green', 'tab:olive']
    for NodeID in range(NUM_NODES):
        ax.bar(NodeID, data[NodeID], color=colors[MODE[NodeID]])
    ModeLines = [Line2D([0],[0],color=colors[mode], lw=4) for mode in modes]
    if len(modes)>1:
        fig.legend(ModeLines, [mode_names[i] for i in modes], loc=legend_loc)
    plt.savefig(dirstr, bbox_inches='tight')


per_node_barplot(REP, 'Node ID', 'Reputation', 'Reputation Distribution', dirstr+'/plots/RepDist.png')