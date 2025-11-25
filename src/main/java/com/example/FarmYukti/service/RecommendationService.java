package com.example.FarmYukti.service;

import com.example.FarmYukti.dto.RecommendationResponse;
import com.example.FarmYukti.dto.SoilDataDTO;
import com.example.FarmYukti.entity.AdvisoryRecord;
import com.example.FarmYukti.repository.AdvisoryRepository;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import java.util.List;
import java.util.Map;

@Service
public class RecommendationService {

    @Autowired
    private RestTemplate restTemplate;

    @Autowired
    private AdvisoryRepository advisoryRepository;

    @Autowired
    private ObjectMapper objectMapper;

    // URL of your Python AI Service
    private final String AI_SERVICE_URL = "http://localhost:5000";

    public RecommendationResponse recommendCrop(SoilDataDTO soil) {
        String url = AI_SERVICE_URL + "/predict_crop";
        
        try {
            // 1. Call Python AI
            ResponseEntity<Map> response = restTemplate.postForEntity(url, soil, Map.class);
            Map<String, Object> body = response.getBody();

            if (body != null && body.containsKey("alternatives")) {
                List<String> crops = (List<String>) body.get("alternatives");
                String bestCrop = (String) body.get("recommended_crop");
                String advice = "AI suggests " + bestCrop + " based on your soil profile.";

                RecommendationResponse result = new RecommendationResponse("CROP", crops, advice);
                
                // 2. Save to Database
                saveRecord(soil, "CROP", result);

                return result;
            }
        } catch (Exception e) {
            e.printStackTrace();
            return new RecommendationResponse("ERROR", null, "AI Service Failed: " + e.getMessage());
        }
        return null;
    }

    public RecommendationResponse recommendFertilizer(SoilDataDTO soil) {
        String url = AI_SERVICE_URL + "/predict_fertilizer";

        try {
            ResponseEntity<Map> response = restTemplate.postForEntity(url, soil, Map.class);
            Map<String, Object> body = response.getBody();

            if (body != null && body.containsKey("recommended_fertilizer")) {
                List<String> fertilizers = (List<String>) body.get("recommended_fertilizer");
                RecommendationResponse result = new RecommendationResponse("FERTILIZER", fertilizers, "Nutrient based recommendation.");

                // Save to Database
                saveRecord(soil, "FERTILIZER", result);

                return result;
            }
        } catch (Exception e) {
            e.printStackTrace();
            return new RecommendationResponse("ERROR", null, "AI Service Failed: " + e.getMessage());
        }
        return null;
    }

    // Helper method to save history
    private void saveRecord(SoilDataDTO soil, String type, RecommendationResponse result) {
        try {
            if (soil.getFarmerUid() != null) {
                AdvisoryRecord record = new AdvisoryRecord();
                record.setFarmerUid(soil.getFarmerUid());
                record.setLandParcelId(soil.getLandParcelId());
                record.setRecommendationType(type);
                // Convert the result object to a JSON String
                record.setRecommendationData(objectMapper.writeValueAsString(result));
                
                advisoryRepository.save(record);
            }
        } catch (Exception e) {
            System.err.println("Failed to save advisory record: " + e.getMessage());
            // We do not throw exception here so the user still gets their answer even if DB save fails
        }
    }
}
