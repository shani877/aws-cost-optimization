import boto3
import datetime

def get_all_regions():
    return [r['RegionName'] for r in boto3.client('ec2').describe_regions()['Regions']]

def find_unattached_ebs(ec2):
    return [v['VolumeId'] for v in ec2.describe_volumes(Filters=[{'Name': 'status', 'Values': ['available']}])['Volumes']]

def find_unassociated_eips(ec2):
    return [e['PublicIp'] for e in ec2.describe_addresses()['Addresses'] if 'AssociationId' not in e]

def find_stopped_ec2_instances(ec2):
    reservations = ec2.describe_instances(Filters=[{'Name': 'instance-state-name', 'Values': ['stopped']}])['Reservations']
    return [i['InstanceId'] for r in reservations for i in r['Instances']]

def find_unused_security_groups(ec2):
    all_sgs = {s['GroupId'] for s in ec2.describe_security_groups()['SecurityGroups']}
    used_sgs = {g['GroupId'] for ni in ec2.describe_network_interfaces()['NetworkInterfaces'] for g in ni['Groups']}
    return list(all_sgs - used_sgs)

def find_unused_elbs(elb):
    elbs = elb.describe_load_balancers()['LoadBalancerDescriptions']
    return [e['LoadBalancerName'] for e in elbs if not e['Instances']]

def find_idle_nat_gateways(ec2):
    return [gw['NatGatewayId'] for gw in ec2.describe_nat_gateways(Filters=[{'Name': 'state', 'Values': ['available']}])['NatGateways']
            if not gw['NatGatewayAddresses'] or 'PrivateIp' not in gw['NatGatewayAddresses'][0]]

def find_stopped_rds_instances(rds):
    return [db['DBInstanceIdentifier'] for db in rds.describe_db_instances()['DBInstances']
            if db['DBInstanceStatus'] == 'stopped']

def find_low_usage_lambda(lambda_client, cw):
    response = lambda_client.list_functions()['Functions']
    low_usage = []
    for fn in response:
        fn_name = fn['FunctionName']
        try:
            metrics = cw.get_metric_statistics(
                Namespace='AWS/Lambda',
                MetricName='Invocations',
                Dimensions=[{'Name': 'FunctionName', 'Value': fn_name}],
                StartTime=datetime.datetime.utcnow() - datetime.timedelta(days=7),
                EndTime=datetime.datetime.utcnow(),
                Period=604800,
                Statistics=['Sum']
            )
            if not metrics['Datapoints'] or metrics['Datapoints'][0]['Sum'] == 0.0:
                low_usage.append(fn_name)
        except Exception:
            continue
    return low_usage

def find_idle_autoscaling_groups(asg):
    return [g['AutoScalingGroupName'] for g in asg.describe_auto_scaling_groups()['AutoScalingGroups']
            if not g['Instances']]

def main():
    for region in get_all_regions():
        print(f"\n=== Region: {region} ===")
        ec2 = boto3.client('ec2', region_name=region)
        elb = boto3.client('elb', region_name=region)
        rds = boto3.client('rds', region_name=region)
        lambda_client = boto3.client('lambda', region_name=region)
        cw = boto3.client('cloudwatch', region_name=region)
        asg = boto3.client('autoscaling', region_name=region)

        print("🔹 Unattached EBS Volumes:", find_unattached_ebs(ec2))
        print("🔹 Unassociated Elastic IPs:", find_unassociated_eips(ec2))
        print("🔹 Stopped EC2 Instances:", find_stopped_ec2_instances(ec2))
        print("🔹 Unused Security Groups:", find_unused_security_groups(ec2))
        print("🔹 Unused Classic Load Balancers:", find_unused_elbs(elb))
        print("🔹 Idle NAT Gateways:", find_idle_nat_gateways(ec2))
        print("🔹 Stopped RDS Instances:", find_stopped_rds_instances(rds))
        print("🔹 Lambda Functions with 0 invocations (7 days):", find_low_usage_lambda(lambda_client, cw))
        print("🔹 Idle Auto Scaling Groups (0 instances):", find_idle_autoscaling_groups(asg))

if __name__ == "__main__":
    main()
