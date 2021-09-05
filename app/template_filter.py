def permission(is_admin: bool) -> str:
    if is_admin:
        return "관리자"
    else:
        return "유저"


filter_list = [name for name in dir() if not name.startswith("_")]
