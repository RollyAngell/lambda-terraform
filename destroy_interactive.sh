#!/bin/bash

# Show the resources that will be destroyed
echo "Showing the resources that will be destroyed:"
terraform plan -destroy

echo ""
# Ask the user for confirmation before destroying resources
read -p "Do you want to continue and delete all these resources? (y/n): " confirm

if [[ "$confirm" == "y" || "$confirm" == "Y" ]]; then
    terraform destroy
else
    echo "Operation cancelled. No resources were deleted."
fi