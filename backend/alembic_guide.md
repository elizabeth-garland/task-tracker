# Alembic Migration Guide for Task Tracker

This guide provides detailed instructions on using Alembic to manage database migrations for your Task Tracker application.

## Setting Up Alembic (Already Done)

The following files have been created for you:
- `alembic.ini`: Configuration file for Alembic
- `alembic/env.py`: Environment configuration for Alembic
- `alembic/script.py.mako`: Template for migration scripts
- `alembic/README.md`: Quick reference for Alembic commands

## Workflow for Database Changes

### 1. Generate Your Initial Migration

Since you already have database models defined (User and Task), you should generate an initial migration to create these tables:

```bash
cd backend
alembic revision --autogenerate -m "Create users and tasks tables"
```

This will create a migration script in the `alembic/versions/` directory that contains the SQL needed to create your tables.

### 2. Review the Generated Migration

Always review the generated migration script before applying it. Open the file in the `alembic/versions/` directory and verify that:
- It creates the correct tables
- It includes all columns with proper types
- Foreign key relationships are properly defined

### 3. Apply the Migration to Create the Tables

```bash
cd backend
alembic upgrade head
```

This will execute the migration script and create the tables in your database.

### 4. Workflow for Future Changes

When you modify your models (adding columns, creating new tables, etc.), follow this workflow:

1. Make changes to your SQLAlchemy models in `app/models/`
2. Generate a new migration to reflect these changes:
   ```bash
   cd backend
   alembic revision --autogenerate -m "Description of your changes"
   ```
3. Review the generated migration script in `alembic/versions/`
4. Apply the migration to update your database:
   ```bash
   cd backend
   alembic upgrade head
   ```

## Useful Alembic Commands

### Check Current Database Version

```bash
cd backend
alembic current
```

### View Migration History

```bash
cd backend
alembic history
```

### Upgrade to a Specific Version

```bash
cd backend
alembic upgrade <revision_id>
```

### Downgrade to a Previous Version

```bash
cd backend
alembic downgrade <revision_id>
```

### Downgrade One Step

```bash
cd backend
alembic downgrade -1
```

## Troubleshooting

### "Can't locate revision" Error

If you see an error like "Can't locate revision identified by '...'", it means Alembic can't find the migration script. Make sure:
- You're running commands from the correct directory (backend)
- The migration script exists in `alembic/versions/`
- The migration script is properly formatted

### Tables Already Exist

If your tables already exist in the database before running migrations, you might see errors. In this case:
1. Drop the existing tables
2. Run the migrations to recreate them properly

### Conflicting Migrations

If you have conflicts between your SQLAlchemy models and the database state, you might need to:
1. Downgrade to a clean state (`alembic downgrade base`)
2. Fix your models and migration scripts
3. Upgrade again (`alembic upgrade head`)

## Working with Docker

If you're using Docker, you'll need to run Alembic commands inside your container:

```bash
docker-compose exec backend alembic revision --autogenerate -m "Your message"
docker-compose exec backend alembic upgrade head
```

Make sure your database container is running before executing these commands.
