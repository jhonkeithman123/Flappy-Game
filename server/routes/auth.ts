import express from 'express'
import type { Router, Request, Response } from 'express'
import dotenv from 'dotenv'
import path from 'path'
import { supabase } from '../config/db'

dotenv.config()
const router: Router = express.Router()

router.get('/', (req: Request, res: Response) => {
  console.log('Accessed the default route')
  console.log(`NODE_ENV: ${process.env.NODE_ENV}`)

  if (process.env.NODE_ENV === 'production') {
    res.sendFile(path.join(import.meta.dir, '../public/index.html'))
  } else {
    res.json({ message: 'Dev server - API only' })
  }
})

router.post('/login', (req: Request, res: Response) => {
  const { identifier, password } = req.body
  console.log(
    `These are the data in the req.body\n
     identifier: ${identifier}\n
     password: ${password}`
  )

  if (!identifier || !password) {
    return res.status(400).json({ error: 'Missing [username/email], password' })
  }

  console.log(`Login attempt - identifier: ${identifier}`)
  res.json({ message: 'Login successful', username: identifier })
})

router.post('/signup', (req: Request, res: Response) => {
  const { username, email, password } = req.body
  console.log(
    `These are the data in the req.body\n
     username: ${username}
     email: ${email}
     password: ${password}`
  )

  if (!username || !email || !password) {
    return res.status(400).json({ error: 'Missing required fields' })
  }

  console.log(`Signup attempt - username: ${username}, email: ${email}`)
  res.json({ message: 'Signup successful', username })
})

export default router
