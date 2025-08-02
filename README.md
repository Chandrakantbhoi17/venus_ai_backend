# VenusAI Backend

## Setup

1. Install dependencies:
   pip install -r requirements.txt

2. Apply migrations:
   alembic upgrade head

3. Run the app:
   uvicorn app.main:app --reload
