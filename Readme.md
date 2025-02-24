# LLM-Powered Chatbot with AWS & GitHub Actions

## Introduction
This project is an AI-powered chatbot built using **Gradio** and **OpenAI's GPT API**, deployed on **AWS** with **CloudFormation** and automated using **GitHub Actions**. The chatbot integrates LLM functions, external APIs, and secure authentication using **AWS Cognito**.

## Features
- **LLM Agent Integration**: Executes dynamic function calls using OpenAI's API.
- **Secure Authentication**: AWS Cognito ensures user identity verification.
- **Infrastructure as Code (IaC)**: Managed using AWS CloudFormation.
- **Automated Deployment**: CI/CD via GitHub Actions.
- **External API Calls**: Fetches real-time data (e.g., weather updates).
- **Scalability & Security**: Uses AWS Fargate, Secrets Manager, and security groups.

## Architecture
### **Workflow Overview**
1. **User Authentication**: AWS Cognito verifies users.
2. **Chatbot UI**: Built using Gradio.
3. **LLM Execution**: Calls OpenAI’s API for responses.
4. **Security & Secrets Management**: Uses AWS Secrets Manager.
5. **Deployment**: CloudFormation provisions infrastructure, automated by GitHub Actions.

![Architecture Diagram](https://via.placeholder.com/800x400) *(Replace with actual diagram)*

## Prerequisites
- **AWS Account** with required permissions.
- **A domain name** from [freedomain.one](https://www.freedomain.one).
- **SSL Certificate** via AWS Certificate Manager (ACM).
- **GitHub Repository** configured with secrets for AWS authentication.
- **Docker** installed for local testing.
- **Python 3.x** with dependencies (`gradio`, `boto3`, `requests`, etc.).

## Deployment Steps
### 1️⃣ Set Up ACM Certificate
- Register a free domain from `freedomain.one`.
- Issue an SSL certificate using AWS Certificate Manager.

### 2️⃣ Deploy Infrastructure
- Push CloudFormation templates to AWS.
- Use GitHub Actions to automate deployment.

### 3️⃣ Run the Application
- Authenticate via Cognito.
- Interact with the chatbot using Gradio UI.

## Installation & Local Setup
```sh
git clone https://github.com/your-repo/llm-chatbot.git
cd llm-chatbot
pip install -r requirements.txt
python app.py
```

## GitHub Actions Workflow
```yaml
on:
  push:
    branches:
      - main
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v3
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v2
        with:
          aws-region: us-east-1
      - name: Deploy CloudFormation Stack
        run: aws cloudformation deploy --template-file cloudformation.yml --stack-name LLMChatbot
```

## Security Considerations
- **Authentication**: AWS Cognito for user management.
- **Secrets Management**: API keys stored in AWS Secrets Manager.
- **Network Security**: Uses security groups to restrict access.
- **IAM Roles**: Grants least-privilege access to AWS resources.

## Future Enhancements
✅ Add more LLM functions for enhanced automation.
✅ Improve monitoring with AWS CloudWatch.
✅ Optimize security configurations for better resilience.

## Contributing
Feel free to submit PRs for improvements! 🚀

## License
[MIT License](LICENSE)

---
Happy coding! 🚀 Reach out if you have any questions.

