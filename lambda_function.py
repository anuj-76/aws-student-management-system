def lambda_handler(event, context):

    for record in event.get("Records", []):

        bucket = record["s3"]["bucket"]["name"]
        file_name = record["s3"]["object"]["key"]

        print("New file uploaded!")
        print("Bucket:", bucket)
        print("File:", file_name)

    return {
        "statusCode": 200,
        "body": "File processed successfully"
    }
