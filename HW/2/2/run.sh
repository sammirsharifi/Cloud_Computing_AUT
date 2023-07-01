set -x

BASEDIR="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
REDIS_CONTAINER_NAME="node-redis"
SERVER_CONTAINER_NAME="node-url-shortener"

cd "${BASEDIR}"/redis || exit
docker build . -t sam/redis

cd "${BASEDIR}"/server || exit
docker build . -t sammirsharifi/node-url-shortener

if ! (docker network ls | grep node-url-shortener); then
  docker network create --subnet=172.20.0.0/16 node-url-shortener
fi

if (docker container ls -a -f NAME="$SERVER_CONTAINER_NAME" | grep "$SERVER_CONTAINER_NAME"); then
  docker container stop "$SERVER_CONTAINER_NAME"
  docker container rm "$SERVER_CONTAINER_NAME"
fi

if (docker container ls -a -f NAME="$REDIS_CONTAINER_NAME" | grep "$REDIS_CONTAINER_NAME"); then
  docker container stop "$REDIS_CONTAINER_NAME"
  docker container rm "$REDIS_CONTAINER_NAME"
fi

docker run -it --name "$REDIS_CONTAINER_NAME" --net node-url-shortener --ip 172.20.0.2 \
  -v "${BASEDIR}"/redis/data:/data -d sam/redis
docker run -it --name "$SERVER_CONTAINER_NAME" --net node-url-shortener --ip 172.20.0.3 \
  -d -p 3000:80 sammirsharifi/node-url-shortener
