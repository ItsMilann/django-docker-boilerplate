# backend template

## Build image
---
Use docker build command to build a image of django project

```bash
sudo docker build -t project/backend:0.0.1 project
```

## Usage
---
```
sudo docker-compose up -d
```

<hr/>

## <b>Change Log </b>

### v1.0.1 <hr/>

 - python version update
 - nginx-proxy.conf file added by default
 - docker-compose.yml added by default (instead of symblink) (to be removed later)

### v1.0.2 <hr>
- auto reload on enabled
- swagger documentation configured

### v1.0.3 <hr>
- method to create user & profile in one shot using form-data