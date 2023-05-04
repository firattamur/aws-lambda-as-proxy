# Remove existing zip file
rm -rf ./terraform/lambda/lambda.zip

# Change to the lambda directory and create a new zip file
pushd ./lambda
zip -r ../terraform/lambda/lambda.zip main.py
popd

# Initialize and apply Terraform configuration
pushd ./terraform
terraform init
terraform apply -auto-approve

# Save Terraform output to a JSON file
terraform output -json > output/lambda_functions.json
popd