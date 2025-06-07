import boto3
import csv
import io
import os
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    s3 = boto3.client('s3')

    input_bucket = os.environ.get('INPUT_BUCKET')
    input_key = os.environ.get('INPUT_KEY')
    output_key = os.environ.get('OUTPUT_KEY')

    logger.info(f"Procesando archivo: s3://{input_bucket}/{input_key}")

    try:
        response = s3.get_object(Bucket=input_bucket, Key=input_key)
        content = response['Body'].read().decode('utf-8')
        lines = content.splitlines()
        reader = csv.DictReader(lines)
    except Exception as e:
        logger.error(f"Error al leer el archivo de entrada: {e}")
        return {
            'statusCode': 500,
            'body': f'Error al leer el archivo de entrada: {e}'
        }

    summary = {}
    row_count = 0
    for row in reader:
        try:
            region = row['region']
            sales = float(row['sales'])
            if region not in summary:
                summary[region] = {'total': 0, 'count': 0}
            summary[region]['total'] += sales
            summary[region]['count'] += 1
            row_count += 1
        except Exception as e:
            logger.warning(f"Fila inválida: {row} - Error: {e}")

    logger.info(f"Filas procesadas correctamente: {row_count}")

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['region', 'average_sales'])
    for region, data in summary.items():
        avg = data['total'] / data['count']
        writer.writerow([region, round(avg, 2)])

    try:
        s3.put_object(Bucket=input_bucket, Key=output_key, Body=output.getvalue())
        logger.info(f"Resumen guardado en: s3://{input_bucket}/{output_key}")
    except Exception as e:
        logger.error(f"Error al guardar el archivo de salida: {e}")
        return {
            'statusCode': 500,
            'body': f'Error al guardar el archivo de salida: {e}'
        }

    return {
        'statusCode': 200,
        'body': f'Summary saved to s3://{input_bucket}/{output_key}'
    }