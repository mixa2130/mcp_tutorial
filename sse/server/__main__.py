import uvicorn

from .api import app_main


def main():
    uvicorn.run(app_main, host='0.0.0.0', port=8080)


if __name__ == '__main__':
    main()
