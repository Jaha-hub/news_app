from typing import List

from fastapi_filter.contrib.sqlalchemy import Filter

from categories.models import Category


class CategoryFilter(Filter):
    order_by : List[str] | None = None
    q: str | None = None
    class Constants(Filter.Constants):
        model = Category
        search_filed_name = 'q'
        search_model_fields = ['name']