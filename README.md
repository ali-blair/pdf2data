# pdf2data 
### Description/Overview
Flask has been used to generate a web app in python. The web app is to be run on a local machine or a server which can then be accessed by users with the generated link. The web app allows a user to input a pdf file from their local machine and select specific locations on a pdf page at which they want to extract the text/data from (this is iterated over all pages of the pdf). The user has the choice of using a text reader to extract the data from the pdf, or from optical character recognition software (OCR) via pytesseract and opencv, or both.
### Further Notes
- The login feature is currently under progress and the user needs to input 'admin' as the username and 'admin' as the password to have access to the app.

More on Text Reading: The pdf is first cropped, then the text is read.

More on OCR: The pdf is first cropped, then saved as a jpeg which then undergoes enhancements (greyscale conversion + more colouring effects) before OCR takes place to maximize effectiveness.

**Currently only works for windows
### Roadmap
- [x] Works for pre-defined areas on pdf page (mainly chunks in bottom right) as that was what was required for a specific document I was working with in recent times. The specific document needed chunks of data in boxes from bottom right of pdfs to be extracted.
- [ ] Allow the user to interact further with the html page and draw boxes onto the inputted pdf (perhaps convert the input to a single jpg page as preview) to identify where exactly on the pdf the user would like to extract data from.
- [ ] Improve the login design, introduce hashing for privacy and a file in which the user can input usernames and passwords with which they want to allow access to.
- [ ] Shift over javascript code and functions from within the html pages' scripts to a new .js file located within the \static folder for tidyness
- [ ] Design web pages to be more visually appealing
