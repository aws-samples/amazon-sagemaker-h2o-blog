# Copyright 2020 Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: LicenseRef-.amazon.com.-AmznSL-1.0
# Licensed under the Amazon Software License  http://aws.amazon.com/asl/

# Based on original Copyright 2018 H2O.ai.
# SPDX-License-Identifier: Apache-2.0

FROM amazonlinux
LABEL maintainer "Anil Sener - AWS <senera@amazon.co.uk>"

ARG build_mode

RUN yum -y update && \
    yum -y install \
      wget \
      curl \
      unzip \
      apt-utils \
      software-properties-common \
      net-tools \
      ca-certificates \
      build-essential

RUN yum -y install java-1.8.0-openjdk-devel

RUN yum -y install \
      python3 \
      python3-setuptools \
      python3-pip \
      git \
      gcc \
      python3-devel

RUN wget https://h2o-release.s3.amazonaws.com/h2o/rel-zahradnik/7/h2o-3.30.0.7.zip && \
    mv h2o-3.30.0.7.zip /opt/h2o-3.30.0.7.zip && \
    unzip -d /opt /opt/h2o-3.30.0.7.zip && \
    rm /opt/h2o-3.30.0.7.zip && \
    cd /opt && \
    mkdir program && \
    cd `find . -name 'h2o.jar' | sed 's/.\///;s/\/h2o.jar//g'` && \
    cp h2o.jar /opt/program && \
    touch /opt/program/flatfile.txt

RUN pip3 install --upgrade --force-reinstall pip==9.0.3 && \
    pip3 install numpy scipy scikit-learn pandas requests tabulate colorama future matplotlib && \
    pip3 install h2o==3.30.0.7 --user

RUN ln -fs /usr/bin/python3 /usr/bin/python

# Set some environment variables. PYTHONUNBUFFERED keeps Python from buffering our standard
# output stream, which means that logs can be delivered to the user quickly. PYTHONDONTWRITEBYTECODE
# keeps Python from writing the .pyc files which are unnecessary in this case. We also update
# PATH so that the train and serve programs are found when the container is invoked.

ENV PYTHONUNBUFFERED=TRUE
ENV PYTHONDONTWRITEBYTECODE=TRUE
ENV PATH="/opt/program:${PATH}"


# Set up the program in the image
COPY gbm_scripts /opt/program
RUN chmod +x /opt/program/startup_h2o_cluster.sh
COPY examples/hyperparameters.json /opt/program/hyperparameters.json
COPY examples/resourceconfig.json /opt/program/resourceconfig.json
COPY examples/train.csv /opt/ml/input/data/training/train.csv
COPY examples/validation.csv /opt/ml/input/data/validation/validation.csv
RUN if [ "$build_mode" = "local" ] ; then echo "$build_mode build mode is used" ; else echo "$build_mode build mode is used" && rm -Rf  /opt/ml/input/data && echo "Test Artifact in /opt/ml/input/data is cleaned!" && echo "$build_mode build mode is used" && rm  /opt/program/hyperparameters.json && echo "Test Artifact in /opt/program/hyperparameters.json is cleaned!" && rm  /opt/program/resourceconfig.json && echo "Test Artifact in /opt/program/resourceconfig.json is cleaned!"; fi

WORKDIR /opt/program
