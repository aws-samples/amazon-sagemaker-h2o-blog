package aws.h2o.modelendpoint.app;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.SpringBootConfiguration;
import org.springframework.boot.autoconfigure.EnableAutoConfiguration;
import org.springframework.context.annotation.ComponentScan;
import org.springframework.scheduling.annotation.EnableAsync;

@SpringBootConfiguration
@EnableAutoConfiguration
@EnableAsync
@ComponentScan(basePackages = "aws.h2o.modelendpoint.entrypoint")
public class SagemakerLauncher {
  public static void main(String[] args) {
    serve();
  }

  public static void serve() {
    SpringApplication.run(SagemakerLauncher.class);
  }
}
