package com.douaa.prediction_traansition.controller;

import com.douaa.prediction_traansition.receiver.PredictionReceiver;
import com.douaa.prediction_traansition.service.PredictionService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;

import java.util.List;
import java.util.stream.Collectors;

@Controller
public class PredictionController {

    @Autowired
    private PredictionService predictionService;

    @Autowired
    private PredictionReceiver predictionReceiver;
    @GetMapping("/predictions")
    public String showPredictions(Model model) {
        // Fetch predictions from the receiver
        List<String> predictions = predictionReceiver.getPredictions();
        // Filter predictions to include only those with status "available"
        // Filter predictions to include only those with status "available"
        List<String> availablePredictions = predictions.stream()
                .filter(prediction -> {
                    String status = predictionService.getPredictionsStatus(prediction);
                    return status != null && status.equals("available");
                })
                .collect(Collectors.toList());
        // Add available predictions to the model
        model.addAttribute("predictions", availablePredictions);


        return "predictions";
    }

    @PostMapping("/predictions/update/{predictionName}")
    public String updatePrediction(@PathVariable String predictionName, @RequestParam String action) {

            // Update prediction status to "in discussion" in the database
            predictionService.updateSinglePrediction(predictionName.replace("%20",""), "in discussion");

        // Redirect back to the predictions page
        return "redirect:/predictions";
    }

    @PostMapping("/predictions/update-all")
    public String updateAllPredictions() {
        // Update all predictions status to the specified status in the database
        List<String> predictions = predictionReceiver.getPredictions();
        for (String name : predictions) {
            predictionService.updatePredictionStatus(name, "in discussion");
        }

        // Redirect back to the predictions page
        return "redirect:/predictions";
    }

    @PostMapping("/predictions/deny-all")
    public String denyAllPredictions() {
        // Update all predictions status to "Denied" in the database
        predictionService.updateAllPredictionsStatus("Denied");
        // Redirect back to the predictions page
        return "redirect:/predictions";
    }
}
