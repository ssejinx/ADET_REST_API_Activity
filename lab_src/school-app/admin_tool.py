import requests

# URL of your API - Ensure this matches your XAMPP folder
URL = "http://localhost/school-app/api.php"
ADMIN_KEY = "1"

def get_headers():
    return {"X-Admin-Token": ADMIN_KEY, "Content-Type": "application/json"}

def main():
    logged_in = False
    
    while True:
        if not logged_in:
            print("\n" + "="*45)
            print("       ART MARKETPLACE: PUBLIC PORTAL")
            print("="*45)
            print("1. Search/Verify Artist")
            print("2. Submit Registration Request")
            print("3. Switch to Admin Login")
            print("4. Exit")
            choice = input("\nSelect an option: ")

            if choice == "1": # VERIFY
                u = input("Enter username to verify: ")
                res = requests.get(f"{URL}?action=verify&username={u}")
                data = res.json()
                if res.status_code == 200 and 'user' in data:
                    print(f"\n✅ VERIFIED: @{data['user']['username']} is registered.")
                    print(f"Bio: {data['user']['bio']}")
                else:
                    print(f"\n❌ NOT FOUND: {data.get('error', 'Artist is not in our database.')}")

            elif choice == "2": # REGISTER REQUEST
                u = input("Desired Username: ")
                b = input("Enter your Bio: ")
                res = requests.post(f"{URL}?action=request", json={"username": u, "bio": b})
                data = res.json()
                if res.status_code == 200:
                    print(f"\n✅ Success: {data.get('message')}")
                else:
                    print(f"\n❌ Error: {data.get('error')}")

            elif choice == "3": # ADMIN LOGIN
                key = input("Enter Admin Secret Key: ")
                if key == ADMIN_KEY:
                    logged_in = True
                    print("\n Admin Access Granted.")
                else:
                    print("\n Incorrect Key. Access Denied.")

            elif choice == "4": break

        else: # ADMIN MODE
            
            print("\n" + "="*42)
            print("         OFFICIAL ADMIN DASHBOARD")
            print("="*42)   
            print("1. View All Approved Artists")
            print("2. View All Pending Applications")
            print("3. APPROVE A USER (Numbered List)")
            print("4. EDIT ARTIST BIO (Numbered List)")
            print("5. DELETE AN ARTIST (Numbered List)")
            print("6. Logout to Public Menu")
            choice = input("\nAdmin Choice: ")

            if choice == "1": # VIEW APPROVED
                res = requests.get(URL, headers=get_headers())
                approved = res.json()

                print("\n✅ APPROVED ARTISTS:")

                if not isinstance(approved, list) or len(approved) == 0:
                    print("--- No approved artists ---")
                else:
                    print("------------------------------------------------------------")
                    print(f"{'No.':<5} | {'Username':<15} | {'Bio':<30}")
                    print("------------------------------------------------------------")

                    for i, user in enumerate(approved, 1):
                        print(f"{i:<5} | {user['username']:<15} | {user['bio']:<30}")

                    print("------------------------------------------------------------\n")
                            

            elif choice == "2": # VIEW PENDING
                res = requests.get(f"{URL}?action=pending", headers=get_headers())
                pending = res.json()

                print("\n⏳ PENDING REQUESTS:")

                if not isinstance(pending, list) or len(pending) == 0:
                    print("--- No pending requests ---")
                else:
                    print("------------------------------------------------------------")
                    print(f"{'No.':<5} | {'Username':<15} | {'Bio':<30}")
                    print("------------------------------------------------------------")

                    for i, user in enumerate(pending, 1):
                        print(f"{i:<5} | {user['username']:<15} | {user['bio']:<30}")

                    print("------------------------------------------------------------\n")

            elif choice == "3": # APPROVE BY NUMBER
                print("\nFetching pending requests...")
                res = requests.get(f"{URL}?action=pending", headers=get_headers())
                pending = res.json()

                if not isinstance(pending, list) or len(pending) == 0:
                    print("\n--- No users are waiting for approval ---")
                else:
                    print("\n--- SELECT A USER TO APPROVE ---\n")
                    print("------------------------------------------------------------")
                    print(f"{'No.':<5} | {'Username':<15} | {'Bio':<30}")
                    print("------------------------------------------------------------")

                    for i, user in enumerate(pending, 1):
                        print(f"{i:<5} | {user['username']:<15} | {user['bio']:<30}")

                    print("------------------------------------------------------------")

                    try:
                        idx = int(input("\nEnter NUMBER to approve (0 to cancel): ")) - 1
                        if idx >= 0:
                            target = pending[idx]['username']
                            res_app = requests.post(f"{URL}?action=approve&username={target}", headers=get_headers())
                            print(f"Server: ✅ {res_app.json().get('message')}")
                    except: print("❌ Invalid selection.")

            elif choice == "4": # EDIT BY NUMBER
                print("\nFetching approved artists for editing...")
                res = requests.get(URL, headers=get_headers())
                approved = res.json()

                if not isinstance(approved, list) or len(approved) == 0:
                    print("\n--- The approved list is empty ---")
                else:
                    print("\n--- SELECT ARTIST TO EDIT ---\n")
                    print("------------------------------------------------------------")
                    print(f"{'No.':<5} | {'Username':<15} | {'Current Bio':<30}")
                    print("------------------------------------------------------------")

                    for i, user in enumerate(approved, 1):
                        print(f"{i:<5} | {user['username']:<15} | {user['bio']:<30}")

                    print("------------------------------------------------------------")
                    
                    try:
                        idx = int(input("\nEnter NUMBER to edit (0 to cancel): ")) - 1
                        if idx >= 0:
                            target = approved[idx]['username']
                            new_bio = input(f"Enter NEW bio for @{target}: ")
                            res_edit = requests.put(URL, headers=get_headers(), json={"username": target, "bio": new_bio})
                            print(f"Server: ✅ {res_edit.json().get('message')}")
                    except: print("❌ Invalid selection.")

            elif choice == "5": # DELETE BY NUMBER
                print("\nFetching approved artists for deletion...")
                res = requests.get(URL, headers=get_headers())
                approved = res.json()

                if not isinstance(approved, list) or len(approved) == 0:
                    print("\n--- The approved list is empty ---")
                else:
                    print("\n--- SELECT ARTIST TO DELETE ---\n")
                    print("------------------------------------------------------------")
                    print(f"{'No.':<5} | {'Username':<15} | {'Bio':<30}")
                    print("------------------------------------------------------------")

                    for i, user in enumerate(approved, 1):
                        print(f"{i:<5} | {user['username']:<15} | {user['bio']:<30}")

                    print("------------------------------------------------------------")
                    
                    try:
                        idx = int(input("\nEnter NUMBER to delete (0 to cancel): ")) - 1
                        if idx >= 0:
                            target = approved[idx]['username']
                            confirm = input(f"Are you sure you want to delete @{target}? (y/n): ")
                            if confirm.lower() == 'y':
                                res_del = requests.delete(f"{URL}?username={target}", headers=get_headers())
                                print(f"Server: ✅ {res_del.json().get('message')}")
                    except: print("❌ Invalid selection.")

            elif choice == "6":
                logged_in = False
                print("🔒 Logged out.")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"❌ Connection Error: {e}")