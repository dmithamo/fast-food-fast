import puppeteer from "puppeteer";

const APP_URL = "http://127.0.0.1:5000/";

let page;
let browser;
const width = 1920;
const height = 1080;

beforeAll(async () => {
    browser = await puppeteer.launch({
        headless: false,
        slowMo : 80,
        args: [`--window-size=${width}, ${height}`]

    });
    page = await browser.newPage();
    await page.setViewport({width, height});
});

afterAll(() => {
    browser.close();
});


describe('Fetch Menu module', function() {
    test("loads the menu page", async () => {
        await page.goto(APP_URL);
        await page.waitForSelector("p");
    })
});
    