import pandas
import boto3
import itertools
import os
from dotenv import load_dotenv
load_dotenv() 

def csvtosg():
    colnames = ['GroupId', 'GroupName', 'Type', 'IpProtocol', 'FromPort', 'ToPort', 'IpRanges', 'Ipv6Ranges', 'PrefixListIds', 'UserIdGroupPairs']
    data = pandas.read_csv('Dev.csv', names=colnames)
    groupid = data.GroupId.to_list()
    type = data.Type.to_list()
    ipprotocol = data.IpProtocol.to_list()
    fromport = data.FromPort.to_list()
    toport = data.ToPort.to_list()
    ipranges = data.IpRanges.to_list()
    ipv6ranges = data.Ipv6Ranges.to_list()
    prefixlistids = data.PrefixListIds.to_list()
    useridgrouppairs = data.UserIdGroupPairs.to_list()

    client = boto3.client('ec2',
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    aws_session_token=os.getenv("AWS_SESSION_TOKEN")
    )

    for (groupid,type,ipprotocol,fromport,toport,ipranges,ipv6ranges,prefixlistids,useridgrouppairs) in itertools.zip_longest(groupid,type,ipprotocol,fromport,toport,ipranges,ipv6ranges,prefixlistids,useridgrouppairs):
        print(type,ipprotocol,fromport,toport,ipranges,ipv6ranges,prefixlistids,useridgrouppairs)
        
        if(type == 'Inbound/Ingress'):
            response = client.authorize_security_group_ingress(
                GroupId=groupid,
                IpPermissions=[
                    {
                        'FromPort': int(fromport),
                        'IpProtocol': ipprotocol,
                        'IpRanges': [
                            {
                                'CidrIp': ipranges,
                                'Description': 'NA',
                            },
                        ],
                        'ToPort': int(toport),
                    },
                ],
            )
            print(response)

        if(type == 'Outbound/Egress'):
            response = client.authorize_security_group_egress(
                GroupId=groupid,
                IpPermissions=[
                    {
                        'FromPort': int(fromport),
                        'IpProtocol': ipprotocol,
                        'IpRanges': [
                            {
                                'CidrIp': ipranges,
                                'Description': 'NA',
                            },
                        ],
                        'ToPort': int(toport),
                    },
                ],
            )
            print(response)

csvtosg()
