import boto3

def find_unattached_ebs_volumes():
    ec2 = boto3.client('ec2')
    volumes = ec2.describe_volumes(Filters=[{'Name': 'status', 'Values': ['available']}])
    print("🔍 Unattached EBS Volumes:")
    for vol in volumes['Volumes']:
        print(f" - Volume ID: {vol['VolumeId']}, Size: {vol['Size']} GB")

def find_unassociated_elastic_ips():
    ec2 = boto3.client('ec2')
    addresses = ec2.describe_addresses()
    print("\n🔍 Unassociated Elastic IPs:")
    for addr in addresses['Addresses']:
        if 'InstanceId' not in addr:
            print(f" - EIP: {addr['PublicIp']}")

def find_stopped_ec2_instances():
    ec2 = boto3.client('ec2')
    instances = ec2.describe_instances(Filters=[
        {'Name': 'instance-state-name', 'Values': ['stopped']}
    ])
    print("\n🔍 Stopped EC2 Instances:")
    for reservation in instances['Reservations']:
        for instance in reservation['Instances']:
            print(f" - Instance ID: {instance['InstanceId']}")

def find_unattached_elbs():
    elb = boto3.client('elb')
    load_balancers = elb.describe_load_balancers()
    print("\n🔍 Classic ELBs with no instances:")
    for lb in load_balancers['LoadBalancerDescriptions']:
        if not lb['Instances']:
            print(f" - ELB Name: {lb['LoadBalancerName']}")

def find_idle_rds_instances():
    rds = boto3.client('rds')
    instances = rds.describe_db_instances()
    print("\n🔍 Idle RDS Instances (stopped or very low usage):")
    for db in instances['DBInstances']:
        if db['DBInstanceStatus'] == 'stopped':
            print(f" - RDS Instance ID: {db['DBInstanceIdentifier']} (stopped)")

def main():
    find_unattached_ebs_volumes()
    find_unassociated_elastic_ips()
    find_stopped_ec2_instances()
    find_unattached_elbs()
    find_idle_rds_instances()

if __name__ == "__main__":
    main()
#Note: Make sure python is installed and aws cli is configured.
