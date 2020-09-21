package aws.h2o.modelendpoint.entrypoint;

import com.google.gson.Gson;
import com.google.gson.JsonSyntaxException;
import hex.genmodel.easy.EasyPredictModelWrapper;
import hex.genmodel.easy.RowData;
import hex.genmodel.easy.prediction.*;
import hex.genmodel.easy.exception.PredictException;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Component;
import java.io.BufferedReader;
import java.time.Duration;
import java.time.Instant;
import java.util.*;

@Component
public class Predictor {
    private JSONParser parser=new JSONParser();
    private Gson gson = new Gson();
    @Async
    public String predict(BufferedReader inputDataReader, EasyPredictModelWrapper model){
        Instant start = Instant.now();
        System.out.println("Prediction Thread " + Thread.currentThread().getName()+" is initiated.");
        JSONObject outObj = new JSONObject();
        try {
            JSONObject inpObj = (JSONObject) parser.parse(inputDataReader);
            System.out.println("Raw Data Parsed: "+inpObj.toString());
            RowData row = jsonToRowData(inpObj.toJSONString());
            inpObj.clear();
            System.out.println("Executing prediction...");
            switch (model.getModelCategory()){
                case Binomial:
                    BinomialModelPrediction b = model.predictBinomial(row);
                    outObj.put("prediction", b.label);
                    outObj.put("predictionIndex", b.labelIndex);
                    outObj.put("classProbabilities", Arrays.toString(b.classProbabilities));
                    outObj.put("calibratedClassProbabilities", Arrays.toString(b.calibratedClassProbabilities));
                    break;
                case Multinomial:
                    MultinomialModelPrediction u = model.predictMultinomial(row);
                    outObj.put("prediction", u.label);
                    outObj.put("predictionIndex", u.labelIndex);
                    outObj.put("classProbabilities", Arrays.toString(u.classProbabilities));
                    break;
                case Regression:
                    RegressionModelPrediction p = model.predictRegression(row);
                    outObj.put("prediction", p.value);
                    break;
                case Ordinal:
                    OrdinalModelPrediction o = model.predictOrdinal(row);
                    outObj.put("prediction", o.label);
                    outObj.put("predictionIndex", o.labelIndex);
                    outObj.put("classProbabilities", Arrays.toString(o.classProbabilities));
                    break;
                case Unknown:
                    throw new PredictException("Unknown Model Category for model inference!");
                default:
                    throw new PredictException("Model Category for model inference is missing or not suitable for this algorithm!");
            }
        } catch (Exception e) {
            System.out.println(e.getMessage());
            e.printStackTrace();
        }
        Instant finish = Instant.now();
        long timeElapsed = Duration.between(start, finish).toMillis();
        System.out.println("Prediction Thread " + Thread.currentThread().getName()+" is closed: "+ timeElapsed +"  milliseconds");
        String outObjStr=outObj.toString();
        System.out.println("Output Object is: "+outObjStr);
        return outObjStr;
    }

    private RowData jsonToRowData(String json) {
        try {
            return gson.fromJson(json, RowData.class);
        }
        catch (JsonSyntaxException e) {
            throw new JsonSyntaxException("Malformed JSON");
        }
    }
}
