# Бот для прогона заявок КК ЮЛ 

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Selenium](https://img.shields.io/badge/-selenium-%43B02A?style=for-the-badge&logo=selenium&logoColor=white)
![CSS3](https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white)
![Qt](https://img.shields.io/badge/Qt-%23217346.svg?style=for-the-badge&logo=Qt&logoColor=white)


> <picture>
>   <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/Mqxx/GitHub-Markdown/main/blockquotes/badge/light-theme/warning.svg">
>   <img alt="Предупреждение" src="https://raw.githubusercontent.com/Mqxx/GitHub-Markdown/main/blockquotes/badge/dark-theme/warning.svg">
> </picture><br>
>
> Данный бот находится в разработке и не настроен для универсального использования на разных стендах КК ЮЛ.


## Начало работы:

1. Запустить в консоли 
```
pip install -r requirements.txt
```
2. Запустить в консоли:
```
python -m root.app.app
```
3. В показавшемся окне либо ввести номер заявки (тогда запуск бота будет по конкретной заявке), либо не вводить (тогда будет создана новая заявка)
4. Проставить чекбоксы по желаемым подзадачам (рекомендуется отмечать либо все подзадачи через самый верхний чекбокс, либо каждый пункт с определенного этапа по другой, без промежутков между задачами)
5. Нажать кнопку Запустить, словить кучу багов и потратить N-ное количество времени на изучение кодовой базы бота и его отладку 😄

## Основная суть

Бот работает на основе Selenium - движка для тестирования различных сценариев поведения. В коде бота модульно настраивается сценарий поведения (начиная от базовых функций, заканчивая прописыванием цепочки действий для каждого этапа заявки), который затем воспроизводится либо через интерфейс от PyQT, либо через запуск python-скрипта.

## Общая структура

В боте можно выделить несколько основных блоков, необходимых для корректной настройки под нужную конфигурацию стенда:

### 1. Конфигурационный файл 
* находится в `config/config.json`
* содержит все данные для работы бота, которые построены по определенной структуре:
```
├── app (ссылка на сервер и на прикладываемый файл)
├── creds (все необходимые логины/пароли)
└── selectors (CSS-селекторы для каждого взаимодействия)
    ├── platform (селекторы для платформенных элементов по типу иконки логаута)
    └── app (селекторы для виджетов приложения, для удобства разбитые на группы, как по этапам, так и по некоторым наиболее часто встречающимся виджетам, например, группе кнопок, группе вкладок и т.д.)
```
* наиболее часто изменяемый файл, т.к. для любого нового взаимодействия необходимо сначала внести CSS-селектор в файл (либо найти подходящий из того списка, который уже есть)
* содержит специальный блок `tabs`, который содержит селекторы для всех групп вкладок и обладает своей логикой использования (больше становится понятно при работе с основным кодом бота). Такое же обобщение логики есть для групп кнопок (поля обычно, но не всегда, имеют постфикс button_group, а также всегда состоят из полей `selector` и `order`) 

### 2. Базовые методы класса testdriver
* расположены в файле `root/api/testdriver.py`
* включают в себя основные простейшие действия (нажатие на кнопку, ввод значения в поле и т.д.), а также некоторые более комплексные наборы действий, которые можно объединить в одну цепочку (залогиниться/разлогиниться, найти объект в таблице)
* платформа, в целом, не предназначена для "нечеловечески" быстрых действий, это зачастую порождает неожиданные поломки в любом месте. Даже преднамеренное замедление бота не гарантирует выполнение действия в 100% случаев. Поэтому, `testdriver` содержит python-декоратор `retry`, который позволяет в случае отказа какой-либо функции повторить ее выполнение 5 раз (обычно это помогает преодолеть баги, связанные со спецификой платформы, если спустя 5 попыток функция все равно отказывает - значит вероятно дело в коде).
* в целом, большинство методов протестировано на нескольких примерах, но можно добавлять свои методы для наиболее часто повторяющихся цепочек действий.

### 3. Сценарии этапов заведения заявки
* отдельные файлы под каждый этап, находятся в директории `root/api/stages`
* каждый файл содержит единственный класс для этапа (наследуется от `testdriver`), который, в свою очередь, содержит один или несколько верхнеуровневых методов, описывающих часть этапа (например, для этапа прескоринг в файле `prescoring.py` в классе `prescoring` определено 3 метода: для проведения прескоринга, для информирования клиента и для прикрепления документов) 
* в конечном итоге, в файле `root/api/scenario.py` собирается итоговый класс `scenario_tester`, который наследуется от всех классов, находящихся в папке `stages`, и именно его методы реализуются в скриптах для запуска бота

### 4. Логи
* записываются как в консоль, так и в папку `logs`. В файлы обычно записываются только ошибки.
* порождаются декораторами `retry` и `exit_with_grace`
* разделены на папки `bot_errors` (запись ошибок бота во время воспроизведения сценариев) и `platf_errors` (запись багов в формраннере во время воспроизведения сценариев, механизм находится в разработке)