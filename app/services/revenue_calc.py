from decimal import Decimal
from typing import Tuple

class RevenueCalculator:
    """Calculate forecast revenue for projects"""
    
    STAGE_WEIGHTS = {
        "Prospect": Decimal("0.25"),
        "Qualified": Decimal("0.35"),
        "In Delivery": Decimal("0.75"),
        "Closed Won": Decimal("1.0"),
        "Closed Lost": Decimal("0.0"),
    }
    
    @staticmethod
    def calculate_forecast_revenue(
        billable_hours: int,
        bill_rate_per_hour: Decimal,
        utilization_percent: int,
        win_probability: Decimal,
        stage: str
    ) -> Decimal:
        """
        Revenue = Hours × Rate × Utilization% × Win Prob × Stage Weight
        """
        stage_weight = RevenueCalculator.STAGE_WEIGHTS.get(stage, Decimal("0.0"))
        
        forecast = (
            Decimal(billable_hours)
            * bill_rate_per_hour
            * (Decimal(utilization_percent) / Decimal("100"))
            * win_probability
            * stage_weight
        )
        
        return forecast.quantize(Decimal('0.01'))

if __name__ == "__main__":
    # Test: Closed Won project
    revenue = RevenueCalculator.calculate_forecast_revenue(
        billable_hours=800,
        bill_rate_per_hour=Decimal("250.00"),
        utilization_percent=85,
        win_probability=Decimal("1.0"),
        stage="Closed Won"
    )
    print(f"Revenue: ${revenue}")