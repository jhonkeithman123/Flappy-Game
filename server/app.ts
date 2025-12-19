import express from 'express'
import type { Express } from 'express'
import cors from 'cors'
import dotenv from 'dotenv'

import main from './routes/auth'

//* Express App
const app: Express = express()
dotenv.config()
const __dirname = import.meta.dir

//* Middlewares
app.use(cors())
app.use(express.json())

app.use(express.static(__dirname + '/public'))

//* Routes
app.use('/', main)

const port = 5000
app.listen(port, () => {
  console.log(`Server is listening in port ${port}`)
  console.log(`Running in http://localhost:${port}`)
})
