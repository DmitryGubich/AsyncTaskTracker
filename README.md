## UberPopugInc

#### Awesome Task Exchange System (aTES) for UberPopug Inc

Диаграммы приложения:

* [Общая схема приложения для нулевой домашки (до всего курса)](https://miro.com/app/board/uXjVMw_TyiA=/?share_link_id=795541479315)
* [Event storming, Data model, Services и Event схемы](https://miro.com/app/board/uXjVMwrO9Fc=/?share_link_id=611585265044)



## Переход на новую версию события
1. Создаём новую версию сообщения в [Schema registry](https://github.com/DmitryGubich/UberPopugIncSchemas). Папка `schemas`.
2. Публикуем новую версию библиотеки.
3. Переходим на новую версию библиотеки в сервисах-консьюмерах, поддерживая одновременно обработку событий двух версий.
4. Переходим на новую версию библиотеки в сервисах-продьюсерах, переставая публиковать события в старом формате.
5. Рефакторинг сервисов-консьюмеров – перестаём обрабатывать события старого формата.
