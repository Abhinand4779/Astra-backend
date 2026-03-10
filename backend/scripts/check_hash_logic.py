from app.auth import get_password_hash, verify_password

def check_logic():
    pwd = "admin123"
    hashed = get_password_hash(pwd)
    print(f"Hashed: {hashed}")
    result = verify_password(pwd, hashed)
    print(f"Verify Correct: {result}")
    
    wrong_result = verify_password("wrong", hashed)
    print(f"Verify Wrong: {wrong_result}")

if __name__ == "__main__":
    check_logic()
