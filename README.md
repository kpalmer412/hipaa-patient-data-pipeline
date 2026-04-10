# HIPAA-Compliant Patient Data Ingestion Pipeline

AWS-based serverless pipeline for ingesting, validating, and storing FHIR patient data with HIPAA compliance features.

## Architecture

- **API Gateway**: RESTful endpoint for data ingestion
- **Lambda**: Validates and processes patient data
- **S3**: Encrypted storage with versioning
- **SQS**: Quarantine queue for invalid data
- **KMS**: Encryption at rest

## Features

✅ FHIR patient data validation  
✅ Encryption at rest (KMS) and in transit (TLS)  
✅ Automatic quarantine for invalid data  
✅ S3 versioning for audit trail  
✅ CloudWatch logging  
✅ Scalable and fault-tolerant architecture  

## Prerequisites

- AWS Account (Free Tier)
- AWS CLI configured
- AWS SAM CLI installed
- Python 3.11+

## Deployment
```bash
# Build
sam build --template infrastructure/template.yaml

# Deploy
sam deploy --guided
```

## Testing

Send test patient data:
```bash
curl -X POST https://YOUR-API-ENDPOINT/ingest \
  -H "Content-Type: application/json" \
  -d @test-data/sample-patient.json
```

## Project Structure
```
hipaa-pipeline/
├── src/ingestion/          # Lambda function code
├── infrastructure/         # SAM templates
├── test-data/             # Synthetic patient data
└── tests/                 # Unit tests
```

## Domain 2 (SAA) Coverage

- **Scalability**: API Gateway + Lambda auto-scaling
- **High Availability**: Multi-AZ S3, Lambda
- **Fault Tolerance**: SQS buffering, retry logic
- **Disaster Recovery**: S3 versioning, backups
- **Loose Coupling**: Event-driven, microservices

## Author

Ken Palmer - AWS Solutions Architect Certified , HCLS Cloud Engineer 

Healthcare Technology Professional | AWS Cloud Institute Graduate
