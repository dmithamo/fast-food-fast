import puppeteer from "puppeteer";

/* 
    - Module tests that pages are rendered properly, 
        with elements rendered as expected.
*/

// Homepage
describe('/menu - Homepage', () => {
  beforeAll(async () => {
    await page.goto('http://127.0.0.1:5000/')
  });

  it('should display a banner on the Homepage', async () => {
    await expect(page).toMatch('Too hungry to go');
  });

  it('should show Login and Register links', async () => {
      const linksOnPage = await page.evaluate(() => {
          let loginLink = document.querySelector("#login-link").innerHTML;
          let registerLink = document.querySelector("#register-link").innerHTML;

          return [loginLink, registerLink];
      })

      expect(linksOnPage[0]).toBe("Login")
      expect(linksOnPage[1]).toBe("Register")
      
  })

  it('should render the menuUL on the Homepage', async () => {
      const menuList = await page.evaluate(() => {
          let list = document.querySelector("#food-items");
          return list.nodeName;
      })
      expect(menuList).toBe("UL");
  })


  it('should render the footer', async () => {
      const footerExists = await page.evaluate(() => {
          let footer = document.querySelector("footer");
          let footerVanityTag = footer.querySelector("p.designer-link>a").innerHTML;
          return [footer, footerVanityTag];
      })

      expect(footerExists[0]).toBeDefined();
      expect(footerExists[1]).toMatch("dmithamo");
  });

});

// Login page
describe('/auth/login - Login page', () => {
    // Visit login page first
    beforeAll(async () => {
    await page.goto('http://127.0.0.1:5000/auth/login');
    });

    it('should display `Login` atop the Login form', async () => {
    await expect(page).toMatch('Login');
    });

    it('should render the Login form on the Login page', async () => {
        
        //   Check that an input for email and password is displayed
        const loginForm = await page.evaluate(() => {
            let form = document.querySelector("form");
            let emailInput = document.querySelector("#login-email-input").placeholder;
            let passwordInput = document.querySelector("#login-password-input").placeholder;
            let loginBtn = document.querySelector("#login-btn");
            
            return [form, emailInput, passwordInput, loginBtn];
        })

        expect(loginForm[0]).toBeDefined();
        expect(loginForm[1]).toMatch("Enter your email");
        expect(loginForm[2]).toMatch("Enter your password");
        expect(loginForm[3]).toBeDefined();
  })

  
  it('should autofocus onto the email input', async () => {
      const checkFocus = await page.evaluate(() => {
        let emailInput = document.querySelector("#login-email-input");

        return document.activeElement === emailInput;
      })

      expect(checkFocus).toBe(true);
  });
      

});

// Register page
describe('/auth/signup - Signup page', () => {
    // Visit register page first
    beforeAll(async () => {
        await page.goto('http://127.0.0.1:5000/auth/register')
    });

    it('should display `Create an Account` atop the Sign up form', async () => {
        await expect(page).toMatch('Create an Account');
    });

    it('should render the Register form on the Register page', async () => {
        
        const registerForm = await page.evaluate(() => {
            let form = document.querySelector("form");
            let usernameInput = document.querySelector("#register-username-input").placeholder;
            let emailInput = document.querySelector("#register-email-input").placeholder;
            let passwordInput = document.querySelector("#register-password-input").placeholder;
            let confirmPasswordInput = document.querySelector("#confirm-password-input").placeholder;
            let registerBtn = document.querySelector("#register-btn");
            
            return [form, usernameInput, emailInput, passwordInput, confirmPasswordInput, registerBtn];
        })

        expect(registerForm[0]).toBeDefined();
        expect(registerForm[1]).toMatch("Enter a username");
        expect(registerForm[2]).toBe("Enter an email address");
        expect(registerForm[3]).toBe("Enter a strong password");
        expect(registerForm[4]).toBe("Reenter the password");
        expect(registerForm[5]).toBeDefined();
  })

});


// Admin edit menu page
describe('/adm_menu - Admin menu editing page', () => {
    // Visit admin menu page
    beforeAll(async () => {
        await page.goto('http://127.0.0.1:5000/adm_menu')
    });

    // When admin is not logged in    
    it('should display links to the login page and to the Homepage', async () => {
        const redirects = await page.evaluate(() => {
            let loginRedirect = document.querySelectorAll("section a")[0].innerHTML;
            let homepageRedirect = document.querySelectorAll("section a")[1].innerHTML;

            let adminPortalIndicator = document.querySelector("nav p").innerHTML;

            return [loginRedirect, homepageRedirect, adminPortalIndicator]
        })
        
        expect(redirects[0]).toBe("login as admin here.");
        expect(redirects[1]).toBe("Homepage");
        expect(redirects[2]).toBe("[ Admin Portal ]");
            
    });
        
});


// User view orders page
describe('/users/view_orders - User view order history page', () => {
    // Visit user order history page
    beforeAll(async () => {
        await page.goto('http://127.0.0.1:5000/users/view_orders')
    }, 5000);

    // When user is not logged in    
    it('should display links to the login and register pages', async () => {
        const redirects = await page.evaluate(() => {
            let loginRedirect = document.querySelectorAll("section a")[0].innerHTML;
            let registerRedirect = document.querySelectorAll("section a")[1].innerHTML;

            return [loginRedirect, registerRedirect]
        })
        
        expect(redirects[0]).toBe("login");
        expect(redirects[1]).toBe("register");
            
    });
        
});