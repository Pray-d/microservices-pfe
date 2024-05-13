package com.douaa.prediction_traansition.service;

import com.douaa.prediction_traansition.model.Prediction;
import com.douaa.prediction_traansition.repository.PredictionRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import java.util.List;
@Service
public class PredictionService {

    private PredictionRepository predictionRepository;

    @Autowired
    public PredictionService(PredictionRepository predictionRepository) {
        this.predictionRepository = predictionRepository;
    }

    public void updatePredictionStatus(String name, String status) {
        // Update the status of the prediction in the database
        int rowsUpdated = predictionRepository.updateStatusByName(name);
        if (rowsUpdated > 0) {
            System.out.println("Prediction status updated successfully.");
        } else {
            System.out.println("Failed to update prediction status.");
        }
    }

    public void updateSinglePrediction(String predictionName, String status) {
        int rowsUpdated = predictionRepository.updateStatusByName(predictionName);
        if (rowsUpdated > 0) {
            System.out.println("Prediction status updated successfully.");
        } else {
            System.out.println("Failed to update prediction status.");
        }
    }

    public void updateAllPredictionsStatus(String status) {
        // Update status of all predictions to the specified status
        List<Prediction> allPredictions = predictionRepository.findAll();
        for (Prediction prediction : allPredictions) {
            prediction.setStatus(status);
            predictionRepository.save(prediction); // Save the updated prediction
        }
    }

    public String getPredictionsStatus(String name) {
        // Retrieve predictions by status from the repository
        return predictionRepository.getPredictionStatus(name);
    }
}
