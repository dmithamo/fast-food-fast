/* 
    - Module tests the logic that logs in a user into the app
*/

// Login page
describe('/auth/login - Login page functionality', () => {
    // Visit login page first
    beforeAll(async () => {
        await page.goto('http://127.0.0.1:5000/auth/login', {waitUntil: 'domcontentloaded'});
    });

    it('should show an error if user does not exist', async () => {
        await page.type('#login-email-input', 'dmithamo');
        await page.type('#login-password-input', 'dmithamo');
        await page.click('#login-btn');

        await page.waitForSelector('.resp-message');

        const resp = await page.$eval('.resp-message', message => (
            message.innerHTML
        ));

        expect(resp).toBe("User not found.");
            
    })
});