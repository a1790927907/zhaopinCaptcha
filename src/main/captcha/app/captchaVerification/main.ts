import { delay } from "../utils"
import { PendingXHR } from "pending-xhr-puppeteer"
import { BoundingBox, ElementHandle, Page } from "puppeteer"

const verify = async (page: Page) => {
    const pendingXhr = new PendingXHR(page)
    const captchaButton = await page.waitForSelector("#nc_1_n1z", {
        timeout: 5000
    })
    const slideBar = await page.waitForSelector("#nc_1__scale_text", {
        timeout: 5000
    })
    const slideBarBoundingBox = await (slideBar as ElementHandle).boundingBox()
    const captchaButtonBoundingBox = await (captchaButton as ElementHandle).boundingBox()
    await page.mouse.move((captchaButtonBoundingBox as BoundingBox).x, (captchaButtonBoundingBox as BoundingBox).y)
    await delay(1000)
    await page.mouse.down()
    await page.mouse.move((captchaButtonBoundingBox as BoundingBox).x + (slideBarBoundingBox as BoundingBox).width + 10, (captchaButtonBoundingBox as BoundingBox).y, {
        steps: 100
    })
    await delay(1000)
    await pendingXhr.waitForAllXhrFinished()
}

export default verify
