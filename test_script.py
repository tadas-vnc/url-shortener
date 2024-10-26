# for testing API endpoint in backend

import requests

BASE_URL = "http://127.0.0.1:5000"

def test_shorten_url(source, alias = None, password = None):
    print("Testing /shorten endpoint...")
    payload = {
        "source_url": source
    }
    if(alias is not None):
        payload["alias"] = alias
    if(password is not None):
        payload["password"] = password
    response = requests.post(f"{BASE_URL}/shorten", json=payload)
    print("Response:", response.json())
    return response.json()  

def test_redirect(short_url):
    print("Testing redirect on GET /<alias> endpoint...")
    response = requests.get(f"{BASE_URL}/{short_url}")
    print("Status Code:", response.status_code)
    print("Redirected URL:", response.url if response.is_redirect else "No redirect")

def test_update_url(alias, password, source = None, new_alias = None, new_password = None):
    print("Testing /update endpoint...")
    payload = {
        "alias": alias,
        "password": password
    }
    if(source is not None):
        payload["new_source_url"] = source
    if(new_alias is not None):
        payload["new_alias"] = new_alias
    if(new_password is not None):
        payload["new_password"] = new_password
    response = requests.post(f"{BASE_URL}/update", json=payload)
    try:
        print("Response:", response.json())
    except:
        print("Response:", response.text)

def test_delete_url(alias, password):
    print("Testing DELETE /delete endpoint...")
    payload = {
        "alias": alias,
        "password": password
    }
    response = requests.delete(f"{BASE_URL}/delete", json=payload)
    print("Response:", response.json())
source_url = "https://www.google.com/search?sca_esv=fa4253f7b1e1cfcc&sxsrf=ADLYWIKChFL30Fw3qkUoPBxZz_ETk3aH1w:1729942652375&q=cat+pictures&udm=2&fbs=AEQNm0Aa4sjWe7Rqy32pFwRj0UkWd8nbOJfsBGGB5IQQO6L3J_86uWOeqwdnV0yaSF-x2jornR9l9QoC_W7eufnFEmyEHeDjy4O0OWyYQ0fz3JjBQfGYnxplk1tJrXWXGVUQmsq8GmAE9Q1XW7FW1vkgCJssYdAy0IKQq2tR8PJjONL933B-eBuE-V0FnNrJe0NHfwCxxYP0&sa=X&ved=2ahUKEwiE8JrK-quJAxUMgP0HHcenKIoQtKgLegQIFRAB&biw=1920&bih=963&dpr=1"
new_source = "https://static.vecteezy.com/system/resources/thumbnails/024/646/930/small_2x/ai-generated-stray-cat-in-danger-background-animal-background-photo.jpg"
#test_shorten_url(source_url)
#test_shorten_url(source_url, "cats")
#test_shorten_url(source_url, "cats","password") # already taken
#test_update_url("cats","sE6OYvEp", new_password="password123")
#test_update_url("cats","password123", new_alias="cat_image",source=new_source)
#test_redirect("cat_image")
test_delete_url("cat_image","wrong_password")
test_delete_url("cat_image","password123")
