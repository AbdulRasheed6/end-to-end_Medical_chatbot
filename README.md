# end-to-end_Medical_chatbot

# How to run ?
### STEPS:

Clone the Repository

```bash
Project repo: https://github.com/
```

### STEP 01- Create a conda environment after opening the repository

```bash
conda create -n medicapp python=3.10 -y
```

```bash
conda activate medicapp
```




### STEP 02- install the requirements
```bash
pip install -r requirements.txt

```

### Create a .env file in the root directory add add your Pinecone and Gemini ai credentials as follows:

```
PINECONE_API_KEY= "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
GEMINI_API_KEY= "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```


```bash
# run the following command to store embedings to pinecone
python store_index.py
```


```bash
# Finally run the following command
python app.py
```

```bash
open up localhost:
```



### Techstack Used:


- Python
- LangChain
- Flask
- Gemini
- Pinecone


# AWS CICD-Deployment-with-Github-Actions

## 1. Login to AWS console

## 2. Create IAM user for deployment


   #with specific Access

   1. EC2 access: It is virtual machine
   2. ECR: Elastic Container Regustry to save your docker image in aws




   # Description : About the deployment
   1. Build docker image of the source code
   2. Push your docker image to ECR
   3. Launch Your EC2
   4. Pull your image from ECR in EC2
   5. Launch your docker image in EC2

   #Policy:
   1. AmazonEC2ContainerRegistryFullAccess
   2. AmazonEC2FullAccess


## 3. Create ECR repo to save ddocker image
    - save the URI: 474668388558.dkr.ecr.eu-north-1.amazonaws.com/medicbot


## 4. Create EC2 machine(ubuntu)

## 5. Open EC2 and install docker in EC2 Machine:


    #Optional
    sudo apt-get update -y
    sudo apt-get upgrade


    #required

    curl -fsSL https://get.docker.com -o get-docker.sh

    sudo sh get-docker.sh

    sudo usermod -aG docker Ubuntu

    newgrp docker


## 6. Configure EC2 as self-hosted runner:

   setting>action>runner>new self hosted runner> choose os > then run command one by one


## 7. Setup github secrets:



     - AWS_ACCESS_KEY_ID
     - AWS_SECRET_ACCESS_KEY
     - AWS_DEFAULT_REGION
     - PINECONE_API_KEY
     - GEMINI_API_KEY