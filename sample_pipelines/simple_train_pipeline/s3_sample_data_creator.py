import pickle, gzip, numpy, urllib.request, json, io
from urllib.parse import urlparse
import boto3

###################################################################
# This is the only thing that you need to change to run this code 
# Give the name of your S3 bucket 
bucket = 'kfp-simple-train-pipeline' 

# If you are gonna use the default values of the pipeline then 
# give a bucket name which is in us-east-1 region 
###################################################################


# Load the dataset
s3 = boto3.client("s3")

# Download file
# data_bucket = S3DataConfig(
#     sm_session, "example-notebooks-data-config", "config/data_config.json"
# ).get_data_bucket()
# print(f"Using data from {data_bucket}")

# s3.download_file(
#     data_bucket, "datasets/image/MNIST/mnist.pkl.gz", "mnist.pkl.gz")

# Manyally download file mnist.pkl.gz

with gzip.open("mnist.pkl.gz", "rb") as f:
    train_set, valid_set, test_set = pickle.load(f, encoding="latin1")



# Upload dataset to S3
from sagemaker.amazon.common import write_numpy_to_dense_tensor
import io
import boto3

train_data_key = 'mnist_kmeans_example/train_data'
test_data_key = 'mnist_kmeans_example/test_data'
train_data_location = 's3://{}/{}'.format(bucket, train_data_key)
test_data_location = 's3://{}/{}'.format(bucket, test_data_key)
print('training data will be uploaded to: {}'.format(train_data_location))
print('training data will be uploaded to: {}'.format(test_data_location))

# Convert the training data into the format required by the SageMaker KMeans algorithm
buf = io.BytesIO()
write_numpy_to_dense_tensor(buf, train_set[0], train_set[1])
buf.seek(0)

print("ready to upload training data")

boto3.resource('s3').Bucket(bucket).Object(train_data_key).upload_fileobj(buf)

print("training data uploaded")

# Convert the test data into the format required by the SageMaker KMeans algorithm
write_numpy_to_dense_tensor(buf, test_set[0], test_set[1])
buf.seek(0)

print("ready to upload testing data")

boto3.resource('s3').Bucket(bucket).Object(test_data_key).upload_fileobj(buf)

print("training data uploaded")

# Convert the valid data into the format required by the SageMaker KMeans algorithm
numpy.savetxt('valid-data.csv', valid_set[0], delimiter=',', fmt='%g')
s3_client = boto3.client('s3')
input_key = "{}/valid_data.csv".format("mnist_kmeans_example/input")
s3_client.upload_file('valid-data.csv', bucket, input_key)