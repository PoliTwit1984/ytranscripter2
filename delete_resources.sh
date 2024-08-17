#!/bin/bash

# Loop through each line in resources.txt
while IFS= read -r resource_group; do
  if [ ! -z "$resource_group" ]; then
    echo "Deleting resource group: $resource_group"
    az group delete --name "$resource_group" --yes --no-wait
  fi
done < resources.txt
