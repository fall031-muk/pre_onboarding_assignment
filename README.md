# [위코드 X 원티드] 백엔드 프리온보딩 선발과제

### 유저 생성, 인가, 인증 구현
### 게시물 C.R.U.D 구현하기

---

## 구현한 방법과 이유에 대한 간략한 내용

### 사용자

- 유효성, 중복, 암호화를 고려한 회원가입 (보안강화)
- JWT 토큰을 사용하여 사용자의 인증과 인가 기능 구현 (게시판 수정 및 삭제 권한)

### 게시판

- 게시글을 읽기 위한 별도의 자격은 없음 (비회원 게시글 확인 가능)
- 게시글을 작서하기 위하여 사용자 로그인 필요
- 게시글을 작성한 사용자는 자신이 로그인 시 발급되는 JWT 토큰을 활용하여 확인하였고, 각 사용자는 본인의 게시물만 수정 및 삭제 가능 (타 유저 게시글 수정 및 삭제 불가)

---

## 자세한 실행 방법(endpoint 호출방법)

### ENDPOINT

| Method | endpoint | Request Body | Remark |
|:------:|-------------|------|--------|
|POST|/users/signup|name, email, password|회원가입|
|POST|/users/login|email, password|로그인|
|POST|/posts|title, content|게시물 작성|
|GET|/posts/post_id||게시물 조회|
|DELETE|/posts/post_id||게시물 삭제|
|PUT|/posts/post_id|content|게시물 수정|
|GET|/posts/list?limit=3&offset=0||게시물 목록 조회|

---

## API 명세(request/response 서술 필요)

### 1. 회원가입
- Method : POST
- EndpointURL : /users/signup
- Remark : (email : @와 .이 포함된 이메일 형식), (password : 8자리 이상. 숫자, 문자, 특수문자 포함)
- Request
```
POST "http://127.0.0.1:8000/users/signup HTTP/1.1"
{
    "name" : "muk",
    "email" : "muk@gmail.com",
    "password" : "mukmuk12!"
}
```
- Response
```
{
    "MESSAGE": "SUCCESS"
}
```

### 2. 로그인
- Method : POST
- EndpointURL : /users/login
- Remark : (email : @와 .이 포함된 이메일 형식), (password : 8자리 이상. 숫자, 문자, 특수문자 포함)
- Request
```
POST "http://127.0.0.1:8000/users/login HTTP/1.1"
{
    "email" : "muk@gamil.com",
    "password" : "mukmuk12!",
}
```
- Response
```
{
    "MESSAGE": "SUCCESS",
    "ACCESS_TOKEN": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NH0.ALnstfNp6Cbca2R26cWRnFnHEAlIrU9O5u4pZnRk2tY"
}
```

### 3. 게시물 
- Method : POST
- EndpointURL : /posts
- Remark : 로그인한 유저만 게시글 작성 가능
- Request
```
POST "http://127.0.0.1:8000/posts HTTP/1.1"
{
    "title"   : "test게시글",
    "content" : "내용 test입니다"
}
```
- Response
```
{
    "MESSAGE": "CREATE",
    "data": {
        "title": "test게시글",
        "username": "muk",
        "content": "내용 test입니다",
        "created_at": "2021-10-24 20:36:01"
    }
}
```

### 4. 게시물 조회
- Method : GET
- EndpointURL : /posts/post_id
- Request
```
GET "http://127.0.0.1:8000/posts/1 HTTP/1.1"
```
- Response
```
{
    "Result": {
        "username": "muk1",
        "title": "1번 게시글",
        "content": "1번 게시글 내용입니다",
        "created_at": "2021-10-19 01:59:27"
    }
}
```

### 5. 게시물 수정
- Method : PATCH
- EndpointURL : /posts/post_id
- Remark : 로그인한 유저가 본인의 게시물 수정 가능
- Request
```
PATCH "http://127.0.0.1:8000/posts/13 HTTP/1.1" 
{
   "content" : "내용 수정test입니다"
}
```
- Response
```
{
    "MESSAGE": "SUCCESS"
}
```

### 6. 게시물 삭제
- Method : DELETE
- EndpointURL : /posts/post_id
- Remark : 로그인한 유저가 해당 게시물 삭제 가능
- Request
```
DELETE "http://127.0.0.1:8000/posts/13 HTTP/1.1"
```
- Response
```
{
    "MESSAGE": "DELETE"
}
```

### 7. 게시물 목록 조회
- Method : GET
- EndpointURL : /posts/list?limit=5&offset=0
- Remark : 게시글 리스트 조회 기능, QueryParams(limit/offset)로 페이지네이션 가능
- Request
```
GET "http://127.0.0.1:8000/posts/list?offset=0&limit=5 HTTP/1.1"
```
- Response
```
{
    "count": 5,
    "Result": [
        {
            "username": "muk1",
            "title": "1번 게시글",
            "content": "1번 게시글 내용입니다",
            "created_at": "2021-10-19 01:59:27"
        },
        {
            "username": "muk1",
            "title": "2번 게시글",
            "content": "2번 게시글 수정 내용입니다",
            "created_at": "2021-10-19 01:59:57"
        },
        {
            "username": "muk1",
            "title": "4번 게시글",
            "content": "4번 게시글 내용입니다",
            "created_at": "2021-10-19 02:00:09"
        },
        {
            "username": "muk1",
            "title": "5번 게시글",
            "content": "5번 게시글 내용입니다",
            "created_at": "2021-10-19 02:00:15"
        },
        {
            "username": "muk2",
            "title": "6번 게시글",
            "content": "6번 게시글 내용입니다",
            "created_at": "2021-10-19 02:00:31"
        }
    ]
}
```
