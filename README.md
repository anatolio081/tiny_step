# stepik_tinysteps


## Installation

### Установка проекта
Для начала работы с проектом достаточно: 
- установить Python3 (https://www.python.org/) 
- клонировать проект в свою рабочую папку

```sh
git clone https://github.com/anatolio081/stepik_travel.git
cd stepik_travel
``` 
- настроить виртуальное окружение (venv)

```sh
python3 -m venv env
source env/bin/activate 
pip install -U pip
pip install -r requirements.txt 
```
- Запустить проект:
```sh
gunicorn app:app 
```
