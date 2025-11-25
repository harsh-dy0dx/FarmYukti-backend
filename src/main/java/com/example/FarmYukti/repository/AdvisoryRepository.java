package com.example.FarmYukti.repository;

import com.example.FarmYukti.entity.AdvisoryRecord;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import java.util.List;

@Repository
public interface AdvisoryRepository extends JpaRepository<AdvisoryRecord, Integer> {
    // This magic method allows us to find all advice given to a specific farmer
    List<AdvisoryRecord> findByFarmerUid(String farmerUid);
}
