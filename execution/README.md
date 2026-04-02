# Execution Layer

This directory contains deterministic Python scripts that handle the actual work:
- API calls
- Data processing
- File operations
- Database interactions

## Principles

- **Deterministic**: Scripts produce the same output for the same input
- **Reliable**: Well-tested, with proper error handling
- **Fast**: Optimized for performance
- **Well-commented**: Clear intent and implementation details

## Environment Variables

Scripts read configuration from `.env` in the project root. Use `python-dotenv` to load:

```python
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv('API_KEY')
```

## Testing

Run scripts with test inputs before deploying to production.
