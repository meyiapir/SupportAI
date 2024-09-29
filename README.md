# SupportAI

## Описание
SupportAI — это проект, направленный на создание умного помощника на базе искусственного интеллекта. 

## Версии
**V1** - Опирается исключительно на данные из датасета (CPU).
**V2** - Делает суммаризацию двух подходящих ответов для пользователя, что делает итоговый текст более понятным, но менее точным (CPU).
**V3** - Экспериментальная вресия, основанная на Deep Learning модели, что требует использование графических ускорителей (GPU).

## Установка

### Требования
Убедитесь, что у вас установлены следующие компоненты:
- Docker
- Docker Compose

### Запуск проекта

1. **Запуск с помощью Docker Compose**:
   Для запуска всех сервисов проекта используйте следующую команду:
   ```bash
   docker-compose -f docker-compose.dev.yml up -d
   ```

2. **Запуск вручную**:
   Если вы предпочитаете запускать каждый сервис вручную, выполните следующие шаги:
    - Установите все необходимые зависимости:
      ```bash
      pip install -r requirements.txt
      ```
    - Запустите каждый сервис отдельно, следуя инструкциям в документации или в файлах `docker-compose`.

## Использование
После успешного запуска проекта вы можете использовать API или интерфейс пользователя для взаимодействия с функционалом SupportAI.
