#!/bin/bash

deploy_hard(){
	echo "Hard Deploy Selected"
	python manage.py collectstatic
 	python manage.py flush --no-input
	python manage.py migrate
	python manage.py loaddata users.json
	uwsgi --ini uwsgi.ini --py-autoreload 1
}


deploy_soft(){
	echo "Soft deploy Selected"
	python manage.py migrate

	uwsgi --ini uwsgi.ini --py-autoreload 1
}


case "${DEPLOY_LEVEL}" in
        hard) deploy_hard ;;
        soft) deploy_soft ;;
	        *) deploy_soft ;;
	esac


	echo "Deploying..."
