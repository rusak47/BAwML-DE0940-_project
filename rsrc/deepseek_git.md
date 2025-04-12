#https://github.com/marketplace/models/azureml-deepseek/DeepSeek-V3-0324
https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/ai/azure-ai-inference/samples
#https://github.com/nvm-sh/nvm?tab=readme-ov-file#installing-and-updating
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.2/install.sh | bash

cat package.json
{
  "type": "module",
  "dependencies": {
    "@azure-rest/ai-inference": "latest",
    "@azure/core-auth": "latest",
    "@azure/core-sse": "latest"
  }
}
Open a terminal window in this folder and run npm install.

# check current version
nvm current

# if current is none, then install 
nvm install --list

#run sample
node sample.js

########### using python
pip install azure-ai-inference

import os
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential

endpoint = "https://models.inference.ai.azure.com"
model_name = "DeepSeek-V3-0324"
token = os.environ["GITHUB_TOKEN"]

client = ChatCompletionsClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(token),
)

response = client.complete(
    messages=[
        SystemMessage("You are a helpful assistant."),
        UserMessage("What is the capital of France?"),
    ],
    temperature=1.0,
    top_p=1.0
    max_tokens=1000,
    model=model_name
)

print(response.choices[0].message.content)

