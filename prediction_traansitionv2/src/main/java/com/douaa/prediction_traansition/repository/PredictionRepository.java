package com.douaa.prediction_traansition.repository;

import com.douaa.prediction_traansition.model.Prediction;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Modifying;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

@Repository
public interface PredictionRepository extends JpaRepository<com.douaa.prediction_traansition.model.Prediction, Long> {

    @Transactional
    @Modifying
    @Query("UPDATE Prediction p SET p.status = 'in discussion' WHERE p.name = :name")
    int updateStatusByName(@Param("name") String name);

    @Query("select status from Prediction WHERE name = :name")
    String getPredictionStatus (@Param("name") String name);

    @Query("SELECT name FROM Prediction WHERE status ='in discussion' ")
    List<String> findByStatus();

    @Query("SELECT name FROM Prediction WHERE status ='in discussion'")
    // Define a method to fetch all predictions
    List<Prediction> findAll();

}
