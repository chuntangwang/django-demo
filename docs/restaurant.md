# Restaurant App

A demo for restaurant review system

## Init app

Clone project and install dependencies with [uv](https://github.com/astral-sh/uv)

```shell
# clone project, then checkout branch
git clone --branch feature/restaurant https://github.com/chuntangwang/django-demo
# create venv and install package
uv sync
```

Run project

```shell
# load venv
source .venv/bin/activate

# run server
python manage.py runserver

# using open api with drf-spectacular and swagger ui
python manage.py spectacular --color --file schema.yml
docker run -p 80:8080 -e SWAGGER_JSON=/schema.yml -v ${PWD}/schema.yml:/schema.yml swaggerapi/swagger-ui
```

Open API:
* swagger-ui: http://127.0.0.1:8000/api/schema/swagger-ui/
* redoc: http://127.0.0.1:8000/api/schema/redoc/

Exported Open API html file:
* [redoc-static.html](redoc-static.html)

## Model Design

Database: `db.sqlite3`

```mermaid
---
title: Restaurant
---
erDiagram
    RESTAURANT {
        int id PK
        string name UK
        string description
        string user_id FK
    }
    REVIEW {
        int id PK
        int restaurant_id FK
        int user_id FK
        int score
        string comment
    }
    USER {
        int id PK
        string name
        string email
        string password
    }
    RESTAURANT ||--o{ REVIEW: "contains"
    USER ||--o{ RESTAURANT: "creates"
    USER ||--o{ REVIEW: "creates"
```

## Sample Database: `db.sqlite3`

### Demo account

* superuser
    * `admin` / `admin123456`
* user
    * `user` / `user123456`
    * `foodie` / `foodie123456`

### Create sample data

#### POST /api/v1/register

```json
{
  "username": "user",
  "email": "user@example.com",
  "password": "user123456"
}

{
  "username": "foodie",
  "email": "foodie@example.com",
  "password": "foodie123456"
}
```

#### POST /api/v1/restaurants/

```json
{
  "name": "八方雲集",
  "description": "源於臺灣的跨國台式麵食連鎖店，1998年成立，創辦人林家鈺，以鍋貼、水餃為主力商品。它與四海遊龍並列為台灣鍋貼連鎖店兩強。"
}

{
  "name": "春水堂人文茶館",
  "description": "是一家源自臺灣臺中的連鎖茶館。主要商品為珍珠奶茶及泡沫紅茶等各式調和茶飲，並推廣半發酵茶葉，提倡雙杯式飲法及色香味三段品茗法。是聲稱發明珍珠奶茶的臺灣連鎖餐廳之一，另一家是翰林茶館。"
}

{
  "name": "鼎泰豐",
  "description": "1958年成立，最初為油行，1972年轉為餐廳兼賣小籠包。1996年，鼎泰豐日本新宿店開幕，發展為跨國企業。在1993年曾被《紐約時報》評為“世界十大美食餐廳”之一。2010年香港尖沙咀分店獲得米其林一星，是台灣首間獲《米其林指南》列入星級的餐廳。"
}

{
  "name": "我家牛排",
  "description": "主打平價和吃到飽（組合）的自助沙拉吧。"
}

{
  "name": "西堤牛排",
  "description": "（英語：TASTY）為王品集團旗下的連鎖餐廳品牌，創辦人陳正輝。"
}

{
  "name": "翰林茶館",
  "description": "於1986年，由凃宗和成立，總部位於臺南市。主要產品為台灣茶文化類商品，如茶的相關飲品及餐點，在台灣已有多家直營店。其與春水堂人文茶館各自宣稱先後研發珍珠奶茶。"
}

{
  "name": "天仁茶業",
  "description": "創始於1953年的臺灣茶葉經銷企業，旗下連鎖門市名為「天仁茗茶」。"
}

{
  "name": "城市漢堡",
  "description": "是一個連鎖早午餐品牌。總部位於桃園市，成立於2016年，創始人為李明宗。目前全台約有150家加盟門市。"
}

{
  "name": "摩斯漢堡",
  "description": "源自日本的跨國連鎖速食餐廳（快速休閒餐廳），由櫻田慧與渡邊和男、吉野祥於1972年在東京創立。"
}
```

#### POST /api/v1/reviews/

**user posted**

```json
{
  "restaurant_id": 1,
  "score": 3,
  "comment": "酸辣湯才是主角"
}

{
  "restaurant_id": 2,
  "score": 5,
  "comment": "珍珠奶茶好喝！"
}

{
  "restaurant_id": 3,
  "score": 4,
  "comment": "有夠貴，我家隔壁巷子好吃又便宜！"
}

{
  "restaurant_id": 4,
  "score": 4,
  "comment": "從小吃到大的好味道"
}

{
  "restaurant_id": 5,
  "score": 3,
  "comment": "👍👍👍"
}

{
  "restaurant_id": 6,
  "score": 4,
  "comment": "👍👍👍👍"
}

{
  "restaurant_id": 7,
  "score": 5,
  "comment": "❤❤❤❤❤"
}
```

**foodie posted**

```json
{
  "restaurant_id": 1,
  "score": 4,
  "comment": "酸辣湯超好喝！"
}

{
  "restaurant_id": 2,
  "score": 5,
  "comment": "氣氛不錯，適合久坐聊天"
}

{
  "restaurant_id": 3,
  "score": 5,
  "comment": "每次回國必吃，台灣的家鄉味"
}

{
  "restaurant_id": 8,
  "score": 2,
  "comment": "😒😒"
}

{
  "restaurant_id": 9,
  "score": 1,
  "comment": "😢"
}

{
  "restaurant_id": 10,
  "score": 5,
  "comment": "紅茶好好喝❤"
}
```
