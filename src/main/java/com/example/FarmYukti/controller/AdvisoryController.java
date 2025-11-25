package com.example.FarmYukti.controller;

import com.example.FarmYukti.dto.RecommendationResponse;
import com.example.FarmYukti.dto.SoilDataDTO;
import com.example.FarmYukti.service.RecommendationService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/advisory")
@CrossOrigin(origins = "*") // Allows your frontend to access this
public class AdvisoryController {

    @Autowired
    private RecommendationService recommendationService;

    @PostMapping("/crop")
    public ResponseEntity<RecommendationResponse> getCropRecommendation(@RequestBody SoilDataDTO soilData) {
        // Validate inputs
        if (soilData.getFarmerUid() == null) {
             // In a real app you might block this, but for now we allow testing
             System.out.println("Warning: No Farmer UID provided. Record won't be saved.");
        }
        return ResponseEntity.ok(recommendationService.recommendCrop(soilData));
    }

    @PostMapping("/fertilizer")
    public ResponseEntity<RecommendationResponse> getFertilizerRecommendation(@RequestBody SoilDataDTO soilData) {
        return ResponseEntity.ok(recommendationService.recommendFertilizer(soilData));
    }
}
