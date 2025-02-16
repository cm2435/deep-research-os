# Lawrence Proactive Service

## Local development

```sh
# Start Inngest dev server
npx inngest-cli@latest dev -u http://localhost:8000/api/inngest --no-discovery

# Start service
uvicorn app:app --reload
```



## In docker 

nixpacks build . -t deep-research-app

 docker-compose up