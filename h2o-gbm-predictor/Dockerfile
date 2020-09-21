FROM amazoncorretto:8
LABEL maintainer "Anil Sener - AWS <senera@amazon.co.uk>"

ARG build_mode

RUN mkdir /opt/program
RUN mkdir /opt/ml
RUN mkdir /opt/ml/model

ADD target/h2o-gbm-predictor-0.0.1-SNAPSHOT.jar /opt/program/app.jar
ADD target/test-classes/model.tar.gz /opt/ml/model/model.tar.gz
RUN if [ "$build_mode" = "local" ] ; then echo "$build_mode build mode is used" ; else echo "$build_mode build mode is used" && rm -Rf  /opt/ml/model && echo "Test Artifact in /opt/ml/model is cleaned!" ; fi
RUN sh -c 'touch /opt/program/app.jar'

EXPOSE 8080
WORKDIR /opt/program
ENTRYPOINT ["java", "-Djava.security.egd=file:/dev/./urandom", "-Dapp.port=${app.port}", "-jar","/opt/program/app.jar"]

