from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlmodel import Field, Session, SQLModel, create_engine, select


class Task(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    content: str = Field(index=True)




sqlite_url = f"postgresql://admin:jk4caRAuZ1BJ@ep-dawn-pond-a572nf3l.us-east-2.aws.neon.tech/Todo-api?sslmode=require"


engine = create_engine(sqlite_url)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the ML model
    create_db_and_tables()
    yield
app:FastAPI = FastAPI(lifespan=lifespan)

@app.post("/task/")
def create_task(task: Task):
    with Session(engine) as session:
        session.add(task)
        session.commit()
        session.refresh(task)
        return task


@app.get("/task/")
def read_task():
    with Session(engine) as session:
        task = session.exec(select(Task)).all()
        return task