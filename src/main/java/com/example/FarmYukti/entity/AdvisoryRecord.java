package com.example.FarmYukti.entity;

import jakarta.persistence.*;
import lombok.Data;
import java.time.LocalDateTime;

@Entity
@Table(name = "advisory_records")
@Data
public class AdvisoryRecord {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    @Column(name = "farmer_uid", nullable = false)
    private String farmerUid;

    @Column(name = "land_parcel_id")
    private Integer landParcelId;

    @Column(name = "recommendation_type", nullable = false)
    private String recommendationType; // 'CROP' or 'FERTILIZER'

    // We store the result as text (JSON string) to keep it simple
    @Column(name = "recommendation_data", columnDefinition = "text")
    private String recommendationData;

    @Column(name = "created_at")
    private LocalDateTime createdAt;

    @PrePersist
    protected void onCreate() {
        createdAt = LocalDateTime.now();
    }
}
