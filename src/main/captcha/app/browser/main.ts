import { Browser } from "puppeteer"
import puppeteer from "puppeteer"


const getBrowser = async (): Promise<Browser> => {
    const launchMethod: string = process.env.launchMethod || "local"
    const browser: Browser = launchMethod === "local" ? await puppeteer.launch({
        headless: false,
        defaultViewport: null,
        ignoreDefaultArgs: ["--enable-automation"],
        args: [
            `--disable-features=site-per-process`,
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--start-maximized'
        ],
        executablePath: process.env.executablePath || "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    }) : await puppeteer.connect({
        browserWSEndpoint: process.env.browserWSEndpoint || "ws://localhost:9800/?--disk-cache-dir=null"
    })
    return browser
}

export default getBrowser
