import pandas as pd

# Load your input CSV (1 column: 'postcondition')
df = pd.read_csv('input.csv')
df['postcondition'] = df['postcondition'].str.strip()

# Extract the 'D3-XXX' technique part
df['technique'] = df['postcondition'].apply(lambda x: '-'.join(x.split('-')[:2]))

# Save to output file
df.to_csv('postconditions_with_technique_column.csv', index=False)

print("Done! Output saved to 'postconditions_with_technique_column.csv'")


#################################################
import pandas as pd

# Load the input CSV
df = pd.read_csv('input.csv')

# Strip any whitespace just in case
df['postcond'] = df['postcond'].str.strip()
df['matching_precond'] = df['matching_precond'].str.strip()

# Split the comma-separated list into individual rows
expanded_rows = []

for _, row in df.iterrows():
    post = row['postcond']
    preconds = [p.strip() for p in row['matching_precond'].split(',')]

    for pre in preconds:
        expanded_rows.append({'postcond': post, 'matching_precond': pre})

# Create the new DataFrame
expanded_df = pd.DataFrame(expanded_rows)

# Save to output CSV
expanded_df.to_csv('exploded_preconditions.csv', index=False)
print("Output saved to 'exploded_preconditions.csv'")

############################################################
!pip install graphistry pandas --quiet

import graphistry
import pandas as pd

graphistry.register(api=3, protocol='https', server='hub.graphistry.com', username='laasya', password='hS*UqWL7x%ZF')

# Load CSVs
nodes_df = pd.read_csv('graphistry-nodes.csv')
edges_df = pd.read_csv('graphistry-edges.csv')

# color by node type
node_style = {
    'technique': '#1f77b4',     # blue
    'precondition': '#ff7f0e',  # orange
    'postcondition': '#2ca02c'  # green
}
nodes_df['color'] = nodes_df['node_type'].map(node_style)

# plot
g = graphistry.bind(source='source', destination='target', node='node_id')
g = g.nodes(nodes_df).edges(edges_df)

g = g.encode_point_color('color')
# edge labels on hover: pass edge_label='edge_type' to the plot() call
g = g.encode_edge_color('edge_type')


g.plot()
