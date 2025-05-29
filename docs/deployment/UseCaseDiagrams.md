---
hide:
    - toc
---

# Use Case Diagrams

=== "User Management"

    ## Sign up Flow

    ![Sign up Flow](images/sign-up.svg)

    **Precondition** - Connect app is installed in mobile.

    - User clicks on signup button on mobile application which launches UIDAM signup page (webpage in application window)
    - This is a public signup page (/SignUp) with captcha to prevent bots creating the user.
    - Backend will take user details like email-id(username), first name, last name and password, validates password against password policies and creates user.
    - Sends email verification link to the email-id(username) entered by user in signup page.
    - On successful verification by clicking the link provided in the verification email, user will be able to login to mobile app.

    ## Sign in Flow

    ![Sign in Flow](images/sign-in.svg)

    **Precondition** - Connect app is installed in mobile and Signup process is complete.  

    - User clicks on sign-in(Login: /oauth2/authorize) button on mobile application which launches UIDAM sign-in page (webpage in application window)
    - This page will be landed from mobile app using oAuth grant type: Authorisation code (PKCE) flow.
    - This is a public signup page (/SignUp) with captcha to prevent bots creating the user
    captcha is configurable, either always or after certain number of failure attempts or specific to user.
    - Post successful login, user should be able to get auth code sent to mobile apps redirect uri provided in login page link.
    - Mobile app will generate access token(/oauth2/token) using the authorisation code received from UIDAM authorisation server.
    - This token will be used for further api access.

    ## Forgot Password Flow

    ![Forgot Password Flow](images/forgot-password.svg)

    **Precondition** - Connect app is installed in mobile and Signup process is complete.  

    - User clicks on sign-in(Login: /oauth2/authorize) button on mobile application which launches UIDAM sign-in page (webpage in application window)
    - User clicks on forgot password option in public page.
    - Public webpage will show option to enter username and challenge captcha to prevent bots anonymous access.
    - On successful user identification, backend will send verification link to registered email-id
    - On clicking link, backend will validate the token in link and if it is valid, Public web page will be opened.
    - User will be able to create new password, backend validates password against password policies
    - Confirmation page will be shown to user once password is changed.
    - User will be able to login with new password.

    ## Change Password Flow

    ![Change Password Flow](images/change-password.svg)

    **Precondition** - Connect app is installed in mobile, user signed in to mobile application.

    - User clicks on change password option in mobile app(the request will go to the backend with the user token),
    - Backend will verify and extract the userid from the token, will send verification link to registered email-id
    - On clicking link, backend will validate the token in link and if it is valid, Public web page will be opened.
    - User will be able to create new password, backend validates password against password policies
    - Confirmation page will be shown to user once password is changed.
    - User will be able to login with new password.

=== "Device Management"

    ## Create Device/Vehicle Flow

    ![Create Device/Vehicle Flow](images/create-device.svg)

    **Precondition** - Device/Vehicle details are available and valid

    - Device/Vehicle Creation will be done by admin (OEM) by calling backend api
    - Admin gets oauth token with admin scope from auth server
    - Admin calls backend API Gateway to create a vehicle with necessary vehicle details (eg: serial number, IMEI etc)
    - API Gateway forwards the requests to Device factory management service which creates the vehicle.
    - Initial state when vehicle created would be, Device State: PROVISIONED and Association Status: NOT ASSOCIATED
    - When vehicle is created, it is considered on-boarded and whitelisted.

    ## Associate Device/Vehicle With User Flow

    ![Create Device/Vehicle Flow](images/device-association.svg)
    
    **Pre Condition** - User is created and logged in to mobile application.(mobile app will have oauth token of user logged in)  

    - Vehicle association can be done by user as well as admin.
    - User will use mobile application to associate vehicle.  
    - User enters serial number of vehicle in to mobile application for which association is required
    - Mobile application calls associate backend API with vehicle details and appropriate scope(oauth token)
    - Device-association backend service checks for the vehicle serial number in database and identifies whether it is onboarded/whitelisted or not
    - Backend service invokes association process with the whitelisted vehicle details from DB and User details from token
    - On successful initiation of association, user will see success response (association initiated successfully) on mobile app
    - Post successful association initiation, at backend, Device State would be READY_TO_ACTIVATE, Association Status would be ASSOCIATION_INITIATED

    ## Activate Device/Vehicle Flow

    ![Create Device/Vehicle Flow](images/activate-device.svg)
    
    **Pre Condition** - User and Vehicle association is successfully initiated by user on mobile application.
 
    - User starts the vehicle
    - When user turns ignition on, vehicle (device client present in vehicle) calls activate api of backend.
    - Device activation backend service will check if Device State is READY_TO_ACTIVATE and Association Status is ASSOCIATION_INITIATED and then activates the vehicle.
    - On Successful activation, at backend, Device State would be ACTIVATED and Association Status would be ASSOCIATED  

