echo "RUNNING SERVER"

echo "WAITING FOR MYSQL"

until mysqladmin ping -h db -u root -p$MYSQL_ROOT_PASSWORD --silent --skip-ssl; do
    sleep 2
done

echo "MIGRATING"

# python pylink/manage.py makemigrations
# python pylink/manage.py migrate

# python pylink/manage.py runserver 0:8000

python pylink/manage.py collectstatic --noinput

cd pylink

gunicorn pylink.wsgi:application --bind 0:8000