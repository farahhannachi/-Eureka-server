# Atelier Eureka : Service Discovery avec Spring Cloud Netflix Eureka

Projet réalisé dans le cadre du module AWD (ESPRIT).

## Équipe

| Nom et prénom | Microservice |
|---|---|
| Farah Hannachi | à compléter |


## Architecture

Un serveur Eureka centralise l'enregistrement et la découverte des microservices, développés avec des technologies différentes.

| Service | Technologie | Port(s) |
|---|---|---|
| eureka-server | Spring Boot / Spring Cloud Netflix Eureka | 8761 |
| candidat | Spring Boot | 8081, 8091 |
| job | Spring Boot (MySQL) | 8082 |
| canditature | Spring Boot | 8085, 8092 |
| meeting | Node.js / Express | 8083, 8093 |
| notification | Python / FastAPI | à compléter (2 instances) |

## Dashboard Eureka

Capture du dashboard (`http://localhost:8761`) avec les services CANDIDAT, JOB, MEETING et NOTIFICATION enregistrés, ainsi que leurs instances :

![Dashboard Eureka](docs/eureka-dashboard.png)

## Configuration des clients Eureka

### Services Spring Boot (candidat, job, canditature)

Dépendances : `spring-cloud-starter-netflix-eureka-client` et `spring-boot-starter-actuator`.

```properties
eureka.client.service-url.defaultZone=http://localhost:8761/eureka
eureka.client.register-with-eureka=true
eureka.client.fetch-registry=true
eureka.instance.prefer-ip-address=true
eureka.instance.instance-id=${spring.application.name}:${server.port}
```

La classe principale est annotée avec `@EnableDiscoveryClient`.

### Meeting (Node.js)

Enregistrement via `eureka-js-client` (voir `meeting/src/config/eureka.js`). Le port se règle avec la variable `PORT`.

### Notification (Python)

Enregistrement via `py-eureka-client` (voir `notification/app/main.py`). Le port se règle au lancement d'`uvicorn`.

## Lancement

1. Démarrer le serveur Eureka (`eureka-server`) et vérifier `http://localhost:8761`.
2. Démarrer MySQL (pour `job`), puis les services Spring Boot.
3. Lancer plusieurs instances d'un même service avec des ports différents :

```bash
# Spring Boot
java -jar target/candidat.jar --server.port=8091

# Meeting (Node.js)
PORT=8083 npm start
PORT=8093 npm start

# Notification (Python)
uvicorn app.main:app --port 8084
uvicorn app.main:app --port 8094
```
## Dashboard Eureka
Sous Windows PowerShell, utiliser `$env:PORT=8093; npm start`.

## Vérification

- Dashboard : `http://localhost:8761`, rubrique « Instances currently registered with Eureka ».
- Chaque service doit apparaître en statut `UP`, avec au moins deux instances pour MEETING ou NOTIFICATION.
