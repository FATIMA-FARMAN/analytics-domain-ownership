# Contributing to People Analytics Domain

## Development Workflow

1. Create a feature branch from `main`
2. Make changes to models/tests
3. Run quality checks locally:
```bash
   dbt compile
   dbt run --select state:modified+
   dbt test --select state:modified+
   sqlfluff lint models/
```
4. Open a pull request
5. Wait for CI checks to pass
6. Merge after approval

## Naming Conventions

- **Staging models:** `stg_{source}_{table}`
- **Intermediate models:** `int_{entity}_{description}`
- **Dimensions:** `dim_{entity}`
- **Facts:** `fct_{entity}`

## Testing Requirements

Every new model must have:
- [ ] Column-level documentation
- [ ] At least 3 tests
- [ ] Schema contract (if analytics-ready)
