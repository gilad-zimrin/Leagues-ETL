from os import getenv

from google.cloud import bigquery

# Create client (will use the default credentials & project you set)
client = bigquery.Client()

# Print the current project
print("Project ID:", client.project)

# List datasets in this project
datasets = list(client.list_datasets())

if datasets:
    print("Datasets in project:")
    for ds in datasets:
        print(" -", ds.dataset_id)
else:
    print("No datasets found in this project.")
