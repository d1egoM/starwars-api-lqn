# 🌌 StarWars GraphQL API

Este proyecto es una API construida con Django y Graphene que expone datos del universo de **Star Wars** usando **GraphQL**. Utiliza contenedores Docker para facilitar su despliegue y ejecución.

---

## 🚀 Características

- API GraphQL para consultar:
  - Personajes
  - Planetas
  - Películas
- Modelado relacional usando Django ORM
- Backend desarrollado con Django
- GraphQL usando Graphene
- Contenerización con Docker y Docker Compose
- Carga de datos desde fixtures
- Pruebas unitarias e integradas

---

## 🧱 Tecnologías

- Python 3.12+
- Django 4.2.23
- Graphene-Django 3.2.3
- SQLite (modo desarrollo)
- Docker & Docker Compose

---

## 🐳 Instalación con Docker

1. Clona el repositorio:

```bash
git clone https://github.com/d1egoM/starwars-api-lqn
cd starwars-api-lqn
```

2. Construye y levanta los servicios:

```bash
docker compose up --build
```

3. Aplica las migraciones y carga datos:

```bash
docker compose exec starwars_api python manage.py migrate
docker compose exec starwars_api python manage.py loaddata initial_data
```

4. Accede a la interfaz GraphQL en:

```
http://localhost:8000/graphql/
```

---

## 🧪 Pruebas

```bash
docker compose exec starwars_api python manage.py test
```

---

## 📁 Estructura del Proyecto

```
├── starwars
│ ├── admin.py
│ ├── apps.py
│ ├── fixtures
│ │ └── initial_data.json
│ ├── migrations
│ ├── models.py
│ ├── mutations.py
│ ├── queries.py
│ ├── schema.py
│ ├── tests
│ │ ├── test_graphql.py
│ │ └── test_models.py
│ ├── types.py
│ └── views.py
└── starwars_api
├── asgi.py
├── db.sqlite3
├── settings
│ ├── base.py
│ ├── dev.py
│ └── prod.py
├── urls.py
└── wsgi.py
├── Dockerfile
├── README.md
├── docker-compose.yml
├── manage.py
├── requirements.txt
└──  schema.py
```

---

## 📚 Ejemplo de Consulta GraphQL

```graphql
query {
  allCharacters {
    id
    name
    homeworld {
      name
    }
    movies {
      title
    }
  }
}
```

---

## 📄 Licencia

Este proyecto es de uso educativo y libre. No afiliado con Disney o Lucasfilm.

---

## 👨‍💻 Autor

Diego Martínez – [https://github.com/d1egoM](https://github.com/d1egoM/starwars-api-lqn)

---

## 🌠 Que la fuerza te acompañe.