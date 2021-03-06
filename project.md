# Глава 1<br/>Задание и анализ предметной области

## 1.1. Задание
Разработать БД заказов интернет-сервиса по онлайн-проверке юридических документов.

## 1.2. Описание
Интернет-сервис по онлайн-проверке юридических документов должен иметь возможность принимать заказы от пользователей, хранить их и обрабатывать. Заказ представляет из себя загрузку пользователем файла (в одном из доступных для обработки фортматов) с текстом договора. Заказ формируется сразу при загрузке файла пользователем на сервер и получает статус "незавершенный заказ". Кроме того, в заказ добавляется сразу время и дата заказа, текст документа в режиме plain txt (исходный либо распознанный), а также, если исходный файл представлял из себя изображение или файл не в формате plain txt, дополнительно добавляется адрес сохраненного на сервере исходного файла. Кроме того, в заказ добавляется информация о виде загруженного договора (вид договора распознается автоматически).
После того, как пользователь завершает оформление заказа и производит его оплату, в заказ добавляются следующие данные:

* e-mail пользователя
* сторона, которой пользователь является по данному договору (напр., лизингодатель/лизингополучатель)
* тип проверки (автоматическая/экспресс/профессиональная)
* и заказ получает статус "завершенный заказ"

В зависимости от выбранного типа проверки, а также объема текста рассчитывается стоимость заказа, время на проверку договора и дедлайн выполнения заказа.

## 1.3 Анализ предметной области

### Сущности:
* заказ
* список загруженных файлов
* форматы данных
* договор
* виды договоров
* типы проверки
* проверяющий

### Атрибуты:
* **заказ** время и дата; договор; e-mail пользователя; тип проверки; завершенность заказа; стоимость; время выполнения; дедлайн проверки;
* **список загруженных файлов** адрес загруженного файла; формат данных;
* **форматы данных** название формата; необходимость распознавания; необходимость форматирования;
* **договор** текст договора; адрес загруженного файла; вид договора; сторона которой является пользователь;
* **виды договоров** навание вида договора; стороны по виду договора;
* **типы проверки** название типа проверки;
* **проверяющий** имя; e-mail проверяющего;

### Связи:
* **заказ – проверяющий** проверяет
* **заказ – типы проверки** тип проверки
* **заказ – договор** содержит договор
* **договор – список загруженных файлов** находится в
* **договор – виды договоров** является договором вида
* **список загруженных файлов – форматы данных** в формате

# Глава 2<br/>Модель предметной области

![model](https://raw.githubusercontent.com/gree-gorey/db/master/static/img/model.png "model")

# Глава 3<br/>ER-модель

Построим ER-модель по модели предметной области. Атрибуты пока опустим, чтобы не переусложнять модель. Рассмотрим связи (см. раздел 1.3) и для каждой определим ее кратность, например:

* заказ проверяет один проверяющий, при этом проверяющий может проверять много заказов => кратность связи "[заказ – проверяющий] проверяет"- N:1;
* у заказа может быть только один тип проверки, при этом на один тип проверки может быть много заказов => кратность связи "[заказ – типы проверки] тип проверки" N:1;
* один заказ содержит один договор, и один договор содержится в одном заказе => кратность связи "[заказ – договор] содержит договор" 1:1;
* один договор содержит один файл, файл относится к одному доовору => кратность связи "[договор – список загруженных файлов] находится в" 1:1;
* у договора может быть только один вид, а к одному виду договора может относиться много договоров => кратность связи "[договор – виды договоров] является договором вида" N:1;
* у файла может быть один формат, к одному формату может относиться много файлов => кратность связи "[список загруженных файлов – форматы данных] в формате" N:1;

![model](https://raw.githubusercontent.com/gree-gorey/db/master/static/img/er_model.png "model")


# Глава 4<br/>Модель БД

Базовый подход: каждая сущность и каждая связь переходит в таблицу в базе данных. Атрибутами таблиц становятся атрибуты сущностей и атрибуты связей.

## 4.1 Объединение отношений

В случае, когда кратность связи N:N, используется базовый подход. В противном случае можно сократить количество таблиц, когда кратность связи 1:N или N:1 до двух таблиц, а для кратности 1:1 - до одной. Решение по сокращению таблиц принимается в каждом случае индивидуально.

* "[заказ – проверяющий] проверяет", кратность N:1 – преобразуется в две таблицы `Order` и `Lawyer`;
* "[заказ – типы проверки] тип проверки", кратность N:1 – `Order` и `CheckType`;
* "[заказ – договор] содержит договор", кратность 1:1 – преобразуется в одну таблицу `Order`;
* "[договор – список загруженных файлов] находится в", кратность 1:1 – преобразуется в одну таблицу `Order`;
* "[договор – виды договоров] является договором вида", кратность N:1 – `Order` и `ContractType`;
* "[список загруженных файлов – форматы данных] в формате", кратность N:1 – `Order` и `Format`;


## 4.2 Таблицы и атрибуты

Составим перечень таблиц и запишем их атрибуты. Атрибуты, которые будут браться из соседних таблиц пометим символом #.

* Order(time, text, file_address, #format, #contract_type, party, user_e_mail, #check_type, #lawyer, done, cost, time_amount, deadline)
* Format(name, needs_recognition, needs_format)
* ContractType(name, parties)
* CheckType(name)
* Lawyer(name, e_mail)

## 4.3 Ключевые поля


## 4.4 Нормализация


# Глава 5<br/>Работа с БД


# Глава 6<br/>Разработка интерфейса