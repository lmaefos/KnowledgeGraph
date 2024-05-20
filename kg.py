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

# Check the columns in the DataFrame
st.write(descriptors_data.columns)
st.write(descriptors_data.head())  # Print the first few rows of the DataFrame to verify data

# Convert DataFrame to a list of lists with all entries as strings
project_data = descriptors_data.astype(str).values.tolist()

# Define a color mapping for each column header
color_map = {
    'Project #': '#e07c3e',           # Orange
    'Application Type': '#ff7f0e',
    'Project Title': '#1f77b4',       # Blue
    'Research Focus Area': '#2ca02c', # Green
    'Administering IC(s)': '#9467bd', # Purple
    'Institution': '#8c564b',
    'Investigator': '#e377c2',
    'Location': '#7f7f7f',
    'Year Awarded': '#bcbd22'
}

# Create a Network graph object
net = Network(notebook=True, width="1000px", height="600px", cdn_resources='remote', font_color='white', bgcolor="black", select_menu=True, filter_menu=True)
st.title('Knowledge Graph of BRIM Projects')

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
        project_id = entry[0]  # Assuming 'Project #' is the first column
        net.add_node(project_id, label=project_id, color=color_map['Project #'])

        for attribute, descriptor in zip(columns[1:], entry[1:]):
            frequency = descriptor_frequency[descriptor]
            node_size = scaling_factor * (frequency / max_frequency)
            node_color = color_map.get(attribute, '#982568')  # Default to purple if not found
            net.add_node(descriptor, label=descriptor, color=node_color, size=node_size)
            net.add_edge(project_id, descriptor)

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