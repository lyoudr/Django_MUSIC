## Use Docker Compose to define containers

### 1. Write your docker-copmose.yml file

- can only use **image** when deploying to ECS, so build dockerfile locally first
- use **links** to link services instead of **depends_on**

```
  ann_server_1:
    
    build :
      context : .
      dockerfile: ./docker/config/Dockerfile

    environment:
      - ENV=prod 
      - STATIC_ROOT=/music/static/
      - DB_HOST=postgres_db
      - DB_NAME=music
      - DB_USER=ann
      - DB_PASSWORD=GxXynskDj134yi7P
      - AWS_ACCESS_KEY_ID=AKIAXSGGC3XSBLLMV4JY
      - AWS_SECRET_ACCESS_KEY=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
      - AWS_STORAGE_BUCKET_NAME=lyoudrmusic
    links:
      - postgres_db

    restart : always
    volumes : 
      - static-content:/music/static
      - media-content:/tmp/media

```

### 2. Push to dockerHub

```
docker build -t ann_server_1 .
docker login -u *** -p ****
docker tag music_ann_server_1:latest lyoudr/music_public:music_1
docker push lyoudr/music_public:music_1
```

### 3. Modify server to use image instead of build

- replace **build** with **image** (which pulled from DockerHub)
- add **logging** to log your docker container log on AWS CloudWatch

```
  ann_server_1:
    
    image : lyoudr/music_public:music_1

    logging :
      driver : awslogs
      options : 
        awslogs-group : music
        awslogs-region : ap-northeast-1
        awslogs-stream-prefix : ann_server_1

    environment:
      - ENV=prod 
      - STATIC_ROOT=/music/static/
      - DB_HOST=postgres_db
      - DB_NAME=music
      - DB_USER=ann
      - DB_PASSWORD=GxXynskDj134yi7P
      - AWS_ACCESS_KEY_ID=AKIAXSGGC3XSBLLMV4JY
      - AWS_SECRET_ACCESS_KEY=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
      - AWS_STORAGE_BUCKET_NAME=lyoudrmusic

    links:
      - postgres_db

    restart : always
    volumes : 
      - static-content:/music/static
      - media-content:/tmp/media

```

-----
## Create Cluster , Deploy task to Elastic Container Service (ECS)

This tutorial shows you how to set up a cluster and deploy a task using the EC2 launch type.


### 1. Configure the AWS ECS CLI

- [Install ecs-cli](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ECS_CLI_installation.html)
- Create cluster configuration 
```
ecs-cli configure --cluster ec2-tutorial --default-launch-type EC2 --config-name ec2-tutorial --region us-west-2
```
- Create a profile using your access key and secret key
```
ecs-cli configure profile --access-key AWS_ACCESS_KEY_ID --secret-key AWS_SECRET_ACCESS_KEY --profile-name ec2-tutorial-profile
```

### 2. Create Cluster
```
ecs-cli up --keypair id_rsa --capability-iam --size 1 --instance-type t2.micro--cluster-config ec2-tutorial --ecs-profile ec2-tutorial-profile
```

### 3. Deploy the Compose File to a Cluster
- go to the directory where your docker-compose.yml resides
```
ecs-cli compose up --create-log-groups --cluster-config ec2-tutorial --ecs-profile ec2-tutorial-profile
```

### 4. Create ECS Service from a Compose File

- stop running container first
```
ecs-cli compose down --cluster-config ec2-tutorial --ecs-profile ec2-tutorial-profile
```
- create service using compose file
```
```
ecs-cli compose service up --cluster-config ec2-tutorial --ecs-profile ec2-tutorial-profile
```