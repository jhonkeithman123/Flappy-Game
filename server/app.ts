import express from 'express'
import type { Express, Request, Response } from 'express'
import cors from 'cors'

const app: Express = express()

app.use(cors())
app.use(express.json())

app.get('/', (req: Request, res: Response) => {
  res.send('Hi')
})

const port = 5000
app.listen(port, () => {
  console.log(`Server is listening in port ${port}`)
})
