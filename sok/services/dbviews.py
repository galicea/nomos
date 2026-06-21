# backend0/services/dbviews.py
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List, Dict, Any, Generator
import re
from schemas.kn_schemas import ViewListSchema, ColumnSchema

class ViewRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_view_list(self) -> List[ViewListSchema]:
        dialect = self.db.bind.dialect.name
        if dialect == "sqlite":
            query = text("""
                SELECT name AS view_name
                FROM sqlite_master
                WHERE type = 'view' AND name LIKE 'q__%';
            """)
        else:
            query = text("""
                SELECT table_name AS view_name
                FROM information_schema.views
                WHERE table_schema NOT IN ('pg_catalog', 'information_schema') 
                  AND table_name LIKE 'q__%';
            """)
        result = self.db.execute(query).mappings().all()
        return [ViewListSchema(**dict(row)) for row in result]

    def get_view_structure(self, view_name: str) -> List[ColumnSchema]:
        dialect = self.db.bind.dialect.name
        if dialect == "sqlite":
            sanitized_name = re.sub(r'[^a-zA-Z0-9_.]', '', view_name)
            query = text(f'PRAGMA table_info("{sanitized_name}")')
            result = self.db.execute(query).all()
            return [ColumnSchema(column_name=row[1], data_type=row[2]) for row in result]
        else:
            query = text("""
                SELECT c.column_name, c.data_type
                FROM information_schema.views AS v
                JOIN information_schema.columns AS c
                    ON v.table_schema = c.table_schema
                    AND v.table_name = c.table_name
                WHERE v.table_schema = 'public' 
                  AND v.table_name = :view_name
                ORDER BY c.ordinal_position;
            """)
            result = self.db.execute(query.bindparams(view_name=view_name)).mappings().all()
            return [ColumnSchema(**dict(row)) for row in result]

    def query_view(self, view_name: str, **filters: Any) -> Generator[Dict[str, Any], None, None]:
        conditions = []
        params = {}
        for i, (key, value) in enumerate(filters.items()):
            if value is None:
                continue
            placeholder = f"p{i}"
            conditions.append(f'"{key}" = :{placeholder}')
            params[placeholder] = value
        where_clause = " AND ".join(conditions) if conditions else "1=1"
        query = text(f'SELECT * FROM "{view_name}" WHERE {where_clause}')
        result = self.db.execute(query, params)
        for row in result.mappings():
            yield dict(row)
