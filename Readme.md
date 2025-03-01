# LLM-Powered Weather Chatbot deployed using AWS services

![Chatbot Demo](/images/Weather%20ChatBot.gif)

## Introduction
This project is an AI-powered chatbot built using **Gradio** and **OpenAI's GPT API**, deployed on **AWS** with **CloudFormation** and automated using **GitHub Actions**. The chatbot integrates LLM functions, external APIs, and secure authentication using **AWS Cognito**.

## Features
- 🤖 **LLM API Integration**: Executes dynamic function calls using OpenAI's API
- 🔐 **Secure Authentication**: AWS Cognito ensures user identity verification
- 🏗️ **Infrastructure as Code (IaC)**: Managed using AWS CloudFormation
- 🚀 **Automated Deployment**: CI/CD via GitHub Actions
- 🌐 **External API Calls**: Fetches real-time data (e.g., weather updates)
- 📈 **Scalability & Security**: Uses AWS Fargate, Secrets Manager, and security groups

## Architecture
![Architecture Diagram](/images/architecture.png)

### **Workflow Overview**
1. **User Authentication**: AWS Cognito verifies users
2. **Chatbot UI**: Built using Gradio
3. **LLM Execution**: Calls OpenAI's API for responses
4. **Security & Secrets Management**: Uses AWS Secrets Manager
5. **Deployment**: CloudFormation provisions infrastructure, automated by GitHub Actions

## Deployment Process
![Deployment Process](/images/trigger_deploy.png)

## Prerequisites
- **AWS Account** with required permissions
- **A domain name** from [freedomain.one](https://www.freedomain.one)
- **SSL Certificate** via AWS Certificate Manager (ACM)
- **GitHub Repository** configured with secrets for AWS authentication
- **Docker** installed for local testing
- **Python 3.x** with dependencies (`gradio`, `boto3`, `requests`, etc.)

## Deployment Steps

### 1️⃣ Set Up ACM Certificate
- Register a free domain from `freedomain.one`
- Issue an SSL certificate using AWS Certificate Manager
- Validate domain ownership through DNS records

### 2️⃣ Deploy Infrastructure
- Push CloudFormation templates to AWS
- Use GitHub Actions to automate deployment
- Monitor stack creation in AWS Console

### 3️⃣ Configure GitHub Repository
Set up repository secrets and variables for secure deployment:

![GitHub Secrets Configuration](/images/git_secret.png)
*Repository secrets for AWS credentials and API keys*

![GitHub Variables Configuration](/images/git_vars.png)
*Environment variables for deployment configuration*

### 4️⃣ Run the Application
After successful deployment, access your chatbot through the provided URL:

![Chatbot Application Interface](/images/app.png)
*Main chatbot interface with conversation history*

![Cognito Login Window](/images/login.png)
*Secure authentication via AWS Cognito*

- Authenticate using your Cognito credentials
- Interact with the chatbot through the intuitive Gradio UI
- Test various LLM functions and API integrations

## Installation & Local Setup
```sh
git clone https://github.com/your-repo/llm-chatbot.git
cd llm-chatbot
pip install -r requirements.txt
python app.py
```

## GitHub Actions Workflow
![Workflow](/images/deploy.png)

## Security Considerations
- 🔒 **Authentication**: AWS Cognito for user management
- 🔑 **Secrets Management**: API keys stored in AWS Secrets Manager
- 🛡️ **Network Security**: Uses security groups to restrict access
- 👤 **IAM Roles**: Grants least-privilege access to AWS resources

## Future Enhancements
- ✅ Add more LLM functions for enhanced automation
- ✅ Improve monitoring with AWS CloudWatch
- ✅ Optimize security configurations for better resilience
- ✅ Implement conversation history storage
- ✅ Add multi-language support
- ✅ Create custom UI themes

## Troubleshooting
| Issue | Solution |
|-------|----------|
| Authentication failures | Verify Cognito user pool configuration |
| Deployment errors | Check CloudFormation logs in AWS Console |
| API rate limiting | Implement request queuing mechanism |
| UI rendering issues | Verify Gradio version compatibility |

## Developer

<div align="center">
  <img src="https://img.shields.io/badge/Developer-K.%20Janarthanan-brightgreen?style=for-the-badge" alt="Developer"/>
</div>

## Blog & Resources

<div align="center">
  <a href="https://scripting4ever.wordpress.com/2025/03/01/building-an-llm-powered-weather-chatbot-deployed-on-aws/">
    <img src="https://img.shields.io/badge/Technical%20Blog-WordPress-blue?style=for-the-badge&logo=wordpress" alt="WordPress Blog"/>
  </a>
</div>

## Contributing
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License
[MIT License](LICENSE)

---
Happy coding! 🚀 Reach out if you have any questions.