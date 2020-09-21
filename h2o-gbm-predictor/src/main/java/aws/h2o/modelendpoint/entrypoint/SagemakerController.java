package aws.h2o.modelendpoint.entrypoint;

import java.io.IOException;
import javax.annotation.PostConstruct;
import javax.servlet.http.HttpServletRequest;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RestController;
import hex.genmodel.MojoModel;
import hex.genmodel.easy.EasyPredictModelWrapper;
import java.nio.file.Files;
import java.nio.file.Paths;
import org.springframework.beans.factory.annotation.Autowired;

@RestController
public class SagemakerController {
  private EasyPredictModelWrapper.Config config;
  private EasyPredictModelWrapper model;
  @Autowired
  private Predictor predictor;
  @PostConstruct
  public void init() throws Exception{
    try {
      String modelLocation="/opt/ml/model";
      String modelFileName = findModelFileName(modelLocation);
      System.out.println("Loading the model from "+modelFileName);
      this.config = new EasyPredictModelWrapper.Config()
              .setModel(MojoModel.load(modelFileName))
              .setConvertUnknownCategoricalLevelsToNa(true)
              .setConvertInvalidNumbersToNa(true);
      this.model = new EasyPredictModelWrapper(this.config);
      System.out.println("Model with "+model.getModelCategory().toString().toLowerCase()+" category is loaded.");
      this.predictor = new Predictor();
    } catch (Exception e) {
      e.printStackTrace();
      throw new Exception("Model Loading failed due to "+e.getMessage());
    }
  }

  @RequestMapping(value = "/ping", method = RequestMethod.GET)
  public ResponseEntity<String> ping() {
    return ResponseEntity
            .ok()
            .body("Model Endpoint Ping Request is successful!");
  }
  
  @RequestMapping(value = "/invocations", method = RequestMethod.POST)
  public String invoke(HttpServletRequest request) throws IOException {
    return this.predictor.predict(request.getReader(), this.model);
  }

  private static String findModelFileName(String rootFolder) throws Exception {
    return Files.walk(Paths.get(rootFolder)).filter(Files::isRegularFile)
            .findFirst().get().toAbsolutePath().toString();
  }

}
