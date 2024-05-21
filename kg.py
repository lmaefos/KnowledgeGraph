import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import networkx as nx
from collections import Counter
from pyvis.network import Network
from IPython.core.display import display, HTML

# Read the new CSV file
descriptors_data = pd.read_csv("BRIM Metadata.csv")

# Convert DataFrame to a list of lists with all entries as strings
project_data = descriptors_data.astype(str).values.tolist()

# Define a color mapping for each column header
color_map = {
    'Project #': '#e07c3e',           # Orange
    'Application Type': '#ff0000',    # Red
    'Project Title': '#1f77b4',       # Blue
    'Research Focus Area': '#2ca02c', # Green
    'Administering IC(s)': '#9467bd', # Purple
    'Institution': '#8c564b',         # Brown
    'Investigator': '#e377c2',        # Pink
    'Location': '#7f7f7f',            # Grey
    'Year Awarded': '#bcbd22'         # Yellow
}

# Create a Network graph object
net = Network(notebook=True, width="1000px", height="600px", cdn_resources='remote', font_color='white', bgcolor="black", select_menu=True, filter_menu=True)
st.title('Knowledge Graph of BRIM Projects')

# Add description before presenting the knowledge graph
st.markdown("""
# Understanding Nodes and Edges

- **Nodes**: Represent the entities in your graph, such as "Research Focus Area," "Project Title," "Institution," etc. Each node can have various properties like size, color, label, etc.
- **Edges**: Represent the relationships or connections between the nodes, such as a project being associated with a particular research focus area.

For more information on using the filter feature, [explanation below](#selecting-a-node).

# Map Key 

**Node Colors:**
- `Project #`: <span style="color:#e07c3e;">Orange</span>
- `Application Type`: <span style="color:#ff0000;">Red</span>
- `Project Title`: <span style="color:#1f77b4;">Blue</span>
- `Research Focus Area`: <span style="color:#2ca02c;">Green</span>
- `Administering IC(s)`: <span style="color:#9467bd;">Purple</span>
- `Institution`: <span style="color:#8c564b;">Brown</span>
- `Investigator`: <span style="color:#e377c2;">Pink</span>
- `Location`: <span style="color:#7f7f7f;">Grey</span>
- `Year Awarded`: <span style="color:#bcbd22;">Yellow</span>

**Node Shapes:**
- `Project Title`: Triangle
- Other Nodes: Circle            

""", unsafe_allow_html=True)

def create_knowledge_graph(data, columns):
    # Flatten the data to get a list of all descriptors
    all_descriptors = [descriptor for entry in data for descriptor in entry[1:]]

    # Calculate the frequency of each descriptor
    descriptor_frequency = Counter(all_descriptors)

    # Scale the size of nodes based on frequency
    max_frequency = max(descriptor_frequency.values())
    scaling_factor = 20  # Adjust the scaling factor as needed

    # Add nodes and edges to the network
    for entry in data:
        investigator = entry[columns.get_loc('Investigator')]  # Assuming 'Investigator' is the main node
        net.add_node(investigator, label=investigator, color=color_map['Investigator'])

        for attribute, descriptor in zip(columns, entry):
            if attribute == 'Investigator':
                continue
            frequency = descriptor_frequency[descriptor]
            node_size = scaling_factor * (frequency / max_frequency)
            node_color = color_map.get(attribute, '#982568')  # Default to purple if not found
            
            # Set shape to triangle for Project Title
            shape = 'triangle' if attribute == 'Project Title' else 'dot'

            net.add_node(descriptor, label=descriptor, color=node_color, size=node_size, shape=shape)
            net.add_edge(investigator, descriptor)
            
    # Generate the HTML content as a string
    html_content = net.generate_html()

    # Write the HTML content to a file with utf-8 encoding
    with open('knowledge_graph.html', 'w', encoding='utf-8') as file:
        file.write(html_content)

create_knowledge_graph(project_data, descriptors_data.columns)

# Display the graph in the Streamlit app
html_path = 'knowledge_graph.html'
try:
    with open(html_path, 'r', encoding='utf-8') as HtmlFile:
        html_content = HtmlFile.read()

    components.html(html_content, height=1000, width=1000)

except FileNotFoundError:
    st.warning(f"HTML file not found at {html_path}.")
except Exception as e:
    st.error(f"An error occurred while reading the HTML file: {e}")

# Details about filtering 
st.markdown("""
# Selecting a Node

- **Select a Node by ID**:
  - You can use the dropdown menu labeled "Select a Node by ID" to choose a specific node. This will highlight the node and its connections, helping you focus on a particular part of the graph. 
  - See [Guide to Possible Selection Choices below](#guide-to-possible-selection-choices)

- **Select a Network Item (Node)**:
  - When you select "node" from the "Select a network item" dropdown, you can then choose a property and value(s) to filter nodes based on those properties. For example, you might filter nodes to only show those with a specific label or color.

- **Node Properties**:
  - Properties you might filter on include label, color, size, etc.
  - Example: To highlight nodes with a specific research focus area, you can select label and type the specific focus area you're interested in.

# Selecting an Edge

- **Select a Network Item (Edge)**:
  - When you select "edge" from the "Select a network item" dropdown, you can choose properties related to the edges. This is useful for highlighting or filtering specific relationships in the graph.

- **Edge Properties**:
  - Properties for edges might include from (starting node), to (ending node), color, width, etc.
  - Example: You might filter edges to show only those connected to a particular node or of a specific color.

# Filtering and Resetting

- **Filter**:
  - After selecting the node or edge and specifying the properties, clicking the "Filter" button will apply the filter to the graph, highlighting the nodes or edges that match your criteria.

- **Reset Selection**:
  - Clicking "Reset Selection" will clear the current filter, returning the graph to its default state where all nodes and edges are visible.

# Practical Use Case

- **Highlight Specific Nodes**:
  - Let's say you want to highlight nodes related to a specific institution. You would:
    - Select "node" from "Select a network item".
    - Choose label from "Select a property".
    - Enter the institution name in "Select value(s)" and click "Filter".

- **Highlight Specific Edges**:
  - To highlight edges that connect to a specific project:
    - Select "edge" from "Select a network item".
    - Choose from or to from "Select a property".
    - Enter the project ID or name in "Select value(s)" and click "Filter".
""")

# Generate and display the guide table for possible selection choices
st.title('Guide to Possible Selection Choices')

unique_values = {column: descriptors_data[column].unique().tolist() for column in descriptors_data.columns}

for column, values in unique_values.items():
    st.subheader(column)
    for value in values:
        st.write(f"- {value}")