import boto3
import face_recognition
import numpy as np
import cv2
import base64
import json

# Configurações do AWS DynamoDB
DYNAMO_TABLE = 'FaceRecognition'
dynamodb_client = boto3.client('dynamodb')

def handler(event, context):
    # Determinar o tipo de operação pela rota
    operation = event['resource']  # e.g., "/register" or "/recognize"
    if operation == "/register":
        return register(event)
    elif operation == "/recognize":
        return recognize(event)
    else:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Invalid operation"})
        }

def register(event):
    body = json.loads(event['body'])

    # Considerando que a imagem e o nome são enviados como base64 em um JSON
    image_base64 = body['image']
    image = base64.b64decode(image_base64)
    name = body['name']

    # Detectar face encodings
    image_np = np.frombuffer(image, np.uint8)
    image_np = cv2.imdecode(image_np, cv2.IMREAD_COLOR)
    face_encodings = face_recognition.face_encodings(image_np)

    if not face_encodings:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "No faces detected"})
        }

    # Armazenar imagem e encoding no DynamoDB
    dynamodb_client.put_item(
        TableName=DYNAMO_TABLE,
        Item={
            'name': {'S': name},
            'encoding': {'B': face_encodings[0].tobytes()},
            'image': {'S': image_base64}
        }
    )

    return {
        "statusCode": 200,
        "body": json.dumps({"message": "Face registered successfully!"})
    }

def recognize(event):
    body = json.loads(event['body'])
    
    # Considerando que a imagem é enviada como base64 em um JSON
    image_base64 = body['image']
    image = base64.b64decode(image_base64)
    
    # Detectar face encodings
    image_np = np.frombuffer(image, np.uint8)
    image_np = cv2.imdecode(image_np, cv2.IMREAD_COLOR)
    face_encodings = face_recognition.face_encodings(image_np)

    if not face_encodings:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "No faces detected"})
        }

    # Consultar encodings no DynamoDB
    response = dynamodb_client.scan(TableName=DYNAMO_TABLE)
    results = response['Items']

    known_encodings = [np.frombuffer(item['encoding']['B'], dtype=np.float64) for item in results]
    matches = face_recognition.compare_faces(known_encodings, face_encodings[0])
    
    if True in matches:
        match_index = matches.index(True)
        face_found = results[match_index]
        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Face recognized", "name": face_found['name']['S']})
        }
    else:
        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Face not recognized"})
        }
