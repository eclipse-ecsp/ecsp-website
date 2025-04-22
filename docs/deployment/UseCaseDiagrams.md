
# Use Case Diagrams

## Sign Up

![Sign up Flow](images/sign-up.png)  

**Precondition** - Connect app is installed in mobile.  

- User clicks on signup button on mobile application which launches UIDAM signup page (webpage in application window)
- This is a public signup page (/SignUp) with captcha to prevent bots creating the user.
- Backend will take user details like email-id(username), first name, last name and password, validates password against password policies and creates user.
- Sends email verification link to the email-id(username) entered by user in signup page.
- On successful verification by clicking the link provided in the verification email, user will be able to login to mobile app.

## Sign In

![Sign in Flow](images/sign-in.png)  

**Precondition** - Connect app is installed in mobile and Signup process is complete.  

- User clicks on sign-in(Login: /oauth2/authorize) button on mobile application which launches UIDAM sign-in page (webpage in application window)
- This page will be landed from mobile app using oAuth grant type: Authorisation code (PKCE) flow.
- This is a public signup page (/SignUp) with captcha to prevent bots creating the user
captcha is configurable, either always or after certain number of failure attempts or specific to user.
- Post successful login, user should be able to get auth code sent to mobile apps redirect uri provided in login page link.
- Mobile app will generate access token(/oauth2/token) using the authorisation code received from UIDAM authorisation server.
- This token will be used for further api access.

## Forgot Password

![Forgot Password Flow](images/forgot-password.png)  

**Precondition** - Connect app is installed in mobile and Signup process is complete.  

- User clicks on sign-in(Login: /oauth2/authorize) button on mobile application which launches UIDAM sign-in page (webpage in application window)
- User clicks on forgot password option in public page.
- Public webpage will show option to enter username and challenge captcha to prevent bots anonymous access.
- On successful user identification, backend will send verification link to registered email-id
- On clicking link, backend will validate the token in link and if it is valid, Public web page will be opened.
- User will be able to create new password, backend validates password against password policies
- Confirmation page will be shown to user once password is changed.
- User will be able to login with new password.

## Change Password

![Change Password Flow](images/change-password.png)  

**Precondition** - Connect app is installed in mobile, user signed in to mobile application.

- User clicks on change password option in mobile app(the request will go to the backend with the user token),
- Backend will verify and extract the userid from the token, will send verification link to registered email-id
- On clicking link, backend will validate the token in link and if it is valid, Public web page will be opened.
- User will be able to create new password, backend validates password against password policies
- Confirmation page will be shown to user once password is changed.
- User will be able to login with new password.
