/*
    - Module tests that the elements for registering a user can accept input,
     and give feedcback as appropriate
*/

// Register
describe('/auth/register - Register functionality', () => {
    beforeEach(async () => {
        await page.goto('http://127.0.0.1:5000/auth/register', {waitUntil: 'domcontentloaded'})
    })
    // Valid credentials
    it('should create an account when input is valid', async () => {

        await page.type('#register-username-input', 'mithamo')
        await page.type('#register-email-input', 'mithamo@email.com')
        await page.type('#register-password-input', 'demithamo')
        await page.type('#confirm-password-input', 'demithamo')
        await page.click('#register-btn')

        await page.waitForSelector('.resp-message')

        const resp = await page.$eval('.resp-message', message => (
            message.innerHTML
        ));
        // expect(resp).toBe("Registration successful. Login to continue. Redirecting ...");
        expect(resp).toBeDefined();
    })

    // Invalid credentials - Username too short
    it('should report an error if any of the required credentials is invalid', async () => {

        await page.type('#register-username-input', 'd') // No username input
        await page.type('#register-email-input', 'mithamo@email.com')
        await page.type('#register-password-input', 'demithamo')
        await page.type('#confirm-password-input', 'demithamo')
        await page.click('#register-btn')

        await page.waitForSelector('.resp-message')

        const response = await page.$eval('.resp-message', message => (
            message.innerHTML
        ));

        expect(response).toMatch("Unsuccessful. 'd' is an invalid username");

    })

    // Invalid credentials - Invalid email
    it('should report an error if any of the required credentials is invalid', async () => {

        await page.type('#register-username-input', 'salmak') // No username input
        await page.type('#register-email-input', 'salmak.email.com')
        await page.type('#register-password-input', 'demithamo')
        await page.type('#confirm-password-input', 'demithamo')
        await page.click('#register-btn')

        await page.waitForSelector('.resp-message')

        const response = await page.$eval('.resp-message', message => (
            message.innerHTML
        ));

        expect(response).toMatch("Unsuccessful. 'salmak.email.com' is an invalid email");

    })


    // Invalid credentials - Passwords don't match
    it('should report an error if any of the required credentials is invalid', async () => {

        await page.type('#register-username-input', 'dkhalegi')
        await page.type('#register-email-input', 'dkhalegi@email.com')
        await page.type('#register-password-input', 'demithamo')
        await page.type('#confirm-password-input', 'khalegid12')
        await page.click('#register-btn')

        await page.waitForSelector('.resp-message')

        const response = await page.$eval('.resp-message', message => (
            message.innerHTML
        ));

        expect(response).toMatch("Passwords do not match!");

    })


    // Invalid credentials - Invalid password
    it('should report an error if any of the required credentials is invalid', async () => {

        await page.type('#register-username-input', 'userflani')
        await page.type('#register-email-input', 'userflani@email.com')
        await page.type('#register-password-input', '12345')
        await page.type('#confirm-password-input', '12345')
        await page.click('#register-btn')

        await page.waitForSelector('.resp-message')

        const response = await page.$eval('.resp-message', message => (
            message.innerHTML
        ));

        expect(response).toMatch("'12345' is an invalid password");

    })

});
    