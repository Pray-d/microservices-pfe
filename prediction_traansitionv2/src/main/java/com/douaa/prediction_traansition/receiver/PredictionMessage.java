package com.douaa.prediction_traansition.receiver;

public class PredictionMessage {
    private String prediction;
    private String start_date;
    private String finish_date;

    // Default constructor (required for Jackson)
    public PredictionMessage() {}

    // Constructor with fields
    public PredictionMessage(String prediction, String start_date, String finish_date) {
        this.prediction = prediction;
        this.start_date = start_date;
        this.finish_date = finish_date;
    }

    // Getters and setters
    public String getPrediction() {
        return prediction;
    }

    public void setPrediction(String prediction) {
        this.prediction = prediction;
    }

    public String getStart_date() {
        return start_date;
    }

    public void setStart_date(String start_date) {
        this.start_date = start_date;
    }

    public String getFinish_date() {
        return finish_date;
    }

    public void setFinish_date(String finish_date) {
        this.finish_date = finish_date;
    }
}
