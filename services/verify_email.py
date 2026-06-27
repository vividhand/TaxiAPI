from repositories.verification import EmailVerifyRepositories

def verify_email(token: str, input_code: int):
    conn = EmailVerifyRepositories()
    code = conn.select_verify_code(token=token)
    if code[0] == input_code:
        return True
    else:
        return False