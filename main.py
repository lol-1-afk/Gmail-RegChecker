import requests
import easygui

file_path = None
emails_list = []
exists_list = []


class Counter:
    exists = 0
    doesnt_exist = 0


def reg_check(email_to_check: str) -> None:
    base_uri = "https://mail.google.com/mail"

    check = requests.get(f"{base_uri}/gxlu?email={email_to_check}")  # GET request to gmail web api

    if check.cookies.get("COMPASS"):  # if email exists, response will contain "COMPASS" cookie with "gmail=..."
        Counter.exists += 1
        print(f"Email exists: {email}")
        exists_list.append(email_to_check)
    else:
        Counter.doesnt_exist += 1
        print(f"Email doesn't exist: {email}")


while file_path is None:
    file_path = easygui.fileopenbox(msg="Select file fith emails")

with open(file_path, errors="ignore", encoding="utf-8") as emails_file:
    emails_list = emails_file.read().splitlines()

print(f"Now starting checker. To check: {len(emails_list)} lines..")
for email in emails_list:  # TODO: add multi-threading
    if email.count(":") > 0:  # if line like email:password
        email = email.split(":")[0]

    if "@gmail.com" not in email:
        continue

    reg_check(email_to_check=email)

print(f"Done! Success: {Counter.exists}; fail: {Counter.doesnt_exist}")

with open("exists.txt", "w", errors="ignore", encoding="utf-8") as save_file:
    save_file.write("\n".join(exists_list))
