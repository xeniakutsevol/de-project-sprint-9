from typing import List
from uuid import UUID

from pydantic import BaseModel


class CdmModel(BaseModel):
    def table_name(self) -> str:
        pass

    def unique_column_names(self) -> List[str]:
        pass


class User_Product_Counters(CdmModel):
    user_id: UUID
    product_id: UUID
    product_name: str
    order_cnt: int

    def table_name(self) -> str:
        return "cdm.user_product_counters"

    def unique_column_names(self) -> List[str]:
        return ["user_id", "product_id"]


class User_Category_Counters(CdmModel):
    user_id: UUID
    category_id: UUID
    category_name: str
    order_cnt: int

    def table_name(self) -> str:
        return "cdm.user_category_counters"

    def unique_column_names(self) -> List[str]:
        return ["user_id", "category_id"]
