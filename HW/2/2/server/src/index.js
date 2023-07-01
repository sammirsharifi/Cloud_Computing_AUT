if (!process.env.API_KEY)
  require('dotenv').config()

const os = require('os')
const express = require('express')
const superagent = require('superagent')
const config = require('config')
const audit = require('express-requests-logger')
const redis = require('./redis')

const { SERVER_SERVICE_PORT: PORT = 3000 } = process.env

const app = express()

app.use(express.json())
app.use(audit())

app.post('/', async (req, res) => {
	const { url } = req.body
	const shortUrl = redis.connected
		? await withTimeout(2000, redis.client.get(url))
			.catch(e => { console.log(e); redis.connected = false })
		: undefined
	if (shortUrl) {
		return res.json({
			long_url: url,
			short_url: shortUrl,
			is_cached: true,
			hostname: os.hostname()
		})
	}
	const shortenerResult = await superagent
		.post(config.api.url)
		.send(url)
		.set({ apikey: process.env.API_KEY })
		.catch((e) => console.log(e?.response?.body || e))
	const body = shortenerResult?.body
	if (!body) {
		res.status(503).json({ error: 'got invalid response from service' })
		return
	}
	if (redis.connected)
		await withTimeout(2000, redis.client.set(url, body.short_url, { EX: config.redis?.EX || 60 }))
			.catch(e => { console.log(e); redis.connected = false })
	res.json({
		...shortenerResult.body,
		is_cached: false,
		hash: undefined,
		hostname: os.hostname()
	})
})

app.listen(PORT, () => {
	console.log(`Server listening on port ${PORT}`)
})

async function withTimeout(millis, promise) {
	const timeout =
		new Promise((resolve, reject) =>
			setTimeout(() => reject(`Timeout after ${millis}`), millis))
	return Promise.race([
		promise,
		timeout
	])
}
