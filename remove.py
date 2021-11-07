from datetime import datetime

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from app.database import get_url
from app.models import Login


def get_time() -> str:
    return datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")


def echo(message: str) -> None:
    print(get_time() + " " + message)


def main():
    echo("데이터베이스에 저장되어 있는 세션을 검색하는 중 입니다...")

    engine = create_engine(get_url())
    session = sessionmaker(bind=engine)()
    length = session.query(Login).count()
    per_page = 5
    total_page = getattr(__import__("math"), "ceil")(length / per_page)

    echo(f"총 {length}개의 세션이 등록되어 있습니다.")
    echo(f"{total_page}개로 나눠서 세션 만료 여부를 검사합니다.")

    last_id = 0
    for page in range(1, total_page + 1):
        logins = session.query(Login).filter(Login.id > last_id).limit(per_page).all()
        for login in logins:
            is_limited = login.expired <= datetime.now()

            if is_limited:
                echo(f"{login.id}번 세션이 만료되어 데이터베이스에서 삭제되었습니다.")
                session.delete(login)
            else:
                echo(f"{login.id}번 세션은 만료되지 않았습니다.")

            last_id = login.id

        session.commit()

    echo("검사가 완료되었습니다.")


if __name__ == "__main__":
    main()
