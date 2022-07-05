import boto3
import botocore.client

client_s3 = boto3.client('s3')
buckets_dict: dict = client_s3.list_buckets()['Buckets']
bucket_names = [bucket['Name'] for bucket in buckets_dict]
bucket_tags = []
required_tags = {'Team', 'plr-cost-allocation', 'CreatedBy', 'CreatedFrom'}
last_string_len = 0
for i, bucket_name in enumerate(bucket_names):
    current_string = f'{i + 1}/{len(bucket_names)} : Current bucket: {bucket_name}'
    needed_spaces = last_string_len - len(current_string)
    if needed_spaces < 0:
        needed_spaces = 0
    print(current_string + ' ' * needed_spaces, end='\r')
    tags_dict = dict.fromkeys(required_tags, 'None')
    try:
        tags: list = client_s3.get_bucket_tagging(Bucket=bucket_name)['TagSet']
        for tag in tags:
            tag_name, tag_value = tag['Key'], tag['Value']
            if tag_name in required_tags:
                tags_dict[tag_name] = tag_value

    except (botocore.client.ClientError, Exception) as e:
        continue
    finally:
        bucket_tags.append((bucket_name, tags_dict))
        last_string_len = len(current_string)

print('\n' + ', '.join(['bucket', *required_tags]))
for bucket_name, tags in bucket_tags:
    print(', '.join([bucket_name, *tags.values()]))
