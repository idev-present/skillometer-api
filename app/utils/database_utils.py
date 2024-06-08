from shortuuid import ShortUUID
from sqlalchemy.dialects import postgresql


def get_result_query(query):
    return str(
        query.statement.compile(
            dialect=postgresql.dialect(),
            compile_kwargs={"literal_binds": True}
        )
    )


def generate_uid(prefix, length=6):
    uid = ShortUUID().random(length=length)
    if prefix:
        return f'{prefix}_{uid}'
    return uid