=== "Remote Operations"

    ## Remote Operation Overall Flow

    ![Remote Operations Response Flow](images/ro-overall-flow.svg)

    **Pre Condition** - User is logged in to mobile app, vehicle is activated and is provisioned for remote operations.

    - User clicks on the desired Remote Operation in mobile app.
    - Mobile application calls the corresponding backend api on API Gateway for remote operation.
    - API Gateway checks whether vehicle has service provisioned for remote operations.
    - RO Service backend checks the current DB state for requested remote operation and verifies if the request is valid or not.
    - RO Service, for a valid remote operation request forwards the request to the vehicle through MQTT Channel.
    - Vehicle sends the response to RO Service through MQTT Channel.
    - RO Service sends the vehicle response to Notification Service.
    - Notification Service then forwards the PUSH notification to the mobile app for intimation of Remote Operation status to user. 
    - Mobile app displays the Remote Operation Completed.

    **Note**: PUSH notifications for Remote Operation response is currently not supported and will be enabled in subsequent releases.

    ## Remote Operation Request Flow

    ![Remote Operations Response Flow](images/ro-request-flow.svg)

    **Pre Condition** - User is logged in to mobile app, vehicle is activated and is provisioned for remote operations.

    - User clicks on the desired Remote Operation in mobile app.
    - Mobile application calls the corresponding backend api on API Gateway for remote operation.
    - API Gateway validates parameters and checks if the request is valid.
    - API Gateway forwards the remote operation request to RO API.
    - RO API Service backend checks the current DB state for requested remote operation and verifies if the request is valid or not.
    - For valid request, RO API Service sends the Accepted response back to API Gateway and also forwards the RO event to RO stream processor.
    - RO stream processor checks if the vehicle is connected, and forwards the RO event to MQTT Broker.
    - MQTT Broker send RO event to vehicle.

    ## Remote Operations Response Flow

    ![Remote Operations Response Flow](images/remote-operation-response.svg)

    **Pre Condition** - User is logged in to mobile app, vehicle is activated and is provisioned for remote operations and has received the RO command.
    
    -  Remote operations like Door opened, door closed etc. are executed successfully in the vehicle and vehicle sends RO Response to RO service via MQTT Channel.
    - Remote Operation service receives remote operation response then validates if the vehicle is active with user and sends notification to the app.
    - Notification Center service receives RO response event and then it triggers PUSH notificaiton to the mobile app.
    - Finally Mobile app receives notification about the remote operation response.

    **Note**: PUSH notifications for Remote Operation response is currently not supported and will be enabled in subsequent releases.

    ## Remote Operations Error Flow

    ### Vehicle Not Provisioned

    ![Remote Operations Response Flow](images/vehicle-error.svg)

    **Pre Condition** - User is logged in to mobile app and vehicle is activated.

    - User clicks on the desired Remote Operation in mobile app.
    - Mobile application calls the corresponding backend api on RO Service for remote operation.
    - Vehicle is Not Provisioned for Remote Operations.
    - Sends Vehicle Not Provisioned response to mobile app.
    - Mobile app displays that Vehicle Not Provisioned.

    ### RO Service Down

    ![Remote Operations Response Flow](images/service-down.svg)

    **Pre Condition** - User is logged in to mobile app, vehicle is activated and is provisioned for remote operations.

    - User clicks on the desired Remote Operation in mobile app.
    - Mobile application calls the corresponding backend api on RO Service for remote operation.
    - Backend RO Service is down.
    - Mobile app displays that RO Service is down.

    ### Vehicle Not Connected

    ![Remote Operations Response Flow](images/vehicle-not-connected.svg)

    **Pre Condition** - User is logged in to mobile app, vehicle is activated and is provisioned for remote operations.

    - User clicks on the desired Remote Operation in mobile app.
    - Mobile application calls the corresponding backend api on API Gateway for remote operation.
    - API Gateway validate parameters and check if request is valid.
    - API Gateway forwards the remote operation request to RO API.
    - RO API checks the current DB state for requested remote operation and verifies if the request is valid or not.
    - For valid request, RO API forwards the RO Event to RO stream processor.
    - RO stream processor checks if the vehicle is connected.
    - The vehicle is not connected, RO stream processor will retry multiple times to check if vehicle is connected.
    - When retry limit is exceeded RO stream processor sends vehicle status as not connected to Notification Service. 
    - Notification Service sends PUSH notification to mobile app.
    - Mobile app displays that vehicle is not connected.
