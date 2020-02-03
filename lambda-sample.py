import boto3
import json
import urllib.parse
import time

print('Loading function')

s3 = boto3.client('s3') # this would be the origin bucket which will be connected automatically through the UI.
s3_destination = boto3.resource('s3').Bucket('DESTINATION-BUCKET') # Here goes the Destination S3 Bucket which is not referenced in the UI
textract_client = boto3.client('textract') # Standard Textract Call.

# Optional
SNS_TOPIC_ARN = 'arn:aws:sns:'
# Textract Call
ROLE_ARN = 'arn:aws:iam::123456789012:role/TextractRole'

# This function starts the Textract Job with the S3 information.
def startJob(s3BucketName, objectName):
    response = None
    client = boto3.client('textract')
    response = client.start_document_text_detection(
    DocumentLocation={
        'S3Object': {
            'Bucket': s3BucketName,
            'Name': objectName
        }
    })

    return response["JobId"]

# This function checks if the job has been completed by checking the STATUS of the ID.
def isJobComplete(jobId):
    time.sleep(3)
    client = boto3.client('textract')
    response = client.get_document_text_detection(JobId=jobId)
    status = response["JobStatus"]
    print("Job status: {}".format(status))

    while(status == "IN_PROGRESS"):
        time.sleep(3)
        response = client.get_document_text_detection(JobId=jobId)
        status = response["JobStatus"]
        print("Job status: {}".format(status))
    return status
    
# Below function supports pagination
def getJobResults(jobId):
    pages = []
    time.sleep(3)
    client = boto3.client('textract')
    response = client.get_document_text_detection(JobId=jobId)
    pages.append(response)
    print("Results page received: {}".format(len(pages)))
    nextToken = None
    if('NextToken' in response):
        nextToken = response['NextToken']
    while(nextToken):
        time.sleep(3)
        response = client.get_document_text_detection(JobId=jobId, NextToken=nextToken)
        pages.append(response)
        print("Results page received: {}".format(len(pages)))
        nextToken = None
        if('NextToken' in response):
            nextToken = response['NextToken']
    return pages


def lambda_handler(event, context):
    # First alert is not defined here - it comes from the Lambda Object Setup.
    # So the definition is by default.
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    try:
        # This gets the S3 Alert and does something with it.
        # Gets the content type - I leave it as I was learning with this function.
        response = s3.get_object(Bucket=bucket, Key=key)
        print("CONTENT TYPE: " + response['ContentType'])
        print(f'Document detection for {bucket}/{key}')
        
        # Then uses the bucket + key [filename] to call the functions above and use Textract directly.
        s3BucketName = bucket
        documentName = key
        jobId = startJob(s3BucketName, documentName)
        print("Started job with id: {}".format(jobId))
        # Uses the function and waits around 3 seconds to iterate. Can be customized further.
        if(isJobComplete(jobId)):
            respuest = getJobResults(jobId)
        # I think this will retrieve the document and the it will be cleaned up/JSON parsed.
        to_json = {'Document': key, 'ExtractedText': respuest, 'TextractJobId': jobId}
        json_content = json.dumps(to_json).encode('UTF-8')
        # I get an output name... ends up being .PDF.JSON but can be stripped if easier.
        output_file_name = str(key + ".json")
        # Save as Bytes in output S3 Object.
        s3_destination.Object(f'{output_file_name}').put(Body=bytes(json_content))
    except Exception as e:
        print(e)
