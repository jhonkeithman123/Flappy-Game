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
  const { username, email, password } = req.body
  console.log(
    `These are the data in the req.body\n
     username: ${username}\n
     email: ${email}\n
     password: ${password}`
  )
  res.json({ message: 'Login recieved' })
})

router.post('/signup', (req: Request, res: Response) => {
  const { username, email, password } = req.body
  console.log(
    `These are the data in the req.body\n
     username: ${username}
     email: ${email}
     password: ${password}`
  )
  res.json({ message: 'Signup recieved' })
})

export default router
