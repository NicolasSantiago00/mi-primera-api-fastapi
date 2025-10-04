# tests/test_database_optimization.py (adaptado para edu_)
import pytest
import time
from sqlalchemy.orm import Session
from app.services.optimized_domain_service import OptimizedDomainService

class TestDatabaseOptimization:
    @pytest.mark.asyncio
    async def test_critical_query_performance(self, db_session: Session):
        service = OptimizedDomainService(db_session, "edu_")
        start_time = time.time()
        result = await service.get_critical_data(1)
        duration = time.time() - start_time
        assert duration < 0.2, f"Consulta lenta: {duration:.3f}s"
        assert len(result) > 0

    @pytest.mark.asyncio
    async def test_availability_query_performance(self, db_session: Session):
        service = OptimizedDomainService(db_session, "edu_")
        start_time = time.time()
        result = await service.get_availability_data(dia="2025-10-03", hora="07:00 PM")
        duration = time.time() - start_time
        assert duration < 0.3, f"Consulta lenta: {duration:.3f}s"
        assert len(result) > 0