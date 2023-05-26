from cdm_loader.repository.cdm_models import CdmModel
from lib.pg import PgConnect


class CdmRepository:
    def __init__(self, db: PgConnect) -> None:
        self._db = db

    def insert(self, model: CdmModel) -> None:
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
