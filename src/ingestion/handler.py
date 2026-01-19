import json
import boto3
import os
from datetime import datetime

s3_client = boto3.client('s3')
sqs_client = boto3.client('sqs')

BUCKET_NAME = os.environ.get('BUCKET_NAME', 'hipaa-patient-data-bucket')
QUARANTINE_QUEUE = os.environ.get('QUARANTINE_QUEUE_URL')

def lambda_handler(event, context):
    """
    Ingests patient data from API Gateway
    Validates basic structure and stores in S3
    """
    print(f"Received event: {json.dumps(event)}")
    
    try:
        body = json.loads(event.get('body', '{}'))
        
        if not validate_patient_data(body):
            return send_to_quarantine(body, "Validation failed")
        
        patient_id = body.get('id', 'unknown')
        timestamp = datetime.utcnow().strftime('%Y%m%d-%H%M%S')
        s3_key = f"raw-data/{timestamp}_{patient_id}.json"
        
        s3_client.put_object(
            Bucket=BUCKET_NAME,
            Key=s3_key,
            Body=json.dumps(body, indent=2),
            ServerSideEncryption='aws:kms',
            ContentType='application/json'
        )
        
        print(f"Successfully stored patient data: {s3_key}")
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps({
                'message': 'Patient data ingested successfully',
                's3_location': s3_key
            })
        }
        
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {str(e)}")
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Invalid JSON format'})
        }
        
    except Exception as e:
        print(f"Error processing request: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Internal server error'})
        }

def validate_patient_data(data):
    """
    Validate FHIR data - accepts both Patient resources and Bundles
    """
    resource_type = data.get('resourceType')
    
    # Accept FHIR Bundles (Synthea format)
    if resource_type == 'Bundle':
        if 'entry' not in data:
            print("Bundle missing 'entry' field")
            return False
        print(f"Valid FHIR Bundle with {len(data.get('entry', []))} entries")
        return True
    
    # Accept individual Patient resources
    if resource_type == 'Patient':
        if 'id' not in data:
            print("Patient missing 'id' field")
            return False
        print(f"Valid FHIR Patient resource")
        return True
    
    print(f"Invalid resourceType: {resource_type}")
    return False
def send_to_quarantine(data, reason):
    """
    Send invalid data to quarantine queue for review
    """
    if QUARANTINE_QUEUE:
        try:
            sqs_client.send_message(
                QueueUrl=QUARANTINE_QUEUE,
                MessageBody=json.dumps({
                    'data': data,
                    'reason': reason,
                    'timestamp': datetime.utcnow().isoformat()
                })
            )
            print(f"Sent to quarantine: {reason}")
        except Exception as e:
            print(f"Failed to send to quarantine: {str(e)}")
    
    return {
        'statusCode': 400,
        'body': json.dumps({
            'error': 'Data validation failed',
            'reason': reason
        })
    }



