from argparse import ArgumentParser
from dataclasses import dataclass

from fastapi import FastAPI
import uvicorn

from app.api import Controller
from app.database import Database
from app.ingest import ingestion


@dataclass
class Args:
    port: int
    db: str


def start_api(args: Args, db: Database):
    app = FastAPI()
    router = Controller(db).router()
    app.include_router(router)
    uvicorn.run(app, port=args.port)


def ingest_data(args: Args, db: Database):
    ingestion.extract_and_save(db)


def main(args: Args):
    db = Database.connect(args.db)
    ingest_data(args, db)
    start_api(args, db)


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--port', default=8000)
    parser.add_argument('--db', default='mysql://user:pass@host:3306/db')

    parsed = parser.parse_args().__dict__
    main(Args(**parsed))
