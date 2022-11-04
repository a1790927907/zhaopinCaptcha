import { delay } from "./utils"
import { Browser, Page } from "puppeteer"
import getBrowser from "./browser/main"
import verify from "./captchaVerification/main"
import extractZhaoPinCompanyPageInfo from "./pageInfoExtractor/main"


class ZhaoPinCompanyExtractor {
    browser!: Browser

    getBrowser = async () => {
        if (!this.browser) {
            this.browser = await getBrowser()
        } else if (!this.browser.isConnected()) {
            this.browser = await getBrowser()
        }
        return this.browser
    }

    _getZhaoPinCompanyPageInfo = async (url: string, page: Page) => {
        await page.evaluateOnNewDocument(() => {
            // @ts-ignore: Unreachable code error
            Object.defineProperty((navigator as any), 'webdriver', {get: () => undefined})
        })
        await page.goto(url, { waitUntil: "networkidle0" })
        await delay(300)
        const [companySelector, jobSelector] = [".mian-company", ".job-summary"]
        const companyInfo = await page.$(companySelector)
        const jobInfo = await page.$(jobSelector)
        let selector: string
        if (!companyInfo && !jobInfo) {
            await verify(page)
            await delay(1000)
        }
        if (await page.$(companySelector)) {
            selector = companySelector
        } else if (await page.$(jobSelector)) {
            selector = jobSelector
        } else {
            throw new Error(`当前页面非公司也非职位, ${(!companySelector && !jobInfo) ? "已验证验证码" : "未验证验证码"}`)
        }
        return await extractZhaoPinCompanyPageInfo(page, selector)
    }

    getZhaoPinCompanyPageInfo = async (url: string) => {
        const browser = await this.getBrowser()
        const page: Page = await browser.newPage()
        try {
            return await this._getZhaoPinCompanyPageInfo(url, page)
        } catch (error: any) {
            throw error
        } finally {
            await page.close()
        }
    }
    
}

export default ZhaoPinCompanyExtractor
