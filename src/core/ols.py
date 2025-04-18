import os
import pandas as pd
from typing import Optional
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    RunReportRequest,
    Metric,
    Dimension,
    OrderBy,
    RunReportResponse,
    Filter,
    FilterExpression,
)
from dotenv import load_dotenv, find_dotenv


class OLS:
    """
    Class to interact with Google Analytics 4 (GA4) API and fetch OLS Funnel data.

    Example usage:
    >>> from core.ols_core import OLSCore
    >>> ols = OLSCore()
    >>> df = ols.get_ols_dataframe()
    """

    EVENT_MAP = {
        None: "traffic",
        "view_item": "view_item",
        "home_type_installation_address": "type_addr",
        "form_home_add_email": "add_contact",
        "form_home_add_installation_address": "add_addr",
        "form_home_add_installation_date": "add_date",
        "begin_checkout": "checkout",
        "purchase": "purchase",
    }

    def __init__(self, property_id: Optional[str] = None):
        load_dotenv(find_dotenv())
        self.property_id = property_id or os.getenv("GOOGLE_ANALYTICS_PROPERTY")
        if not self.property_id:
            raise EnvironmentError("GOOGLE_ANALYTICS_PROPERTY not set in environment.")
        self.client = BetaAnalyticsDataClient()

    def _run_report(
        self, start_date: str, end_date: str, event_name: Optional[str] = None
    ) -> pd.DataFrame:
        try:
            req = {
                "property": f"properties/{self.property_id}",
                "metrics": [Metric(name="totalUsers")],
                "dimensions": [Dimension(name="date")],
                "date_ranges": [{"start_date": start_date, "end_date": end_date}],
                "order_bys": [
                    OrderBy(
                        dimension=OrderBy.DimensionOrderBy(dimension_name="date"),
                        desc=True,
                    )
                ],
            }
            if event_name:
                req["dimension_filter"] = FilterExpression(
                    filter=Filter(
                        field_name="eventName",
                        string_filter=Filter.StringFilter(
                            value=event_name,
                            match_type=Filter.StringFilter.MatchType.EXACT,
                        ),
                    )
                )
            resp: RunReportResponse = self.client.run_report(RunReportRequest(**req))
            data = [
                {
                    "date": row.dimension_values[0].value,
                    "totalUsers": int(row.metric_values[0].value),
                }
                for row in resp.rows
            ]
            return pd.DataFrame(data).set_index("date")
        except Exception as e:
            raise RuntimeError(f"Failed to fetch data for event '{event_name}': {e}")

    def get_ols_dataframe(
        self, start_date: str = "7daysAgo", end_date: str = "yesterday"
    ) -> pd.DataFrame:
        dfs = []
        for event, col in self.EVENT_MAP.items():
            df = self._run_report(start_date, end_date, event)
            df = df.rename(columns={"totalUsers": col})
            dfs.append(df)
        return pd.concat(dfs, axis=1)
