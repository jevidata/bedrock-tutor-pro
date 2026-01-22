import boto3
import json

client = boto3.client("bedrock-runtime", region_name="us-east-1")
MODEL_ID = "amazon.nova-lite-v1:0"

def main():
    body = {
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "text": (
                            "Eres un tutor del curso de Especialización en IA y Big Data. "
                            "Resume en 3 frases el objetivo del curso."
                        )
                    }
                ],
            }
        ],
        "inferenceConfig": {
            "maxTokens": 256,
            "temperature": 0.3,
        },
    }

    response = client.invoke_model(
        modelId=MODEL_ID,
        contentType="application/json",
        accept="application/json",
        body=json.dumps(body),
    )

    response_body = json.loads(response["body"].read())
    print(json.dumps(response_body, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
