# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License. 


FROM amazonlinux:2

ENV PYTHONPATH /app

RUN yum update -y \
    && yum install -y -q \
    ca-certificates \
    python3 \
    wget \
    unzip \
    vim \ 
    sudo\
    tar

# Install awscli
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64-2.6.3.zip" -o "awscliv2.zip" \
    && unzip -qq awscliv2.zip \
    && ./aws/install

# Install kubectl
RUN  curl -LO "https://dl.k8s.io/release/v1.24.0/bin/linux/amd64/kubectl" \
    && chmod +x ./kubectl \
    && cp ./kubectl /bin

# Install eksctl
RUN curl --silent --location "https://github.com/weaveworks/eksctl/releases/latest/download/eksctl_$(uname -s)_amd64.tar.gz" | tar xz -C /tmp && mv /tmp/eksctl /bin

# # Install aws-iam-authenticator
# RUN curl -o aws-iam-authenticator https://s3.us-west-2.amazonaws.com/amazon-eks/1.21.2/2021-07-05/bin/linux/amd64/aws-iam-authenticator
# RUN chmod +x ./aws-iam-authenticator
# RUN mkdir -p $HOME/bin && cp ./aws-iam-authenticator $HOME/bin/aws-iam-authenticator && export PATH=$PATH:$HOME/bin
# RUN echo 'export PATH=$PATH:$HOME/bin' >> ~/.bashrc

COPY requirements.txt .
RUN pip3 install -r requirements.txt

WORKDIR /app

COPY . .

ENTRYPOINT [ "bash" ]
