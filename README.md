# 정지원 Wanted 기술과제
  ✅ 원티드랩 기술 과제입니다.
- HP : 01099561993
- Email : jung2one@gmail.com

### **[기능 개발]**

✔️ **REST API 기능**

- 회사명 자동완성
    - 회사명의 일부만 들어가도 검색이 되어야 합니다.
- 회사 이름으로 회사 검색
- 새로운 회사 추가 (태그 같이 추가)
- 회사 태그 정보 추가
- 회사 태그 정보 삭제


# ⚒️ 기술 환경 및 tools
- Back-End: python 3.11
- Framework: FastAPI 0.115.6
- ORM: SqlAlchemy 2.0.36, Pydantic 2.10.3
- DB: MySQL
- WAS: Uvicorn
- ETC: Git, Github, Docker
- Test: Pytest
- 가상환경: pipenv

# 📋 모델링 ERD

![wanted_erd](https://user-images.githubusercontent.com/64240637/140931939-781a552f-46ed-46be-a239-85751fd329f1.png)
- companies와 company_names는 one-to-many 관계
  + companies가 여러 언어의 명의를 가질수 있음, 언어가 추가 될 수있음
  + 언어는 company_names의 language_code로 관리

- companies와 tags는 company_tags를 bridge table로 둔 many-to-many 관계
  + companies는 여러 태그를 가질 수 있고 tags도 여러 회사에 해당할수 있음

- tags 와 multi_language_tag_names는 one-to-many 관계
  + 이부분 고민이 가자 많았음, tags에 저장할 대표 이름을 명시가 test 구조상 불가능
  + 언어가 달라도 의미가 같으면 같은 태그로 그룹화
  + 언어의 종류는 multi_language_tag_names의 language_code로 관리


<hr>

# 디렉토리 구조
```
├── company
│   ├── routes
│   │   ├── delete.py
│   │   ├── get.py
│   │   ├── post.py
│   │   └── put.py
│   ├── models.py
│   ├── schema.py
│   └── urls.py
│  
├── config
│   ├── database.py
│   └── models.py
│  
├── .dockerignore
├── .gitignore
├── company_tag_sample_csv
├── csv_data_uploader.py
├── docker-compose.yml
├── Dockerfile
├── main.py
├── Pipfile
├── Pipfile.lock
├── README.md
├── requirements.txt
├── test_config.py
└── test_senior_app.py
```
<hr>

# 🔖 API 명세서
SWAGGER : local에서 `python3 main.py` 실행 후 http://127.0.0.1:8000/docs 접속


# 🔖 설치 및 실행 방법

1. 가상환경은 pipenv를 사용하였습니다, pipenv를 사용하셔도 좋고 requirements.txt 이용하여 편하신 가상환경 사용
  ```
  pip install pipenv
  pipenv shell
  pipenv install
  ```

2. mysql 설치

3. 프로젝트 데이터베이스 생성
  database.py에 기본 default db 정보 입력하였습니다. 로컬 MySQL 사용시 사용자는 root, pwd는 ""

  개인 계정으로 변경 희망시 베이스 디렉토리에서 env.sh 파일 만드신후 
  ```
  export DB_USER='{사용자명}'
  export DB_PW='{비밀번호}'
  export DB_HOST='{호스트}'
  export DB_PORT='{포트}'
  ```

  적용
  ```
  source env.sh
  ```

  mysql 접속후
  ```
  create database wanted_lab character set utf8mb4 collate utf8mb4_general_ci;
  create database test_db character set utf8mb4 collate utf8mb4_general_ci;
  ```

4. 데이터 세팅
 최초 진입시 `python3 csv_data_uploader.py` 실행하면 모델 디비마이그레이션과 csv파일에 해당하는 데이터 세팅 가능
!!!!(주의)!!!! 여러번호출에 대한 예외처리는 안되어있는 상태, 여러번 호출시 디비 드랍하고 다시 실행하길 추천

5. `python3 main.py`로 로컳 서버 실행


# 🔖  테스트 실행 방법

1.  `pytest test_senior_app.py` 실행
  - 기본으로 csv파일 업로드가 되도록 설정하여 따로 디비 설정 불필요



# 회고
- 구조를 혼자서 복잡하게 생각했나 싶어서 조금 아쉬웠습니다. 제가 기존에 생각한 구조가 아니였다는 것을... 뒤늦게 알아버려서 갈아 엎는 작업이 있었어요!
  + 기존에는 tags에 flat하게 ko, en, jp 컬럼을 두고 companies에도 kor name, eng name 이런식으로 플랫하게 가져가려다가 같은 tag를 보고 있더라도 어떤 언어를 가져갈지 고를수가 있더라구요
- 원격 DB 세팅 시간이 부족해서 Docker 세팅이 부족합니다! 양해 부탁드리겠습니다 ㅜㅜ
- 원래 TortoisORM이라는 Django like orm을 사용하다가 처음 SqlAlchemy를 써봤습니다!
- 파일 구조는 현재 즐겨 사용하는 구조로 가져왔습니다.