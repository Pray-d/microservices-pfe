package com.douaa.prediction_traansition.receiver;


import com.douaa.prediction_traansition.service.PredictionService;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import java.util.ArrayList;
import java.util.List;



@Component
public class PredictionReceiver {

    @Autowired
    private PredictionService predictionService;

    private  List<String> predictions = new ArrayList<>();

    @KafkaListener(topics = "prediction_names", groupId = "group_id")
    public void receivePrediction(String predictionName) {
        System.out.println("Received prediction: " + predictionName);
       // System.out.println("Received prediction: " + predictionName);
        // Update status of prediction to "in discussion"
        // Add prediction to the list
        predictions.add(predictionName.split("#")[0]);
    }

    public List<String> getPredictions() {

        return predictions;
    }
}
