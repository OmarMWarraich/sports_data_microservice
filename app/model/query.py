from dataclasses import fields
from typing import Any, Optional
from pypika import Query as PypikaQuery, Table, Order

class FindQuery:

      def __init__(
            self, entity_class: Any, where_expression: Any = None, entity_fields: Optional[list[str] | None] = None,
            limit: Optional[int] = 20, ascending: Optional[bool] = False):

        self.entity_class = entity_class
        self.entity_fields = entity_fields
        self.limit = limit
        self.where_expression = where_expression
        self.use_ascending_order = ascending
        self.db_table: Table = self.entity_class.table()

        def _fields(self) -> list[str]:
            return [f.name for f in fields(self.entity_class)]
        
        def _validate_query_args(self, entity_fields: list[str]) -> None:
            for field in entity_fields:
                if not (field in self._fields()):
                    raise ValueError(
                        'Invalid query field for %s Entity: %s' % (self.entity_class.entity_name(), field))
                
        def _build_querystring(self, *entity_fields: list[str] | str) -> str:
            query_order = Order.asc if self.use_ascending_order else Order.desc
            query_uses_where_expression = self.where_expression
            if query_uses_where_expression:
                return PypikaQuery.from_(self.db_table).orderby('rowid', order=query_order).select(*entity_fields) \
                    .where(self.where_expression) \
                    .limit(self.limit).get_sql().strip()
            return PypikaQuery.from_(self.db_table).orderby('rowid', order=query_order).select(*entity_fields) \
                    .limit(self.limit).get_sql().strip()
            
        def get_sql_querystring(self):
            entity_fields = self.entity_fields

            should_get_all_fields = not entity_fields
            if should_get_all_fields:
                ALL_FIELDS_TOKEN = '*'
                return self._build_querystring(ALL_FIELDS_TOKEN)
            
            self._validate_query_args(entity_fields)
            return self._build_querystring(*entity_fields)