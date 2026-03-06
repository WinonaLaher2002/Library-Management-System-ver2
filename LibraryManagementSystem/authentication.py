from supabase_db import check_connection


def verify_supabase_connection():
    try:
        response = check_connection()
        print("Supabase connection verified.")
        print("Books query returned", len(response or []), "row(s).")
    except Exception as error:
        print("Supabase connection failed:", error)


if __name__ == "__main__":
    verify_supabase_connection()
