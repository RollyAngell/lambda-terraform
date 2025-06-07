import boto3
import csv
import io
import os

def lambda_handler(event, context):
    s3 = boto3.client('s3')

    input_bucket = os.environ['INPUT_BUCKET']
    input_key = os.environ['INPUT_KEY']
    output_key = os.environ['OUTPUT_KEY']

    response = s3.get_object(Bucket=input_bucket, Key=input_key)
    content = response['Body'].read().decode('utf-8')
    lines = content.splitlines()
    reader = csv.DictReader(lines)

    summary = {}
    for row in reader:
        region = row['region']
        sales = float(row['sales'])
        if region not in summary:
            summary[region] = {'total': 0, 'count': 0}
        summary[region]['total'] += sales
        summary[region]['count'] += 1

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['region', 'average_sales'])
    for region, data in summary.items():
        avg = data['total'] / data['count']
        writer.writerow([region, round(avg, 2)])

    s3.put_object(Bucket=input_bucket, Key=output_key, Body=output.getvalue())

    return {
        'statusCode': 200,
        'body': f'Summary saved to s3://{input_bucket}/{output_key}'
    }