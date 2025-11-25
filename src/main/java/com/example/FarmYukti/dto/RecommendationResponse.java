package com.example.FarmYukti.dto;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import java.util.List;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class RecommendationResponse {
    private String type; // "CROP" or "FERTILIZER"
    private List<String> recommendations;
    private String advice;
}
