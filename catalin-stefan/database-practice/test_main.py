from fastapi.testclient import TestClient
from main import app

client=TestClient(app)
# i)test api call
def test_get_all_blogs():
    response=client.get("/blog/all")
    assert response.status_code==200
# ii)test token creation – failure - test scenario when no token is present, we need to present error message
def test_auth_error():
    response=client.post("/token",data={"username":"","password":""})
    access_token=response.json().get("access_token")
    assert access_token==None
    message=response.json().get("detail")[0].get("msg")
    assert message=="field required"
# iii)test token creation - success - test scenario when token is present
def test_auth_success():
    response=client.post("/token",data={"username":"john","password":"john"})
    access_token=response.json().get("access_token")
    assert access_token
# iv)test api call with generated token - test scenario to make api call with created token
def test_post_article():
    auth=client.post("/token",data={"username":"john","password":"john"})
    access_token=auth.json().get("access_token")

    assert access_token

    response=client.post("/article/",
                         json={"title":"Test article","content":"Test content","published":True,"creator_id":1},
                         headers={"Authorization":"bearer "+access_token}
                         )
    assert response.status_code==200
    assert response.json().get("title")=="Test article"
