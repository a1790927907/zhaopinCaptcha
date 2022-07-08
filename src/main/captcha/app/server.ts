import express from "express"
import { getNow } from "./utils"
import ZhaoPinCompanyExtractor from "./main"

const app = express()
const port: number = 9000

interface ZhaoPinCompanyRequestBody {
    url: string
}

const extractor = new ZhaoPinCompanyExtractor()

app.use(express.json())
app.use(express.urlencoded({extended: true}))
console.log(process.env)

app.post('/api/zhaopin/company/info', async function (req: express.Request, res: express.Response) {
    const body: ZhaoPinCompanyRequestBody = req.body
    console.log("收到 request body: ", body)
    try {
        const response = await extractor.getZhaoPinCompanyPageInfo(body.url)
        console.log(`- ${getNow()} status: ${200}, url: ${req.url}, method: ${req.method}`)
        res.status(200).json({ result: response, message: "ok" })
    } catch (error: any) {
        console.error(error)
        console.error(`- ${getNow()} status: ${500}, url: ${req.url}, method: ${req.method}`)
        res.status(500).json({ message: error.message, result: null })
    }
})

app.listen(9000, () => {
    console.log("listen port on ", port)
})
