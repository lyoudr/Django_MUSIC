## Use Docker Compose to define containers

Architecture diagram
![alt text](https://gitlab.com/lyoudr/music_server/-/blob/ecs/ecs_architecture.png)

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
      - AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID
      - AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY
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
      - AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID
      - AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY
      - AWS_STORAGE_BUCKET_NAME=lyoudrmusic
```

### 4. Add ecs-params.yml to define the memory and CPU usage of your container
- cpu_shares : cpu your container can use
- mem_limit : memory limit
- docker_volumes : docker volume used

```
version : 1
task_definition :
  ecs_network_mode : awsvpc
  task_execution_role : ecsTaskExecutionRole
  task_size :
    mem_limit : 0.5GB
    cpu_limit : 256
  services:
    postgres_db : 
      cpu_shares : 80
      mem_limit : 300MB

    ann_server_1 :
      cpu_shares : 80
      mem_limit : 300MB
      # set "depends_on" in ecs-params instead of setting in docker-copmose.yml
      depends_on : 
        - container_name : postgres_db
          condition : HEALTHY
    nginx :
      cpu_shares : 80
      mem_limit : 300MB
      depends_on:
        - container_name : ann_server_1
          condition : HEALTHY
run_params:
  network_configuration:
    awsvpc_configuration:
      subnets:
        - "subnet ID 1"
        - "subnet ID 2"
      security_groups:
        - "security group ID"
      assign_public_ip : ENABLED
```

-----
## Create Cluster , Deploy task to Elastic Container Service (ECS)

This tutorial shows you how to set up a cluster and deploy a task using the EC2 launch type.

### 1. Create the Task Execution IAM Role
- Create a file namme "task-execution-assume-role.json" with the following contents:
```
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "",
      "Effect": "Allow",
      "Principal": {
        "Service": "ecs-tasks.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
```
- Create the task execution role:
```
aws iam --region ap-northeast-1 create-role --role-name ecsTaskExecutionRole --assume-role-policy-document file://task-execution-assume-role.json
```
- Attach the task execution role policy:
```
aws iam --region ap-northeast-1 attach-role-policy --role-name ecsTaskExecutionRole --policy-arn arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy
```

### 2. Configure the AWS ECS CLI

- [Install ecs-cli](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ECS_CLI_installation.html)
- Create cluster configuration, which defines the AWS region to use, resource createtion prefixes, nd the cluster name to use with the Amazon ECS CLI:
```
ecs-cli configure --cluster music --default-launch-type FARGATE --config-name music-config --region ap-northeast-1
```
- Create a profile using your access key and secret key
```
ecs-cli configure profile --access-key AWS_ACCESS_KEY_ID --secret-key AWS_SECRET_ACCESS_KEY --profile-name music-profile
```

### 3. Create Cluster and Configure the Security Group

- Because you specified Fargate as your default launch type in the cluster configuration, this command creates an empty cluster and a VPC configured with two public subnets.

```
ecs-cli up --cluster-config music-config --ecs-profile music-profile
```
The output of this command contains the VPC and subnet IDs that are created. Take note of these IDs as they are used later.

- Using the AWS CLI, retrieve the default security group ID for the VPC. Use the VPC ID from the previous output:
```
aws ec2 describe-security-groups --filters Name=vpc-id, Values=VPC_ID --region ap-northeast-1
```

- Using AWS CLI, add a security group rule to allow inbound access on port 80:
```
aws ec2 authorize-security-group-ingress --group-id security_group_id --protocol tcp --port 80 --cidr 0.0.0.0/0 --region ap-northeast-1
```

### 4. Deploy the Compose File to a Cluster
- After you create the compose file, you can deploy it to your cluster with ecs-cli compose service up. By default, the command looks for files called **docker-compose.yml** and **ecs-params.yml** in the current directory
```
ecs-cli compose --project-name music service up --create-log-groups --cluster-config music-config --ecs-profile music-profile
```

- Deploy compose file with Elastic Load Balancer (application load balancer) created before , --target-group-arn (enter the target group arn in this load balancer)
```
ecs-cli compose --project-name music service up --cluster-config music --ecs-profile music --target-group-arn arn:aws:elasticloadbalancing:ap-northeast-1:520106466788:targetgroup/music/302aa40515d42364 --container-name nginx --container-port 80
```

- Scale the Tasks on the Cluster
You can scale up your task count to increase the number of instances of your application with ecs-cli compose service scale.
```
ecs-cli compose --project-name music service scale 2 --cluster-config music --ecs-profile music
```



### 5. Create ECS Service by AWS CLI
- The first time to create a cluster
```
  aws ecs create-cluster \
      --cluster-name music \
      --capacity-providers FARGATE
```
- The first time create task definition
```
  ecs-cli compose \
    --file docker-compose.yml \
    --ecs-params ecs-params.yml \
    --region ap-northeast-1 \
    create \
    --launch-type FARGATE
```

- The first time to create service 
```
  aws ecs create-service \
  --cluster music \
  --service-name music \
  --task-definition music:123 \
  --desired-count 1 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[subnet-09404f0b49797d74e, subnet-051007b1fde1ea43b], securityGroups=[sg-0e84dd0849b3fc954], assignPublicIp=ENABLED}" \
  --load-balancers "loadBalancerName=musicnew, containerName=nginx, containerPort=80"
```

- Update Service each time push to gitlab
```
  aws ecs update-service \
  --cluster music \
  --service music \
  --desired-count 1 \
  --force-new-deployment
```
