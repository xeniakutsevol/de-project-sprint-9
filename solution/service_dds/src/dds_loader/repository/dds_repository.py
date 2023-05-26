from typing import List, Tuple

from dds_loader.repository.dds_models import DdsModel
from lib.pg import PgConnect


class DdsRepository:
    def __init__(self, db: PgConnect) -> None:
        self._db = db

    def insert(self, model: DdsModel) -> None:
        table_name = model.table_name()
        unique_column_names = model.unique_column_names()
        column_names = list(model.__fields__.keys())
        column_names_str = ", ".join(column_names)
        unique_column_names_str = ", ".join(unique_column_names)
        values_names_str = ", ".join([f"%({name})s" for name in column_names])
        update_names_str = ", ".join(
            [f"{name}=excluded.{name}" for name in column_names]
        )

        query = f"""
        insert into {table_name} ({column_names_str})
        values ({values_names_str})
        on conflict ({unique_column_names_str})
        do update set {update_names_str};
        """

        with self._db.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, model.dict())

    def counter(self, user_id: str, object_type: str) -> List[Tuple]:
        if object_type == "product":
            query = f"""
            select
            lou.h_user_pk as user_id,
            lop.h_product_pk as product_id,
            spn.name as product_name,
            count(*) as order_cnt
            from dds.l_order_product lop
            join dds.l_order_user lou
            on lou.h_order_pk=lop.h_order_pk
            join dds.s_product_names spn
            on lop.h_product_pk=spn.h_product_pk
            where lou.h_user_pk='{user_id}'
            group by user_id, product_id, product_name;
            """

        elif object_type == "category":
            query = f"""
            with cte as (
            select
            lpc.h_category_pk,
            category_name,
            h_product_pk
            from dds.l_product_category lpc
            join dds.h_category hc
            on lpc.h_category_pk=hc.h_category_pk
            )
            select
            lou.h_user_pk as user_id,
            cte.h_category_pk as category_id,
            cte.category_name as category_name,
            count(lop.h_order_pk) as order_cnt
            from dds.l_order_product lop
            join dds.l_order_user lou
            on lou.h_order_pk=lop.h_order_pk
            join cte
            on lop.h_product_pk=cte.h_product_pk
            where lou.h_user_pk='{user_id}'
            group by user_id, category_id, category_name;
            """

        with self._db.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                query_result = cur.fetchall()

        return query_result
