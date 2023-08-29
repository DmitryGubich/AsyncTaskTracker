## AsyncTaskTracker

#### Demo project to try async communication between microservices.

**Technology stack:**
Each project is a separate Django application. All of them use Postgres as a database, but every application uses using corresponding database schema.

Useful links:
* [Initial diagram](https://miro.com/app/board/uXjVMw_TyiA=/?share_link_id=795541479315)
* [Event storming, Data model, Services and Event schemas](https://miro.com/app/board/uXjVMwrO9Fc=/?share_link_id=611585265044)
* [Schema registry repository](https://github.com/DmitryGubich/AsyncTaskTrackerSchemas)

## How to run the project
Run this command in the console 
```
docker-compose up
```

### TODO:
* Implement celery logic with redis
* Refactor code (move events logic)
* Ideally rewrite using FastAPI