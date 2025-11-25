package com.example.FarmYukti.dto;

import lombok.Data;

@Data
public class SoilDataDTO {
    // Identity fields (For Database saving)
    private String farmerUid;      // Must match a user in your 'users' table
    private Integer landParcelId;  // Optional, can be null

    // Soil Data (For AI Analysis)
    private Double nitrogen;
    private Double phosphorus;
    private Double potassium;
    private Double phLevel;
    private Double rainfall;
    private Double temperature;
    private Double humidity;
}
