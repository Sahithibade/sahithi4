import boto3
import json
aws_access_key_id = '<AKIA53BDMR3LYGMEGNOC>'
aws_secret_access_key = '<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>'
aws_region = '<us-east-1>'

ec2_client = boto3.client('ec2', aws_access_key_id=aws_access_key_id,
                          aws_secret_access_key=aws_secret_access_key,
                          region_name=aws_region)

rds_client = boto3.client('rds', aws_access_key_id=aws_access_key_id,
                          aws_secret_access_key=aws_secret_access_key,
                          region_name=aws_region)

iam_client = boto3.client('iam', aws_access_key_id=aws_access_key_id,
                          aws_secret_access_key=aws_secret_access_key,
                          region_name=aws_region)

s3_client = boto3.client('s3', aws_access_key_id=aws_access_key_id,
                         aws_secret_access_key=aws_secret_access_key,
                         region_name=aws_region)

codepipeline_client = boto3.client('codepipeline', aws_access_key_id=aws_access_key_id,
                                   aws_secret_access_key=aws_secret_access_key,
                                   region_name=aws_region)

elasticbeanstalk_client = boto3.client('elasticbeanstalk', aws_access_key_id=aws_access_key_id,
                                       aws_secret_access_key=aws_secret_access_key,
                                       region_name=aws_region)
# set up parameters for EC2 instance
instance_type = 't2.micro'
ami_id = 'ami-1234567890abcdef0'
key_name = 'my-key-pair'
security_group_id = 'sg-12345678'
subnet_id = 'subnet-12345678'

# create EC2 instance
response = ec2_client.run_instances(ImageId=ami_id, InstanceType=instance_type,
                                    KeyName=key_name, SecurityGroupIds=[security_group_id],
                                    SubnetId=subnet_id)
instance_id = response['Instances'][0]['InstanceId']
# set up parameters for RDS instance
db_instance_identifier = 'my-db-instance'
db_name = 'mydatabase'
db_username = 'myuser'
db_password = 'mypassword'
db_instance_class = 'db.t2.micro'
db_engine = 'mysql'
db_port = 3306

# create RDS instance
response = rds_client.create_db_instance(DBInstanceIdentifier=db_instance_identifier,
                                          DBName=db_name, Engine=db_engine,
                                          EngineVersion='5.7.26', DBInstanceClass=db_instance_class,
                                          MasterUsername=db_username, MasterUserPassword=db_password,
                                          AllocatedStorage=20, Port=db_port)
# set up parameters for S3 bucket
bucket_name = 'my-bucket-name'
region = 'us-east-1'

# create S3 bucket
response = s3_client.create_bucket(Bucket=bucket_name,
                                   CreateBucketConfiguration={'LocationConstraint': region})
policy_document = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:GetObjectVersion",
                "s3:GetBucketVersioning",
                "s3:ListBucketVersions"
            ],
            "Resource": [
                "arn:aws:s3:::my-bucket/*"
            ]
        },
        {
            "Effect": "Allow",
            "Action": [
                "s3:PutObject"
            ],
            "Resource": [
                "arn:aws:s3:::my-bucket/*"
            ]
        },
        {
            "Effect": "Allow",
            "Action": [
                "elasticbeanstalk:*"
            ],
            "Resource": [
                "*"
            ]
        },
        {
            "Effect": "Allow",
            "Action": [
                "codedeploy:*"
            ],
            "Resource": [
                "*"
            ]
        }
    ]
}
role_name = 'my-codepipeline-role'

response = iam_client.create_role(RoleName=role_name,
                                  AssumeRolePolicyDocument=json.dumps({
                                      "Version": "2012-10-17",
                                      "Statement": [
                                          {
                                              "Effect": "Allow",
                                              "Principal": {
                                                  "Service": "codepipeline.amazonaws.com"
                                              },
                                              "Action": "sts:AssumeRole"
                                          }
                                      ]
                                  }))
role_arn = response['Role']['Arn']
response = iam_client.put_role_policy(RoleName=role_name, PolicyName='my-policy-name',
                                       PolicyDocument=json.dumps(policy_document))

