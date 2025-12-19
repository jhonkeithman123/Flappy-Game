import express from 'express'
import type { Router, Request, Response } from 'express'

const router: Router = express.Router()

router.get('/', (req: Request, res: Response) => {
  console.log('Accessed the default route')
  res.sendFile('/index.html')
})

export default router
