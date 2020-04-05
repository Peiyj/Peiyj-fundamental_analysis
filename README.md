# Solemate README

## Table of Contents
1. [Overview](#Overview)
2. [Product Spec](#Product-Spec)
3. [Wireframes](#Digital-Wireframes)

## Overview
### Description
Solemate is a shoe insert that tracks foot pressures in order to assist patients in the rehabilitation process after a foot injury. The iOS application serves as a tool to recieve information sent from the bluetooth transmitter embedded within the hardware. The application will showcase information and provide summaries similar to Apple's Health app.

### App Evaluation
- **Category:** 
- **Mobile:** 
- **Story:**
- **Market:** 
- **Habit:** 
- **Scope:** 

## Product Spec
### 1. User Stories (Required and Optional)

**Required Must-have Stories**

* 
* 
* 
* 
* 

**Optional Nice-to-have Stories**

* 


### 2. Screen Archetypes

* 

### 3. Navigation

**Tab Navigation** (Tab to Screen)

**Flow Navigation** (Screen to Screen)


## Digital Wireframes

### [BONUS] Interactive Prototype

### 4. Models

**user object**

**height object**

**date object**


### 5. Outline Network Requests

* Sign In Screen
  * (Read/GET) sign up users
  * (Read/GET) tap forget password to fetch the password
* Sign Up Screen
  * (Create/POST) create users
* Account Info Screen
  * (Create/POST) create account information
* Personal Info Screen
  * (Create/POST) create personal info

## Sprint 1
# Solemate README

## Table of Contents
1. [Overview](#Overview)
2. [Product Spec](#Product-Spec)
3. [Wireframes](#Digital-Wireframes)

## Overview
### Description
Solemate is a shoe insert that tracks foot pressures in order to assist patients in the rehabilitation process after a foot injury. The iOS application serves as a tool to recieve information sent from the bluetooth transmitter embedded within the hardware. The application will showcase information and provide summaries similar to Apple's Health app.

### App Evaluation
- **Category:** Health Care
- **Mobile:** This app would be primarily developed for mobile. 
- **Story:** The application allows you to create a user profile and start tracking your foot pressures via Bluetooth within the insole. Data is pushed to the application and processed into an easily digestible form for users. Information summaries can be used to adjust choices in the rehabilitation process.
- **Market:** Individuals who have had injuries in the lower extremity.
- **Habit:** This app would ideally be used at least once a day to continue tracking progress in the rehabilitation process.
- **Scope:** TODO

## Product Spec
### 1. User Stories (Required and Optional)

**Required Must-have Stories**

* User logs in to summaries and other pertinent information
* User begins the tracking process by pressing the start button and proceeds to walk a set distance.
* Application analyzes data and shows real time feedback
* Profile page 
* Settings (Accesibility, Notification, General, etc.)

**Optional Nice-to-have Stories**

* Profile add ons: height, weight, gender, etc.


### 2. Screen Archetypes

* Login 
* Register - User signs up or logs into their account
   * Upon Download/Reopening of the application, the user is prompted to log in to gain access to their profile information to be properly matched with another person. 
   * ...
* Profile Screen 
   * Allows user to upload a photo and fill in information that is interesting to them and others
* Summary Screen
  * User accesses aggregate data from all previous tests
* Settings Screen
   * Lets people change language, and app notification settings.

### 3. Navigation

**Tab Navigation** (Tab to Screen)

* Summary
* Dashboard
* Profile
* Settings

Optional:
* etc

**Flow Navigation** (Screen to Screen)
* Forced Log-in -> Account creation if no log in is available
* Information set up process
* Start test 
* Settings

## Digital Wireframes
![Alt text](/img_assets/Wireframes.png?raw=true "Wireframes")

### [BONUS] Interactive Prototype
<img src="http://g.recordit.co/B2r87BPmTs.gif" width=200>

### 4. Models

**user object**

| Property    | Type    | Description                       |
|-------------|---------|-----------------------------------|
| userID      | Int     | the user ID                       |
| firstName   | String  | first name of the user            |
| lastName    | String  | second name of the user           |
| gender      | String  | the gender of the user            |
| dateOfBirth | Date    | the user's date of birth          |
| height      | Height  | the user's height                 |
| weight      | Int     | the user's weight                 |
| rehabTime   | Int     | the user's rehab time             |
| goalWeight  | Int     | the user's weight gain percentage |
| condition   | String  | the injury condition              |
| date        | DateObj | the date of the injury            |

**height object**

| Property | Type  | Description           |
|----------|-------|-----------------------|
| feet     | Int   | height in feet        |
| inches   | Int   | height in inches      |
| cm       | Int   | height in centermeter |

**date object**

| Property  | Type | Description |
|-----------|------|-------------|
| day       | Int  | day         |
| month     | Int  | month       |
| year      | Int  | year        |

### 5. Outline Network Requests

* Sign In Screen
  * (Read/GET) sign up users
  * (Read/GET) tap forget password to fetch the password
* Sign Up Screen
  * (Create/POST) create users
* Account Info Screen
  * (Create/POST) create account information
* Personal Info Screen
  * (Create/POST) create personal info

## Sprint 1

**Design**
- [ ] create app icon in various sizes for Xcode
- [x] provide all image assets to Steven
- [x] Finish developing Hi-Fi's

**Development**
- [ ] Compute data from real time feedback
- [x] post information into Firebase database
- [x] get requests to database for summary data
- [x] display calculated summary data


