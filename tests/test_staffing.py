from app.services.staffing_engine import calculate_staffing_position
from app.services.staffing_insight_engine import generate_staffing_insights
from app.services.staffing_recommendation_engine import generate_staffing_recommendations


class _Mappings:
    def one(self):
        return {
            "actual_hours": 1814.0,
            "actual_cost": 181400.0,
            "actual_revenue": 272100.0,
            "budget_hours": 1000.0,
            "budget_utilization": 0.76,
        }


class _Result:
    def mappings(self):
        return _Mappings()


class FakeDB:
    def execute(self, query):
        return _Result()


def test_staffing_does_not_fake_utilization():
    result = calculate_staffing_position(FakeDB())

    assert result["hours_attainment_pct"] == 181.4
    assert result["actual_utilization"] is None
    assert result["bench_hours"] is None
    assert result["bench_percentage"] is None
    assert result["capacity_status"] == "hours_above_budget_review_required"
    assert result["utilization_data_quality"] == "review_required"


def test_staffing_insights_flag_missing_capacity_denominator():
    staffing = {
        "hours_attainment_pct": 181.4,
        "hours_variance_pct": 81.4,
        "budget_utilization": 76.0,
        "utilization_data_quality": "review_required",
    }

    insights = generate_staffing_insights(staffing)

    assert any(
        i["metric"] == "Capacity Denominator"
        and i["severity"] == "HIGH"
        for i in insights
    )


def test_staffing_recommendation_requests_capacity_data():
    staffing = {
        "hours_attainment_pct": 181.4,
        "utilization_data_quality": "review_required",
    }

    recommendations = generate_staffing_recommendations(staffing, [])

    assert recommendations
    assert recommendations[0]["priority"] == "HIGH"
    assert "capacity-hours denominator" in recommendations[0]["action"]
