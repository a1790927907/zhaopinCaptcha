import { Page, Protocol } from "puppeteer";
import { delay } from "../utils";

interface ZhaoPinCompanyPageInfo {
    content: string
    cookies: Protocol.Network.Cookie[]
    url: string
}

const extractZhaoPinCompanyPageInfo = async (page: Page): Promise<ZhaoPinCompanyPageInfo> => {
    await page.waitForSelector(".mian-company", {
        timeout: 5000
    })
    await delay(500)
    const content: string = await page.content()
    const cookies: Protocol.Network.Cookie[] = await page.cookies()
    return { content, cookies, url: page.url() }
}

export default extractZhaoPinCompanyPageInfo
