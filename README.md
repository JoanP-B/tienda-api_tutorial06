# Tienda API: Django, Docker y AWS RDS MySQL

La aplicación ofrece una tienda web en `/` y expone el catálogo y la operación
de compra en `/api/v1/comprar/`. Nginx recibe las solicitudes HTTP en el puerto
80 y las reenvía a Django, servido por Gunicorn en la red interna de Docker.
Django se conecta a una instancia MySQL administrada (por ejemplo, AWS RDS),
externa a Docker Compose.

## Requisitos

- Docker con Docker Compose v2
- Una instancia MySQL accesible desde el equipo o la EC2
- Una base de datos creada en MySQL (por defecto, `djangodocker`)

## Configuración

Copia `.env.example` a `.env` sin sobrescribir un `.env` existente:

```bash
cp .env.example .env
```

Edita `.env` y configura:

- `SECRET_KEY`: una clave secreta aleatoria.
- `DEBUG`: `0` en AWS/producción; `1` solo durante desarrollo.
- `DJANGO_ALLOWED_HOSTS`: lista de hosts separada por comas. El valor de ejemplo
  `*` permite cualquier host; en producción, reemplázalo por la IP o dominio.
- `SQL_HOST`: endpoint de RDS o hostname del servidor MySQL.
- `SQL_DATABASE`, `SQL_USER`, `SQL_PASSWORD` y `SQL_PORT`: valores de tu instancia.

El archivo `.env` contiene secretos: no lo agregues a Git ni lo compartas.
Si la contraseña contiene `$`, escápalo como `$$` en la configuración interpretada
por Docker Compose. Por ejemplo, `"clave!#$$tjJW"` representa la contraseña literal
`clave!#$tjJW`.

## Ejecutar localmente contra MySQL/RDS

La máquina donde corre Docker debe poder conectarse al host MySQL por TCP `3306`.
En AWS RDS, permite ese puerto en el security group de la base únicamente desde la
IP pública del equipo durante pruebas, o desde el security group de EC2 para AWS.

```bash
docker compose up --build -d
docker compose ps
docker compose logs --tail=100 web
docker compose logs --tail=100 nginx
```

El entrypoint ejecuta las migraciones y luego inicia Gunicorn. Solo Nginx publica
un puerto en el host; Django escucha en el puerto 8000, accesible únicamente
dentro de la red de Docker. Comprueba la tienda en `http://localhost/` o
`http://localhost/api/v1/comprar/` desde el navegador. La segunda ruta muestra la
misma tienda cuando se solicita HTML y conserva la respuesta JSON para clientes
de la API. Para cargar los productos de demostración:

```bash
docker compose exec web python manage.py seed_demo
```

Pruebas (requieren que el MySQL definido en `.env` esté disponible y permita crear
la base de datos temporal de Django):

```bash
docker compose exec web python manage.py test
```

Para detener la aplicación y Nginx (sin borrar datos de RDS):

```bash
docker compose down
```

## Despliegue en AWS Academy EC2

1. Crea una instancia RDS for MySQL y una base llamada `djangodocker` (o el nombre
   que indiques en `SQL_DATABASE`).
2. Configura el security group de RDS para permitir TCP `3306` desde el security
   group de EC2. No expongas la base de datos a `0.0.0.0/0`.
3. En la EC2 instala Docker, Git y Compose. Si ya tienes el proyecto del
   tutorial anterior clonado y configurado en esa instancia, actualiza ese mismo
   directorio para conservar su `.env` local:

   ```bash
   cd ~/tienda-api
   git pull origin main
   ```

   Si todavía no has clonado el proyecto en EC2, clónalo:

   ```bash
   git clone https://github.com/JoanP-B/tienda-api_tutorial05.git
   cd tienda-api_tutorial05
   ```

4. `.env` no se publica en GitHub porque contiene credenciales. En el directorio
   del proyecto debe existir el `.env` que apunta a tu RDS. Si ya estaba en el
   directorio clonado del tutorial anterior, `git pull` lo conserva y no necesitas
   cambiarlo. Si acabas de clonar en un directorio nuevo, copia/configura ese
   archivo usando tus credenciales existentes; no subas `.env` a GitHub. Nginx y
   Gunicorn no requieren cambios en ese archivo.
5. Permite HTTP (TCP `80`) en el security group de EC2 desde los clientes que
   deban acceder a la API. No abras el puerto `8000`: Django queda aislado detrás
   del proxy.
6. Construye y levanta la aplicación y el proxy:

   ```bash
   docker compose up --build -d
   docker compose ps
   docker compose logs --tail=100 web
   docker compose logs --tail=100 nginx
   docker compose exec web python manage.py seed_demo
   ```

En una actualización de una instalación existente, ejecuta `git pull` antes del
comando de despliegue. Verifica que los contenedores `web` y `nginx` estén activos
(MySQL/RDS continúa siendo un servicio administrado aparte). Abre
`http://IP_PUBLICA_EC2/` o
`http://IP_PUBLICA_EC2/api/v1/comprar/` para abrir la tienda. Los clientes de
API que soliciten JSON siguen recibiendo el catálogo JSON en la segunda ruta.
En ambas direcciones, omite `:8000`. Como comprobación de aislamiento,
`http://IP_PUBLICA_EC2:8000/` no debe responder.

## Variables de entorno esperadas

`DEBUG`, `SECRET_KEY`, `DJANGO_ALLOWED_HOSTS`, `SQL_ENGINE`, `SQL_DATABASE`,
`SQL_USER`, `SQL_PASSWORD`, `SQL_HOST` y `SQL_PORT`.
