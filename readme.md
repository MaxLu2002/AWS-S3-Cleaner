# AWS S3 Bucket Cleanup Lambda Deployment Project

This project provides a highly efficient and flexible AWS Lambda solution for cleaning up S3 buckets. It supports Terraform deployment, allowing you to quickly create or remove the service as needed.

## Features
- **Flexible Configuration**: Choose to retain specific buckets or delete designated ones.
- **Regional Selection**: Specify the AWS region where the cleanup should be performed.
- **Simple Setup**: All cleanup-related configurations are managed in `config.py`.
- **Terraform Integration**: Deploy and remove the service quickly using Terraform.

## Deployment Methods

This project offers two ways to execute the S3 bucket cleanup Lambda:

### Method 1: Deploying with Terraform
1. Navigate to the `./env_prod` directory.
```bash
cd ./env_prod
```

2. Replace your AWS user profile in `provider.tf`.

3. Set the desired tag name in `terraform.tfvars`, such as `2025-test`.

4. Deploy the Lambda function using Terraform.
```bash
terraform init; terraform validate; terraform plan; terraform apply -auto-approve
```

5. Once deployed, go to the AWS Lambda console and modify the cleanup settings in `config.py`:
   - **BUCKET_PROCESSING**:
     - `"RETAIN"`: Retain specified S3 buckets.
     - `"DELETE"`: Delete specified S3 buckets.
   - **PREFIX**: Apply the cleanup process to buckets with the specified prefix.
   - **REGION**: Define the AWS region where the cleanup should take place.

6. Execute the Lambda function from the AWS console to complete the cleanup process.

### Method 2: Manually Creating the Lambda in AWS Console
1. Manually create a Lambda function in the AWS Lambda console.
2. Navigate to the `./lambda/` directory and copy all code files into the Lambda function.
3. Modify the cleanup settings in `config.py` (same as in Method 1).
4. Execute the Lambda function to perform the S3 bucket cleanup.

## Conclusion
This project provides a streamlined solution for managing S3 bucket cleanup using Terraform for automated deployment while allowing manual configuration for flexible adjustments. Whether you deploy using Terraform or create the Lambda function manually in the AWS console, you can easily manage your S3 bucket cleanup process.
