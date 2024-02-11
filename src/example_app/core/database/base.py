from __future__ import annotations

import sqlalchemy as sa
import sqlalchemy.orm as so

REGISTRY: so.registry = so.registry()
METADATA: sa.MetaData = sa.MetaData()


class Base(so.DeclarativeBase):
    registry = REGISTRY
    metadata = METADATA
