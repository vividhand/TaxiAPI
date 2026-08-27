from repositories import EmailVerifyRepositories


def verify_email(token: str, input_code: int):
    conn = EmailVerifyRepositories()
    code_data = conn.get_code_data_by_token(token=token)
    if code_data is None:
        return False
    if code_data.code == input_code:
        return True
    return False