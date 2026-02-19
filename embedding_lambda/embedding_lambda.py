import json
import os
import boto3
import requests
from openai import OpenAI


# Load OpenAI client
openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))


# Verify reCAPTCHA function
def verify_recaptcha(token: str, secret_key: str) -> dict:
    """Verify reCAPTCHA token with Google."""
    try:
        response = requests.post(
            'https://www.google.com/recaptcha/api/siteverify',
            data={
                'secret': secret_key,
                'response': token
            }
        )
        result = response.json()
        
        # Check if verification was successful and score is acceptable
        if result.get('success') and result.get('score', 0) >= 0.5:
            return {'valid': True, 'score': result.get('score')}
        else:
            return {'valid': False, 'reason': result}
    except Exception as e:
        return {'valid': False, 'error': str(e)}


def handler(event, context):
    """
    Handle both embedding and reCAPTCHA verification.
    
    For embedding:
        Input: {"action": "embed", "query": "text"}
        Output: {"embedding": [...]}
    
    For reCAPTCHA:
        Input: {"action": "verify_recaptcha", "token": "...", "secret_key": "..."}
        Output: {"valid": true/false, "score": 0.9}
    """
    try:
        action = event.get('action', 'embed') 
        
        if action == 'verify_recaptcha':
            token = event['token']
            secret_key = event['secret_key']
            result = verify_recaptcha(token, secret_key)
            return {
                'statusCode': 200,
                **result
            }
        
        elif action == 'embed':
            query = event['query']
            
            response = openai_client.embeddings.create(
                input=query,
                model="text-embedding-3-small"
            )
            
            embedding = response.data[0].embedding
            
            return {
                'statusCode': 200,
                'embedding': embedding
            }
        
        else:
            return {
                'statusCode': 400,
                'error': f'Unknown action: {action}'
            }
            
    except Exception as e:
        return {
            'statusCode': 500,
            'error': str(e)
        }