# Alembic Migrations

This directory contains database migration scripts for your Task Tracker application.

## Migration Commands

### Generate a Migration

To generate a new migration based on changes to your SQLAlchemy models:

```bash
cd backend
alembic revision --autogenerate -m "Description of the changes"
```

### Apply Migrations

To apply all pending migrations to the database:

```bash
cd backend
alembic upgrade head
```

### Rollback Migrations

To roll back the last migration:

```bash
cd backend
alembic downgrade -1
```

To roll back to a specific migration:

```bash
cd backend
alembic downgrade <revision_id>
```

### View Migration History

To see the migration history:

```bash
cd backend
alembic history
```

### Check Current Migration Status

To see the current database version:

```bash
cd backend
alembic current
```
