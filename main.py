import requests
from bs4 import BeautifulSoup

# 時間割URL
URL = "https://www.k.kyoto-u.ac.jp/student/u/t/entry/zenki"

LOGIN_INFO = {
    "j_username": "a0163601",
    "j_password": "cHoco0923",
    "_eventId_proceed": ""
}

# LOGIN
s = requests.session()
res = s.get(URL)
res = s.post(res.url, data=LOGIN_INFO)
soup = BeautifulSoup(res.text, "html.parser")
inputs = soup.find_all("input")
saml_data = {
    "RelayState": inputs[0].get("value"),
    "SAMLResponse": inputs[1].get("value")
}
res = s.post(soup.form.get("action"), data=saml_data)

# Fetch mail
soup = BeautifulSoup(res.text, "html.parser")
new_imgs = soup.find_all("img", id="id_img_1172_0")

for i, new in enumerate(new_imgs):
    address = new.findPreviousSibling("a").get("href")
    types = address[: address.find("top")]
    number = address[address.find("no=") + 3: address.find("&from")]
    res = s.get("https://www.k.kyoto-u.ac.jp" + types + "course_mail_list?no=" + number)
    soup = BeautifulSoup(res.text, "html.parser")
    mail = soup.find("a", id="id_a_1240_1").get("href")
    res = s.get("https://www.k.kyoto-u.ac.jp" + types + mail)
    soup = BeautifulSoup(res.content, "html.parser")
    contents = soup.find_all("td", class_="odd_normal")
    subject = contents[0].string
    date = contents[6].string
    title = contents[7].string
    contents = contents[8].text

    text_name = "mail" + str(i)
    with open(text_name, "w") as f:
        f.write(subject + date + title + contents)
