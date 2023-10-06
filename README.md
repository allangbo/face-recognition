# face-recognition

O repositório `face-recognition` contém uma solução de reconhecimento facial baseada em AWS Lambda, AWS DynamoDB, AWS API Gateway e AWS ECR.

## Estrutura do Repositório

├── Dockerfile
├── lambda_function.py
└── requirements.txt


## Como compilar a imagem Docker e carregá-la no ECR da AWS

1. **Autenticação no AWS ECR**:

aws ecr get-login-password --region <YOUR_REGION> | docker login --username AWS --password-stdin <YOUR_ECR_REPO_URL>

Substitua `<YOUR_REGION>` pela região da AWS em que o ECR foi criado.
Substitua `<YOUR_ECR_REPO_URL>` pela url do repositório ECR

2. **Construir a imagem Docker**:

docker build -t face-recognition .

3. **Taggear a imagem para o ECR**:

docker tag face-recognition:latest <YOUR_ECR_REPO_URL>:latest

Substitua `<YOUR_ECR_REPO_URL>` pelo URL do repositório ECR.

4. **Enviar a imagem para o ECR**:

docker push <YOUR_ECR_REPO_URL>:latest

## Como criar e implementar a Lambda usando a imagem do ECR

1. Vá para o AWS Lambda e clique em "Criar função".
2. Escolha "Container Image".
3. Forneça o nome da função e selecione a imagem do ECR que acabou de ser enviada.
5. Complete a criação da função.

## Como configurar o AWS API Gateway

1. **Crie um novo recurso API**:

Crie um recurso chamado "register".

2. **Defina um novo método POST para "register"**:

Conecte este método à função Lambda criada anteriormente.

3. **Crie um segundo recurso chamado "recognize"**:

E defina um novo método POST para ele. Conecte-o à mesma função Lambda.

## Usando a API

- **Register**:
Faça uma chamada POST para o endpoint `/register` com um corpo JSON contendo `name` (nome da pessoa) e `image` (imagem codificada em base64).

- **Recognize**:
Faça uma chamada POST para o endpoint `/recognize` com um corpo JSON contendo `image` (imagem codificada em base64).