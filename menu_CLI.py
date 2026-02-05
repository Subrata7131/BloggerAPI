import requests
import sys

API_URL = "http://127.0.0.1:8000"

BOLD = "\033[1m"
RESET = "\033[0m"


def create_blog():
    print(f"\n--- {BOLD}Create a New Blog Post{RESET} ---")
    user_name = input("Enter User Name: ")
    title = input("Enter Blog Title: ")
    description = input("Enter Blog Description: ")

    payload = {"user_name": user_name, "title": title, "description": description}

    try:
        response = requests.post(f"{API_URL}/create_blog", json=payload)

        if response.status_code == 200:
            data = response.json()
            print(f"\n✅ Success! Blog Created.")
            print(f"🆔 Blog ID: {BOLD}{data['id']}{RESET} (Save this ID to view later)")
        else:
            print(f"\nError: {response.status_code} - {response.text}")
    except requests.exceptions.ConnectionError:
        print("\nCould not connect to the server.")


def view_blog_by_id():
    print(f"\n--- {BOLD}View Blog by ID{RESET} ---")
    blog_id = input("Enter Blog ID to view: ").strip()

    try:
        response = requests.get(f"{API_URL}/get_blog/{blog_id}")

        if response.status_code == 200:
            blog = response.json()

            print("\n" + "=" * 40)
            user = blog.get("user_name", "Unknown")
            date = blog.get("date", "N/A")
            time = blog.get("time", "N/A")

            print(f"User: {user}")
            print(f"Date: {date} | Time: {time}")
            print("-" * 40)
            print(f"Title: {BOLD}{blog['title']}{RESET}")
            print("-" * 40)
            print(f"Description:\n{blog['description']}")
            print("=" * 40 + "\n")

        else:
            print("\n❌ Blog not found. please check id.")
    except Exception as e:
        print(f"Error: {e}")


def view_all_blogs():
    print(f"\n--- {BOLD}All Blogs List{RESET} ---")
    try:
        response = requests.get(f"{API_URL}/get_all_blogs")
        if response.status_code == 200:
            data = response.json()
            print(f"Total Blogs Found: {data['total']}\n")

            for blog in data["data"]:
                print("-" * 40)
                print(f"🆔 ID: {blog['_id']}")
                print(f"👤 User: {blog['user_name']}")
                print(f"📅 Date: {blog['date']}")
                print(f"📌 {BOLD}Title: {blog['title']}{RESET}")
            print("-" * 40)
        else:
            print(" Failed to fetch blogs.")
    except Exception as e:
        print(f"Error: {e}")


def delete_blog():
    print(f"\n--- {BOLD}Delete Blog{RESET} ---")
    blog_id = input("Enter ID to Delete: ").strip()

    try:
        res = requests.delete(f"{API_URL}/delete_blog/{blog_id}")

        if res.status_code == 200:
            print(f"\n  {BOLD}Deleted Successfully!{RESET}")
        else:
            print("\n Failed. ID wrong.")

    except:
        print("\n Connection Error.")


def main():
    while True:
        print(f"\n=== {BOLD}BLOG CLI MENU{RESET} ===")
        print("1. Create New Blog")
        print("2. View Blog by ID")
        print("3. View All Blogs")
        print("4. Delete Blog")
        print("5. Exit")

        choice = input("Select an option (1-5): ")

        if choice == "1":
            create_blog()
        elif choice == "2":
            view_blog_by_id()
        elif choice == "3":
            view_all_blogs()
        elif choice == "4":
            delete_blog()
        elif choice == "5":
            print("Exiting... Sucessfully")
            sys.exit()
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
