# 🛡️ Taskify — Multi-Tenant Task Management API

Профессиональный REST API сервиса управления задачами с поддержкой **мультитенантности** (строгая изоляция данных между организациями), авторизацией по JWT и полным покрытием ключевых бизнес-сценариев тестами.

---

## 🛠 Технологический стек

- **Backend:** Python 3.11, Django 5.0, Django REST Framework
- **Database:** PostgreSQL
- **Security & Auth:** Simple JWT (Bearer Tokens), Role-Based Access Control
- **Testing:** Pytest, Pytest-Django (изоляция данных и бизнес-логика)
- **Containerization:** Docker, Docker Compose

---

## 🔑 Ключевые особенности

1. **Мультитенантность (Data Isolation):**
   - Строгая изоляция проектов и задач на уровне организаций.
   - Защищенные тестами проверки на невозможность доступа пользователей одной организации к данным другой.
2. **Аутентификация & Разграничение прав:**
   - JWT-токены (Access/Refresh).
   - Разграничение прав между владельцами, администраторами и участниками организаций.
3. **Готовность к Production:**
   - Полноценная работа с PostgreSQL.
   - Упаковка сервиса и СУБД в изоляты Docker.

---

## 🚀 Быстрый запуск через Docker

### Требования
- Установленный [Docker Desktop](https://www.docker.com/products/docker-desktop/)

### Инструкция по установке

1. **Клонируйте репозиторий:**
   ```bash
   git clone [https://github.com/ВАШ_NICKNAME/DRF-Taskify.git](https://github.com/ВАШ_NICKNAME/DRF-Taskify.git)
   cd DRF-Taskify