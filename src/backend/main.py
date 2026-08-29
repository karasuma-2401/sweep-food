import uvicorn
from src.app import app


def main() -> None:
    uvicorn.run("src.app:app", host="0.0.0.0", port=4000, reload=True)


if __name__ == "__main__":
    main()
