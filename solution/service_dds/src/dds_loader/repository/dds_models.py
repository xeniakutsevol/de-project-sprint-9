from datetime import datetime
from typing import List
from uuid import UUID

from pydantic import BaseModel


class DdsModel(BaseModel):
    def table_name(self) -> str:
        pass

    def unique_column_names(self) -> List[str]:
        pass


class H_User(DdsModel):
    h_user_pk: UUID
    user_id: str
    load_dt: datetime
    load_src: str

    def table_name(self) -> str:
        return "dds.h_user"

    def unique_column_names(self) -> List[str]:
        return ["h_user_pk"]


class H_Product(DdsModel):
    h_product_pk: UUID
    product_id: str
    load_dt: datetime
    load_src: str

    def table_name(self) -> str:
        return "dds.h_product"

    def unique_column_names(self) -> List[str]:
        return ["h_product_pk"]


class H_Category(DdsModel):
    h_category_pk: UUID
    category_name: str
    load_dt: datetime
    load_src: str

    def table_name(self) -> str:
        return "dds.h_category"

    def unique_column_names(self) -> List[str]:
        return ["h_category_pk"]


class H_Restaurant(DdsModel):
    h_restaurant_pk: UUID
    restaurant_id: str
    load_dt: datetime
    load_src: str

    def table_name(self) -> str:
        return "dds.h_restaurant"

    def unique_column_names(self) -> List[str]:
        return ["h_restaurant_pk"]


class H_Order(DdsModel):
    h_order_pk: UUID
    order_id: str
    order_dt: datetime
    load_dt: datetime
    load_src: str

    def table_name(self) -> str:
        return "dds.h_order"

    def unique_column_names(self) -> List[str]:
        return ["h_order_pk"]


class L_Order_Product(DdsModel):
    hk_order_product_pk: UUID
    h_order_pk: UUID
    h_product_pk: UUID
    load_dt: datetime
    load_src: str

    def table_name(self) -> str:
        return "dds.l_order_product"

    def unique_column_names(self) -> List[str]:
        return ["hk_order_product_pk"]


class L_Product_Restaurant(DdsModel):
    hk_product_restaurant_pk: UUID
    h_product_pk: UUID
    h_restaurant_pk: UUID
    load_dt: datetime
    load_src: str

    def table_name(self) -> str:
        return "dds.l_product_restaurant"

    def unique_column_names(self) -> List[str]:
        return ["hk_product_restaurant_pk"]


class L_Product_Category(DdsModel):
    hk_product_category_pk: UUID
    h_product_pk: UUID
    h_category_pk: UUID
    load_dt: datetime
    load_src: str

    def table_name(self) -> str:
        return "dds.l_product_category"

    def unique_column_names(self) -> List[str]:
        return ["hk_product_category_pk"]


class L_Order_User(DdsModel):
    hk_order_user_pk: UUID
    h_order_pk: UUID
    h_user_pk: UUID
    load_dt: datetime
    load_src: str

    def table_name(self) -> str:
        return "dds.l_order_user"

    def unique_column_names(self) -> List[str]:
        return ["hk_order_user_pk"]


class S_User_Names(DdsModel):
    h_user_pk: UUID
    username: str
    userlogin: str
    load_dt: datetime
    load_src: str
    hk_user_names_hashdiff: UUID

    def table_name(self) -> str:
        return "dds.s_user_names"

    def unique_column_names(self) -> List[str]:
        return ["hk_user_names_hashdiff"]


class S_Product_Names(DdsModel):
    h_product_pk: UUID
    name: str
    load_dt: datetime
    load_src: str
    hk_product_names_hashdiff: UUID

    def table_name(self) -> str:
        return "dds.s_product_names"

    def unique_column_names(self) -> List[str]:
        return ["hk_product_names_hashdiff"]


class S_Restaurant_Names(DdsModel):
    h_restaurant_pk: UUID
    name: str
    load_dt: datetime
    load_src: str
    hk_restaurant_names_hashdiff: UUID

    def table_name(self) -> str:
        return "dds.s_restaurant_names"

    def unique_column_names(self) -> List[str]:
        return ["hk_restaurant_names_hashdiff"]


class S_Order_Cost(DdsModel):
    h_order_pk: UUID
    cost: float
    payment: float
    load_dt: datetime
    load_src: str
    hk_order_cost_hashdiff: UUID

    def table_name(self) -> str:
        return "dds.s_order_cost"

    def unique_column_names(self) -> List[str]:
        return ["hk_order_cost_hashdiff"]


class S_Order_Status(DdsModel):
    h_order_pk: UUID
    status: str
    load_dt: datetime
    load_src: str
    hk_order_status_hashdiff: UUID

    def table_name(self) -> str:
        return "dds.s_order_status"

    def unique_column_names(self) -> List[str]:
        return ["hk_order_status_hashdiff"]
