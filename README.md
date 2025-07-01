# Great Wolf Lodge Margarita Tracker

I have a 32 oz. tumbler from GWL that cost $28. Refills are only $24, this web app will serve as my long term tracking to measure the value of the cup over the lifetime of its usage.

![20250701131846_9a61924b.png](https://cdn.statically.io/gh/pypeaday/images.pype.dev/main/blog-media/20250701131846_9a61924b.png)

## Stack

- **Backend**: FastAPI, SQLAlchemy
- **Database**: SQLite (via `aiosqlite`)
- **Frontend**: HTMX, TailwindCSS
- **Server**: Uvicorn
- **Package Management**: uv

## Getting Started

1.  **Create a virtual environment:**
    ```bash
    uv venv
    ```

2.  **Activate the virtual environment:**
    ```bash
    source .venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    uv sync
    ```

4.  **Run the application:**
    ```bash
    uvicorn app.main:app --reload
    ```

The application will be available at [http://127.0.0.1:8000](http://127.0.0.1:8000).