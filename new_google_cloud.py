import random
import time
from googleapiclient import discovery
from google_auth_oauthlib.flow import InstalledAppFlow


#向 Google Cloud API 进行身份验证
SCOPES = ['https://www.googleapis.com/auth/cloud-platform']
flow = InstalledAppFlow.from_client_secrets_file(
    'client_secret.json', SCOPES)#这一块请自行上网寻找相关资料，谷歌服务器和其他服务器不同的地方在于，它不需要token，而是通过和本地主机建立一个客户端信任，用户在谷歌页面上同意之后才能自动申请服务器

creds = flow.run_local_server(port=0)

# 构建 Compute Engine API 客户端
service = discovery.build('compute', 'v1', credentials=creds)

#创建服务器（大约需要四~五分钟）
def createserver(instance_name):
    project = 'massive-bliss-376404'
    zons = ['us-west4-c','us-west4-b','us-west4-a','us-west3-c','us-west3-b','us-west3-a','us-west2-c','us-west2-b',
            'us-west2-a','us-west1-c','us-west1-b','us-west1-a','us-south1-c','us-south1-b','us-south1-a','us-east5-c',
            'us-east5-b','us-east5-a','us-east4-c','us-east4-b','us-east4-a','us-east1-d','us-east1-c','us-east1-b',
            'us-central1-f','us-central1-c','us-central1-b','us-central1-a','southamerica-east1-c','southamerica-east1-b',
            'southamerica-east1-a','northamerica-northeast1-c','northamerica-northeast1-b','northamerica-northeast1-a',
            'me-west1-c','me-west1-b','me-west1-a','europe-west9-c','europe-west9-b','europe-west9-a','europe-west8-c',
            'europe-west8-b','europe-west8-a','europe-west6-c','europe-west6-b','europe-west6-a','europe-west4-c','europe-west4-b',
            'europe-west4-a','europe-west3-c','europe-west3-b','europe-west3-a','europe-west2-c','europe-west2-b','europe-west2-a',
            'europe-west1-d','europe-west1-c','europe-west1-b','europe-southwest1-c','europe-southwest1-b','europe-southwest1-a',
            'europe-north1-c','europe-north1-b','europe-north1-a','europe-central2-c','europe-central2-b','europe-central2-a',
            'australia-southeast1-c','australia-southeast1-b','australia-southeast1-a','asia-southeast2-c','asia-southeast2-b',
            'asia-southeast2-a','asia-southeast1-c','asia-southeast1-b','asia-southeast1-a','asia-south1-c','asia-south1-b',
            'asia-south1-a','asia-northeast3-c','asia-northeast3-b','asia-northeast3-a','asia-northeast2-c','asia-northeast2-b',
            'asia-northeast2-a','asia-northeast1-c','asia-northeast1-b','asia-northeast1-a','asia-east2-c','asia-east2-b',
            'asia-east2-a','asia-east1-c','asia-east1-b','asia-east1-a']
    zone = zons[random.randint(0, 93)]
    instance_config = {
        'name': instance_name,
        'machineType': f'/compute/v1/projects/{project}/zones/{zone}/machineTypes/n1-standard-1',
        'disks': [
            {
                'boot': True,
                'autoDelete': True,
                'initializeParams': {
                    'sourceImage': 'projects/ubuntu-os-cloud/global/images/family/ubuntu-2004-lts',
                }
            }
        ],
        'networkInterfaces': [
            {
                'network': f'/compute/v1/projects/{project}/global/networks/default',
                'accessConfigs': [
                    {
                        'type': 'ONE_TO_ONE_NAT',
                        'name': 'External NAT'
                    }
                ]
            }
        ],
    }
    try:
        operation = service.instances().insert(
            project=project,
            zone=zone,
            body=instance_config
        ).execute()
    except:
        print("没创建成功？？")
        return
    time.sleep(15)
    print(f"成功创建{instance_name}")

    result = service.instances().list(project=project, zone=zone).execute()


    for instance in result['items']:
        name = instance['name']
        network_interfaces = instance.get('networkInterfaces', [])
        for network_interface in network_interfaces:
            access_configs = network_interface.get('accessConfigs', [])
            for access_config in access_configs:
                ip_address = access_config.get('natIP')
                #print(ip_address)

    return ip_address,operation,zone

def breakserver(instance_name,zone):
    project = 'XXXXXX'
    operation = service.instances().delete(
        project=project,
        zone=zone,
        instance=instance_name
    ).execute()
    print(f"已成功删除 ID: {instance_name}")
    return operation



for i in range(0,300):#先搞2轮，目的是5000/3
    # try:
    name=['aa','bb','cc','dd','ee','ff','gg','hh','ii','jj','kk']
    qq = name[random.randint(0, 10)]
    print(f"第{i}次轮回")
    try:
        ip, operation, zone = createserver(qq)  # 创建服务器并返回ip和SUBID
    except:
        print("跳过吧，应该是没有这个地区了")
        continue
    print(ip)

    try:
        breakserver(qq,zone)
    except:
        while True:
            print("还是删不掉，等20s后再试一次！")
            time.sleep(20)
            try:
                breakserver(qq,zone)
                break
            except:
                continue
