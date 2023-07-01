const { createClient } = require('redis')

const {
  REDIS_SERVICE_HOST: host,
  REDIS_SERVICE_PORT: port,
  REDIS_PASSWORD: password,
} = process.env
const redisOptions = {
  url: `redis://:${password}@${host}:${port}`
}
const client = createClient(redisOptions)

client.on('error', () => {})
client.on('connect', (e) => {
  console.log('Redis connection established.')
  module.exports.connected = true
})

client.connect().catch(console.log)
Object.assign(module.exports, { client })
